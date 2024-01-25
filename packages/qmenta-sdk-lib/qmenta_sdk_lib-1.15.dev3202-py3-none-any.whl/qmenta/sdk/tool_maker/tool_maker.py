import glob
import inspect
import json
import logging
import os
import shlex
import shutil
import subprocess
from numbers import Number
from types import SimpleNamespace
from typing import List, Union
from collections.abc import Mapping

from qmenta.sdk.context import AnalysisContext
from qmenta.sdk.local.context import LocalAnalysisContext
from qmenta.sdk.local.parse_settings import parse_tool_settings

from .make_files import build_local_dockerfile, build_local_requirements
from .context import TestFileInput
from .file_filter import ConditionForFilter
from .inputs import (
    CheckBox,
    ContainerHandler,
    Decimal,
    Heading,
    IndentText,
    InfoText,
    Integer,
    Line,
    MultipleChoice,
    Options_type,
    SingleChoice,
    String,
    SubjectHandler,
)
from .run_test_docker import run_docker
from .modalities import Modality


def add_container_filters(file_list: List) -> str:
    final_file_filter = list()
    or_file_filter = list()
    for idx, inp in enumerate(file_list):
        if not isinstance(inp, list):
            conditions = list()
            if not isinstance(inp.filter_file, list):
                inp.filter_file = [inp.filter_file]

            for idf, inf in enumerate(inp.filter_file):
                filter_file_conditions = list()
                if inf.modality != Modality.none:
                    filter_file_conditions.append(inf.modality)
                if inf.tags:
                    filter_file_conditions.append(inf.tags)
                if inf.regex != ".*":
                    filter_file_conditions.append(inf.regex)
                conditions.append((filter_file_conditions, idf))

            file_filter = ConditionForFilter(inp.id, conditions, min_files=inp.min_files, max_files=inp.max_files)
            final_file_filter.append(f"{inp.id}{file_filter}" if inp.mandatory else f"({inp.id}{file_filter} OR TRUE)")

        else:
            and_section = add_container_filters(inp)
            if idx > 0 and isinstance(file_list[idx - 1], list):
                or_file_filter.append(and_section)
            else:
                or_file_filter = list()
                final_file_filter.append(and_section)

    if or_file_filter:
        [final_file_filter.append(el) for el in or_file_filter]
        final_file_filter = "(" + " OR ".join(final_file_filter) + ")"
        return final_file_filter
    else:
        final_file_filter = (
            " AND ".join(final_file_filter) if len(file_list) == 1 else "(" + " AND ".join(final_file_filter) + ")"
        )
        return final_file_filter


def create_setting_values_json(args: SimpleNamespace, input_folder: str, settings=None):
    if settings is None:
        settings = []

    class MyEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Mapping):
                return {}
            if not isinstance(o, TestFileInput):
                print(o)
                return o.__dict__
            attrs = ["path", "modality", "tags", "file_filter_condition_name", "file_info"]
            return {a: getattr(o, a) for a in attrs if bool(getattr(o, a))}

    outfile = os.path.join(input_folder, "setting_values.json")
    encoded = json.dumps(args.__dict__, indent=2, cls=MyEncoder)
    if settings:
        for k, v in args.__dict__.items():
            if (
                k != "test_name"
                and k != "sample_data_folder"
                and not sum([s["id"] == k for s in settings if "id" in s]) == 1
            ):
                raise KeyError(f"Key {k} defined in test arguments, not found in settings.")
    with open(outfile, "w") as f:
        f.write(encoded)
    return outfile


class FilterFile:
    def __init__(
        self,
        modality: Union[Modality, List[Modality]] = Modality.none,
        tags=None,
        regex: str = ".*",
    ):
        if tags is None:
            tags = list()
        self.modality = modality
        self.tags = tags
        self.regex = regex


class InputFile:
    def __init__(
        self,
        file_filter_condition_name: str,
        filter_file: Union[FilterFile, List[FilterFile]] = FilterFile(regex=".*"),
        mandatory: int = 1,
        min_files: int = 1,
        max_files: Union[int, str] = "*",
    ):
        """

        :param file_filter_condition_name:
            Is the ID that will be used to define the file filter condition name as 'c_{id_}' and also used
            to get the file in the tool from the self.inputs.{container_id} dictionary
        :param mandatory:
            Used to add the clause 'OR TRUE' in the file filter to make that file optional
        :param min_files:
            Specify the minimum number of files that are accepted using this filter
        :param max_files:
            Specify the maximum number of files that are accepted using this filter
        """
        self.id = file_filter_condition_name
        self.filter_file = filter_file
        self.mandatory = mandatory
        self.min_files = min_files
        self.max_files = max_files


class Tool:
    def __init__(self, context=None, testing_tool=False):
        self.context = context
        self.inputs = SimpleNamespace()
        self.testing = True if context is None else False
        self._inputs = []
        self.testing_tool = testing_tool

        self.tool_inputs()
        self.tool_path = os.path.dirname(inspect.getfile(self.__class__))
        self.settings_path = os.path.join(self.tool_path, "settings.json")

    def tool_inputs(self):
        if not self.testing_tool:
            raise NotImplementedError("You forgot to define the inputs in tool_inputs")

    def run(self, context=None):
        raise NotImplementedError("You forgot to implement the run method")

    def tool_outputs(self):
        pass

    def add_input_container(
        self,
        container_id: str,
        file_list: Union[List[InputFile], List[List[InputFile]]],
        title: str = "",
        info: str = "",
        anchor: int = 1,
        batch: int = 1,
        mandatory: int = 1,
        out_filter=None,
    ):
        if out_filter is None:
            out_filter = list()
        _final_file_filter = add_container_filters(file_list)
        container = ContainerHandler(
            id_=container_id,
            file_filter=_final_file_filter,
            title=title,
            info=info,
            anchor=anchor,
            batch=batch,
            mandatory=mandatory,
            out_filter=out_filter,
        )
        self._inputs.append(container)

    def add_subject(
        self,
        container_id: str,
        file_list: Union[List[InputFile], List[List[InputFile]]],
        title: str = "",
        info: str = "",
        anchor: int = 1,
        batch: int = 1,
        mandatory: int = 1,
        out_filter=None,
    ):
        if out_filter is None:
            out_filter = list()
        _final_file_filter = add_container_filters(file_list)
        self._inputs.append(
            SubjectHandler(
                id_=container_id,
                file_filter=_final_file_filter,
                title=title,
                info=info,
                anchor=anchor,
                batch=batch,
                mandatory=mandatory,
                out_filter=out_filter,
            )
        )

    def add_input_single_choice(self, id_: str, options: Options_type, default: object, title: str = ""):
        opt = SingleChoice(id_, options, default, title)
        if default not in [o[0] for o in options]:
            raise ValueError(f"Default value [{default}] not in options {[o[0] for o in options]}")
        self._inputs.append(opt)
        setattr(self.inputs, id_, opt)

    def add_input_multiple_choice(self, id_: str, options: Options_type, default: List[object], title: str = ""):
        opt = MultipleChoice(id_, options, default, title)
        for defa in default:
            if defa not in [o[0] for o in options]:
                raise ValueError(f"Default value ({defa}) not in options {[o[0] for o in options]}")
        self._inputs.append(opt)
        setattr(self.inputs, id_, opt)

    def add_input_checkbox(self, id_: str, default: int, title: str = ""):
        self._inputs.append(CheckBox(id_, title, default))

    def add_input_string(self, id_: str, default: str, title: str = ""):
        self._inputs.append(String(id_, title, default))

    def add_input_decimal(self, id_: str, default: Number, title: str = "", minimum=-1e9, maximum=1e9):
        self._inputs.append(Decimal(id_, title, default, minimum, maximum))

    def add_input_integer(self, id_: str, default: Number, title: str = "", minimum=0, maximum=1e9):
        self._inputs.append(Integer(id_, title, default, minimum, maximum))

    def add_line(self):
        self._inputs.append(Line())

    def add_heading(self, content: str):
        self._inputs.append(Heading(content))

    def add_info(self, content: str):
        self._inputs.append(InfoText(content))

    def add_indent(self, content: str):
        self._inputs.append(IndentText(content))

    def prepare_inputs(self, context: Union[AnalysisContext, LocalAnalysisContext], logger: logging.Logger):
        """
        Prepare the inputs for the tool. Downloads the data and sets input variables for the tool.

        Parameters
        ----------
        context: AnalysisContext or LocalAnalysisContext
            The context of the analysis given by the SDK
        logger: logging.Logger
            The logger to use for logging

        """
        context.fetch_analysis_data()
        for inp in self._inputs:
            if (
                isinstance(inp, Line)
                or isinstance(inp, Heading)
                or isinstance(inp, InfoText)
                or isinstance(inp, IndentText)
            ):
                continue
            # TODO: how can we handle this better?
            try:
                setattr(self.inputs, inp.id, inp.get_input(context))
            except Exception as e:
                logger.error(f"Could not download input: {e}")
                if inp.mandatory:
                    raise
                setattr(self.inputs, inp.id, None)

    def generate_settings_file(self) -> list:
        """
        Generates a settings file for the tool.
        """
        settings = [iw.__dict__ for iw in self._inputs]
        encoded = json.dumps(settings, indent=2)
        if not self.testing_tool:
            with open(self.settings_path, "w") as f:
                f.write(encoded)
        return settings

    def copy_input_files_to_folder(self, args: dict) -> SimpleNamespace:
        """
        Copy all input files to a folder.
        Parameters
        ----------
        args: SimpleNamespace
            The arguments passed to the tool.

        """
        logger = logging.getLogger(__name__)
        input_folder = os.path.join(self.tool_path, "local", "test", args["test_name"], "input_folder")
        sample_data_folder = os.path.join(self.tool_path, "local", "test", args["sample_data_folder"])
        tools_resources = glob.glob(
            os.path.join(self.tool_path, "local", "test", "tools_resources", "**", "*.*"), recursive=True
        )
        execution_folder = os.path.join(self.tool_path, "local", "test", args["test_name"], "execution_folder")
        for res in tools_resources:
            rel_path = os.path.relpath(res, os.path.join(self.tool_path, "local", "test"))
            os.makedirs(os.path.dirname(os.path.join(execution_folder, rel_path)), exist_ok=True)
            shutil.copy(res, os.path.join(execution_folder, rel_path))

        new_args = args
        for id_key in args:
            ref_test_file = None
            argument_files = None
            mandatory = None
            if isinstance(args[id_key], dict) and "files" in args[id_key]:
                argument_files = args[id_key]["files"]
                mandatory = args[id_key]["mandatory"]
                ref_test_file = args[id_key]["files"][0]
            elif isinstance(args[id_key], list) and isinstance(args[id_key][0], TestFileInput):
                # TO DEPRECATE THIS CASE in the near future
                argument_files = args[id_key]
                mandatory = True  # before this was not taken into account, always True
                ref_test_file = args[id_key][0]
            if ref_test_file is None:
                continue

            new_files_id = list()
            failed_copy_files = 0
            is_one_mandatory = False
            for lfile in argument_files:
                is_one_mandatory = is_one_mandatory or lfile.mandatory
                if os.path.isdir(os.path.join(sample_data_folder, lfile.path)):
                    dst = os.path.join(input_folder, id_key, lfile.path)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    src = os.path.join(sample_data_folder, lfile.path)
                    for filename in glob.glob(os.path.join(src, "**"), recursive=True):
                        if os.path.isdir(filename):
                            # skip folder
                            continue
                        rel_path = os.path.relpath(filename, os.path.join(sample_data_folder, lfile.path))
                        dst = os.path.join(input_folder, id_key, lfile.path, rel_path)
                        src = filename
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        # Copy to input folder
                        try:
                            shutil.copy(src, dst)
                        except FileNotFoundError:
                            if mandatory:
                                raise
                            logger.error(f"File not found in optional argument: {src}")
                            failed_copy_files += 1
                            break

                        # Include file in args. Modality is not considered
                        newfileinput = TestFileInput(
                            path=os.path.join(lfile.path, rel_path),
                            file_name_path=os.path.join(lfile.path, rel_path),
                            file_filter_condition_name=ref_test_file.file_filter_condition_name,
                            file_info=ref_test_file.file_info,
                            tags=ref_test_file.tags,
                            regex=ref_test_file.regex,
                            mandatory=ref_test_file.mandatory,
                        )
                        new_files_id.append(newfileinput)

                else:
                    # Copy the source files
                    dst = os.path.join(input_folder, id_key, lfile.path)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    src = os.path.join(sample_data_folder, lfile.path)
                    try:
                        shutil.copy(src, dst)
                    except FileNotFoundError:
                        failed_copy_files += 1
                        if mandatory and len(argument_files) == failed_copy_files:
                            raise ValueError(f"All files not found in mandatory argument {id_key}")

                        logger.error(f"File not found in optional argument: {src}")
                    new_files_id.append(lfile)

            # if files in the defined folder in test where added as TestFileInput, replace the value in the
            # setting id so the download gets the files instead of the folder.
            # setting id so the download gets the files instead of the folder.
            new_args[id_key] = new_files_id
            if mandatory and not is_one_mandatory:
                raise Exception(
                    f"The setting input {id_key} is set to mandatory but none of the condition filters is mandatory. "
                    f"At least one should be mandatory. Make sure you have defined the 'mandatory' argument in the"
                    f" 'TestFileInput' of you local test"
                )
            elif not mandatory and is_one_mandatory:
                raise Exception(
                    f"The setting input {id_key} is NOT set to mandatory and there is one condition filter is set to "
                    f"mandatory. All filters in this input should be set NOT mandatory. Make sure you have defined "
                    f"the 'mandatory' argument in the 'TestFileInput' of you local test"
                )

        return SimpleNamespace(**new_args)

    def test_with_args(self, in_args: dict, overwrite_settings: bool = True, refresh_test_data: bool = False) -> None:
        """
        Run the tool with the given arguments.

        Parameters
        ----------
        in_args: dict
            The arguments to pass to the tool.
        overwrite_settings: bool
            If True, the settings file will be overwritten with the current settings.
        refresh_test_data: bool
            If True, the test data will be removed, and it will create the folder structure and copy the files again.
        """
        args = SimpleNamespace(**in_args)
        local_test_folder = os.path.join(self.tool_path, "local", "test", args.test_name)

        settings = dict()
        if overwrite_settings:
            settings = self.generate_settings_file()
        if refresh_test_data and os.path.exists(local_test_folder):
            shutil.rmtree(local_test_folder)

        current_dir = os.getcwd()  # Remember the current directory
        # Create input folder
        input_folder = os.path.join(local_test_folder, "input_folder")
        os.makedirs(input_folder, exist_ok=True)

        # Create execution folder
        exec_folder = os.path.join(local_test_folder, "execution_folder")
        os.makedirs(exec_folder, exist_ok=True)

        # Create output folder
        out_folder = os.path.join(local_test_folder, "output_folder")
        os.makedirs(out_folder, exist_ok=True)

        # Copy input files to input folder and update settings_values for folders
        input_settings = os.path.join(input_folder, "setting_values.json")
        if refresh_test_data or not os.path.exists(input_settings):
            args = self.copy_input_files_to_folder(in_args)

            # Create settings_values.json in input_folder
            input_settings = create_setting_values_json(args, input_folder, settings)

        # Parse settings
        settings = parse_tool_settings(self.settings_path, input_settings)

        # Instantiate local context
        context = LocalAnalysisContext(settings, input_folder, out_folder, "")

        # Change to execution folder
        os.environ["MINTEXE_PATH"] = exec_folder

        # Run the tool
        logger = logging.getLogger("main")
        logger.setLevel(logging.INFO)
        file_ch = logging.FileHandler("logger.log", "w")
        file_ch.setLevel(logging.INFO)
        logger.addHandler(file_ch)
        logger.info("This is the execution log --> Starting context.")

        self.tool_outputs()
        self.run(context)

        # Back to the original directory
        os.chdir(current_dir)

    def test_docker_with_args(
        self,
        folder_exec: str,
        in_args: dict,
        overwrite_output: bool = True,
        stop_container: bool = True,
        delete_container: bool = True,
        attach_container: bool = True,
    ):
        # Parse in_args as SimpleNameSpace
        # Load the requirements from the build yaml file
        local_folder = os.path.join(self.tool_path, "local")
        os.chdir(local_folder)  # move here to create the nDockerfile and requirements.txt

        build_local_requirements()
        build_local_dockerfile()

        os.chdir(self.tool_path)
        args = SimpleNamespace(**in_args)
        # Build the Docker image found in the Dockerfile
        local_tests_folder = os.path.join(local_folder, "test")
        local_test_folder = os.path.join(local_tests_folder, args.test_name)
        # run the docker build commandline
        base_image_name = os.path.basename(self.tool_path)
        # copy the tool.py file in the tool path to the local folder
        shutil.copy(os.path.join(self.tool_path, "tool.py"), os.path.join(self.tool_path, "local"))
        docker_build_command = f"docker build -t {base_image_name} ."
        print(f"Building the docker image {os.path.basename(self.tool_path)}...")
        print(docker_build_command)

        os.chdir(local_folder)
        process = subprocess.Popen(shlex.split(docker_build_command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, error_data = process.communicate(timeout=99999)  # Halts execution until process finishes
        if process.returncode:
            raise OSError(error_data)
        # The following folders should already exist because we have run the tool locally, otherwise create them
        # Create input folder
        input_folder = os.path.join(local_test_folder, "input_folder")
        os.makedirs(input_folder, exist_ok=True)

        # Create execution folder
        exec_folder = os.path.join(local_test_folder, "execution_folder")
        os.makedirs(exec_folder, exist_ok=True)

        # Create output folder
        out_folder = os.path.join(local_test_folder, "output_folder")
        os.makedirs(out_folder, exist_ok=True)

        run_docker(
            image=base_image_name,
            inputs=input_folder,
            outputs=out_folder,
            overwrite_output=True,
            settings=os.path.join(self.tool_path, "settings.json"),
            values=os.path.join(input_folder, "setting_values.json"),
            mounts=[f"{self.tool_path}/tool.py:{folder_exec}/tool.py"],
            resources=os.path.join(local_tests_folder),
            stop_container=stop_container,
            delete_container=delete_container,
            attach_container=attach_container,
        )

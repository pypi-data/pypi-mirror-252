"""
Parsers provided by aiida_gromacs.

This calculation configures the ability to use the 'gmx mdrun' executable.
"""
import os
import json
from aiida.common import exceptions
from aiida.engine import ExitCode
from aiida.orm import SinglefileData, Dict
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory
from aiida_gromacs.utils import fileparsers

MdrunCalculation = CalculationFactory("gromacs.mdrun")


class MdrunParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a MdrunCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.nodes.process.process.ProcessNode`
        """
        super().__init__(node)
        if not issubclass(node.process_class, MdrunCalculation):
            raise exceptions.ParsingError("Can only parse MdrunCalculation")

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        # the directory for storing parsed output files
        output_dir = self.node.get_option("output_dir")
        # Map output files to how they are named.
        outputs = ["stdout"]
        output_template = {
                "c": "grofile",
                "e": "enfile",
                "g": "logfile",
                "o": "trrfile",
                "x": "x_file",
                "cpo": "cpo_file",
                "dhdl": "dhdl_file",
                "field": "field_file",
                "tpi": "tpi_file",
                "tpid": "tpid_file",
                "eo": "eo_file",
                "px": "px_file",
                "pf": "pf_file",
                "ro": "ro_file",
                "ra": "ra_file",
                "rs": "rs_file",
                "rt": "rt_file",
                "mtx": "mtx_file",
                "if": "if_file",
                "swap": "swap_file"
            }

        for item in output_template:
            if item in self.node.inputs.parameters.keys():
                outputs.append(output_template[item])

        # Grab list of retrieved files.
        files_retrieved = self.retrieved.base.repository.list_object_names()

        # Grab list of files expected and remove the scheduler stdout and stderr files.
        files_expected = [files for files in self.node.get_option("retrieve_list") if files not in ["_scheduler-stdout.txt", "_scheduler-stderr.txt"]]

        # Check if the expected files are a subset of retrieved.
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error(
                f"Found files '{files_retrieved}', expected to find '{files_expected}'"
            )
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # Map retrieved files to data nodes.
        for i, f in enumerate(files_expected):
            self.logger.info(f"Parsing '{f}'")
            with self.retrieved.base.repository.open(f, "rb") as handle:
                output_node = SinglefileData(filename=f, file=handle)
            self.out(outputs[i], output_node)
            # Include file parsers here
            if outputs[i] == "logfile":
                MdrunParser.parse_file_contents(self, f, output_dir,
                                    fileparsers.parse_gromacs_logfile, 
                                    node_name="logfile_metadata")

        # If not in testing mode, then copy back the files.
        if "PYTEST_CURRENT_TEST" not in os.environ:
            self.retrieved.copy_tree(output_dir)

        return ExitCode(0)
    
    def parse_file_contents(self, f, output_dir, parser_func, node_name):
        """
        Read in the gromacs output file, save into a dictionary node and 
        output dictionary as a json file.

        :param f: the name of the file node outputted from mdrun for parsing
        :type f: str
        :param output_dir: path to where json file should be saved
        :param parser_func: the function used to parse the file f
        :type parser_func: `class 'function'`
        :param node_name: the name of the outputted Dict node
        :type node_name: str
        """
        metadata_dict = parser_func(self, f)
        metadata_node = Dict(metadata_dict)
        self.out(node_name, metadata_node)
        MdrunParser.output_parsed_metadata(f, output_dir, metadata_dict)


    def output_parsed_metadata(f, output_dir, metadata_dict):
        """
        Save a dictionary into a json file if not in testing mode.

        :param f: the name of the file node outputted from mdrun
        :param output_dir: path to where json file should be saved
        :param metadata_dict: the aiida dictionary containing metadata
        """
        # If not in testing mode, then copy back dict as json file.
        if "PYTEST_CURRENT_TEST" not in os.environ:
            f_prefix = f.split(".")[0]
            file_path = os.path.join(output_dir, f"{f_prefix}_metadata.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata_dict, f, ensure_ascii=False, indent=4)
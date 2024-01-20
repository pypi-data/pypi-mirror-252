from dotenv import load_dotenv, find_dotenv, set_key
from cdh_dav_python.cdc_metadata_service.environment_metadata import (
    EnvironmentMetaData,
)

import cdh_dav_python.cdc_admin_service.sequence_diagram as cdc_sequence_diagram
import cdh_dav_python.cdc_tech_environment_service.environment_file as cdc_env_file

import pytest
from unittest.mock import patch
import sys
import os
from unittest.mock import Mock
from pathlib import Path
import unittest

sys.path.append("..")

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


ENVIRONMENT = "dev"

# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)

# Get the project root directory by going up one or more levels
project_root = os.path.dirname(os.path.dirname(current_script_path))

# Change the current working directory to the project root directory
os.chdir(project_root)

REPOSITORY_PATH_DEFAULT = str(Path(os.getcwd()))

parameters = {
    "data_product_id": "wonder_metadata",
    "data_product_id_root": "wonder",
    "data_product_id_individual": "metadata",
    "environment": "dev",
    "repository_path": REPOSITORY_PATH_DEFAULT,
}


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


class TestCDCAdminSequenceDiagram(unittest.TestCase):
    def get_config(self, parameters):
        environment_metadata = EnvironmentMetaData()
        config = environment_metadata.get_configuration_common(parameters, None)
        return config

    def test_generate_timeline_download_manifest_excel_synapse(self):
        # Change the current working directory to the project root directory
        os.chdir(project_root)

        config = self.get_config(parameters)

        # Get the file utility object
        obj_file = cdc_env_file.EnvironmentFile()

        # Get the manifest file
        app_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(app_dir)
        log_path = parent_dir + "/" + ENVIRONMENT + "_log_trace_sequence/"
        log_path = obj_file.convert_to_current_os_dir(log_path)
        # Make sure you have put a file in the uploads directory

        sequence_diagram = cdc_sequence_diagram.SequenceDiagram()
        timeline_string = sequence_diagram.generate_timeline(
            log_path=log_path, file_name="download_manifest_excel_synapse.xlsx"
        )
        print(f"timeline_string: {timeline_string}")

    def test_generate_timeline_download_manifest_excel_dcipher(self):
        # Change the current working directory to the project root directory
        os.chdir(project_root)

        # Get the file utility object
        obj_file = cdc_env_file.EnvironmentFile()

        # Get the manifest file
        app_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(app_dir)
        log_path = parent_dir + "/" + ENVIRONMENT + "_log_trace_sequence/"
        log_path = obj_file.convert_to_current_os_dir(log_path)
        # Make sure you have put a file in the uploads directory

        sequence_diagram = cdc_sequence_diagram.SequenceDiagram()
        timeline_string = sequence_diagram.generate_timeline(
            log_path=log_path, file_name="download_manifest_excel_dcipher.xlsx"
        )
        print(f"timeline_string: {timeline_string}")

    def test_generate_diagram(self):
        # Change the current working directory to the project root directory
        os.chdir(project_root)

        config = self.get_config(parameters)

        # Get the file utility object
        obj_file = cdc_env_file.EnvironmentFile()

        # Get the manifest file
        app_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(app_dir)
        log_path = parent_dir + "/" + ENVIRONMENT + "_log_trace_sequence/"
        log_path = obj_file.convert_to_current_os_dir(log_path)
        # Make sure you have put a file in the uploads directory

        sequence_diagram = cdc_sequence_diagram.SequenceDiagram()
        mermaid_diagram_string = sequence_diagram.generate_diagram(
            log_path=log_path, file_name="download_manifest_excel_dcipher.xlsx"
        )
        print(mermaid_diagram_string)

    def test_validate_application_insights_connection_string():
        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        validated_connection_string = (
            logger_singleton.validate_application_insights_connection_string()
        )
        print(validated_connection_string)

        # Assert the result
        assert len(validated_connection_string) > 0


if __name__ == "__main__":
    pytest.main()

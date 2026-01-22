import json
import sys
import os

import pandas as pd

from pandas import DataFrame

from src.exception import MyException
from src.logger import logging
from src.utils.utils_main import read_yaml_file
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_validation_config: configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)
        
    def validate_schema_columns(self, df: DataFrame) -> bool:

        expected_columns = set(self._schema_config["columns"].keys())
        actual_columns = set(df.columns)

        missing_columns = expected_columns - actual_columns
        extra_columns = actual_columns - expected_columns

        if missing_columns:
            logging.error(f"Missing columns: {missing_columns}")

        if extra_columns:
            logging.error(f"Unexpected columns: {extra_columns}")

        return len(missing_columns) == 0 and len(extra_columns) == 0


    # def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
    #     """
    #     Method Name :   validate_number_of_columns
    #     Description :   This method validates the number of columns
        
    #     Output      :   Returns bool value based on validation results
    #     On Failure  :   Write an exception log and then raise an exception
    #     """
    #     try:
    #         status = len(dataframe.columns) == len(self._schema_config["columns"])
    #         logging.info(f"Is required column present: [{status}]")
    #         return status
    #     except Exception as e:
    #         raise MyException(e, sys)

    # def is_column_exist(self, df: DataFrame) -> bool:
    #     """
    #     Method Name :   is_column_exist
    #     Description :   This method validates the existence of a numerical and categorical columns
        
    #     Output      :   Returns bool value based on validation results
    #     On Failure  :   Write an exception log and then raise an exception
    #     """
    #     try:
    #         dataframe_columns = df.columns
    #         missing_numerical_columns = []
    #         missing_categorical_columns = []
    #         for column in self._schema_config["numerical_columns"]:
    #             if column not in dataframe_columns:
    #                 missing_numerical_columns.append(column)

    #         if len(missing_numerical_columns)>0:
    #             logging.info(f"Missing numerical column: {missing_numerical_columns}")


    #         for column in self._schema_config["categorical_columns"]:
    #             if column not in dataframe_columns:
    #                 missing_categorical_columns.append(column)

    #         if len(missing_categorical_columns)>0:
    #             logging.info(f"Missing categorical column: {missing_categorical_columns}")

    #         return False if len(missing_categorical_columns)>0 or len(missing_numerical_columns)>0 else True
    #     except Exception as e:
    #         raise MyException(e, sys) from e

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)
        
        
    def validate_column_types(self, df: DataFrame) -> bool:

        schema_columns = self._schema_config["columns"]
        errors = []

        for col, expected_type in schema_columns.items():
            if col not in df.columns:
                continue

            if expected_type == "int" and not pd.api.types.is_integer_dtype(df[col]):
                errors.append(col)

            elif expected_type == "float" and not pd.api.types.is_float_dtype(df[col]):
                errors.append(col)

            elif expected_type == "category" and not pd.api.types.is_object_dtype(df[col]):
                errors.append(col)

        if errors:
            logging.error(f"Column type mismatch: {errors}")

        return len(errors) == 0


    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """

        try:
            validation_error_msg = ""
            logging.info("Starting data validation")
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

            # Checking col len of dataframe for train/test df
            status = self.validate_schema_columns(train_df)
            if not status:
                validation_error_msg += "Schema mismatch in training data. "

            # status = self.validate_number_of_columns(dataframe=train_df)
            # if not status:
            #     validation_error_msg += f"Columns are missing in training dataframe. "
            else:
                logging.info(f"All required columns present in training dataframe: {status}")

            status = self.validate_schema_columns(test_df)
            if not status:
                validation_error_msg += "Schema mismatch in testing data. "

            # status = self.validate_number_of_columns(dataframe=test_df)
            # if not status:
            #     validation_error_msg += f"Columns are missing in test dataframe. "
            else:
                logging.info(f"All required columns present in testing dataframe: {status}")

            # Validating col dtype for train/test df
            status = self.validate_column_types(df=train_df)
            if not status:
                validation_error_msg += f"Columns data type mismatch in training dataframe. "
            else:
                logging.info(f"All column data types are valid in training dataframe: {status}")


            status = self.validate_column_types(df=test_df)
            if not status:
                validation_error_msg += f"Columns data type mismatch in test dataframe."
            else:
                logging.info(f"All column data types are valid in training dataframe: {status}")

            validation_status = len(validation_error_msg) == 0

            if not validation_status:
                logging.error("Data validation failed. Stopping pipeline.")
                # raise MyException("Data validation failed.", sys)


            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )

            # Ensure the directory for validation_report_file_path exists
            report_dir = os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            # Save validation status and message to a JSON file
            validation_report = {
                "validation_status": validation_status,
                "message": validation_error_msg.strip()
            }

            with open(self.data_validation_config.validation_report_file_path, "w") as report_file:
                json.dump(validation_report, report_file, indent=4)

            logging.info("Data validation artifact created and saved to JSON file.")
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e, sys) from e
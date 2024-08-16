# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=broad-exception-raised
import json
import csv
from io import StringIO
import os
import time
from google.api_core.exceptions import NotFound
from google.cloud.storage import Client as GCSClient
from google.cloud import bigquery
from ipulse_shared_base_ftredge import (DuplicationHandling, DuplicationHandlingStatus, MatchConditionType,DataSourceType, LogLevel,
                                        log_error, log_warning, log_info)
from ipulse_shared_data_eng_ftredge import ContextLog, Pipelinemon

############################################################################
##################### GOOGLE CLOUD PLATFORM UTILS ##################################
############################################################################

def create_bigquery_schema_from_json(json_schema: list) -> list:
    schema = []
    for field in json_schema:
        if "max_length" in field:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"], max_length=field["max_length"]))
        else:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"]))
    return schema


def read_json_from_gcs(storage_client:GCSClient, bucket_name:str, file_name:str, logger=None,print_out=False):
    """ Helper function to read a JSON file from Google Cloud Storage """
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_string = blob.download_as_text()
        data = json.loads(data_string)
        return data
    except NotFound:
        log_warning(msg=f"Warning: The file {file_name} was not found in the bucket {bucket_name}.", logger=logger, print_out=print_out)
        return None
    except json.JSONDecodeError:
        log_error(msg=f"Error: The file {file_name} could not be decoded as JSON.", logger=logger, print_out=print_out)
        return None
    except Exception as e:
        log_error(msg=f"An unexpected error occurred: {e}", exc_info=True, logger=logger, print_out=print_out)
        return None

def  read_json_from_gcs_extended(storage_client:GCSClient, bucket_name:str, file_name:str, pipelinemon:Pipelinemon=None,  logger=None, print_out=False):
    """ Helper function to read a JSON file from Google Cloud Storage with optional Pipelinemon monitoring. """
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_string = blob.download_as_text()
        data = json.loads(data_string)
        if blob.size == 0:
            msg = f"File {file_name} is empty in bucket {bucket_name}"
            logger.warning(msg)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_OPERATION_FAILED, subject=f"blob {file_name} in {bucket_name}", description="blob.size == 0, meaning empty file"))
            return None
        return data
    except NotFound:
        log_warning(msg=f"Warning: The file {file_name} was not found in the bucket {bucket_name}.", logger=logger, print_out=print_out)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(LogLevel.ERROR_OPERATION_FAILED, subject=file_name, description=f"File not found in GCS: {file_name} in bucket {bucket_name}"))
        return None
    except json.JSONDecodeError:
        msg=f"Error decoding JSON from GCS: {file_name} in bucket {bucket_name}"
        log_error(msg=msg, logger=logger, print_out=print_out)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(LogLevel.ERROR_OPERATION_FAILED, subject=file_name, description=msg))
        return None
    except Exception as e:
        msg=f"An unexpected error occurred: {e}"
        log_error(msg=f"An unexpected error occurred: {e}", exc_info=True, logger=logger, print_out=print_out)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(LogLevel.ERROR_EXCEPTION, e=e))
        return None


def read_csv_from_gcs(bucket_name:str, file_name:str, storage_client:GCSClient, logger=None, print_out=False):
    """ Helper function to read a CSV file from Google Cloud Storage """

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_string = blob.download_as_text()
        data_file = StringIO(data_string)
        reader = csv.DictReader(data_file)
        return list(reader)
    except NotFound:
        log_warning(msg=f"Error: The file {file_name} was not found in the bucket {bucket_name}.", logger=logger, print_out=print_out)
        return None
    except csv.Error:
        log_error(msg=f"Error: The file {file_name} could not be read as CSV.", logger=logger, print_out=print_out)
        return None
    except Exception as e:
        log_error(msg=f"An unexpected error occurred: {e}", logger=logger, print_out=print_out, exc_info=True)
        return None

def write_json_to_gcs_extended(storage_client: GCSClient, data: dict | list | str, bucket_name: str, file_name: str,
                                                duplication_handling_enum: DuplicationHandling, duplication_match_condition_type_enum: MatchConditionType,
                                                duplication_match_condition: str = "", max_retries: int = 2, max_deletable_files: int = 1,
                                                logger=None, print_out=False, raise_e=False, pipelinemon: Pipelinemon = None):

    """Saves data to Google Cloud Storage with optional Pipelinemon monitoring.

    Handles duplication with strategies: OVERWRITE, INCREMENT, SKIP, or RAISE_ERROR.

    !! As of now only supporting STRING duplication_match_condition !!
    """

    max_deletable_files_allowed = 3
    cloud_storage_ref=DataSourceType.GCS.value

    # GCS-related metadata
    saved_to_path = None
    matched_duplicates_count = 0
    matched_duplicates_deleted = []
    duplication_handling_status = None
    error_during_operation = None

    response = {
        "saved_to_path": saved_to_path,
        "matched_duplicates_count": matched_duplicates_count,
        "matched_duplicates_deleted": matched_duplicates_deleted,
        "duplication_handling_status": duplication_handling_status,
        "duplication_match_condition_type": duplication_match_condition_type_enum.value,
        "duplication_match_condition": duplication_match_condition,
        "error_during_operation": error_during_operation
    }

    supported_match_condition_types = [MatchConditionType.EXACT, MatchConditionType.PREFIX]
    supported_duplication_handling = [DuplicationHandling.RAISE_ERROR, DuplicationHandling.OVERWRITE, DuplicationHandling.INCREMENT, DuplicationHandling.SKIP]

    try:
        if max_deletable_files > max_deletable_files_allowed:
            raise ValueError(f"max_deletable_files should be less than or equal to {max_deletable_files_allowed} for safety.")
        if duplication_handling_enum not in supported_duplication_handling:
            msg = f"Error: Duplication handling not supported. Supported types: {[dh.value for dh in supported_duplication_handling]}"
            raise ValueError(msg)
        if duplication_match_condition_type_enum not in supported_match_condition_types:
            msg = f"Error: Match condition type not supported. Supported types: {[mct.value for mct in supported_match_condition_types]}"
            raise ValueError(msg)
        elif duplication_match_condition_type_enum != MatchConditionType.EXACT and not duplication_match_condition:
            msg = f"Error: Match condition is required for match condition type: {duplication_match_condition_type_enum.value}"
            raise ValueError(msg)

        # Prepare data
        if isinstance(data, (list, dict)):
            data_str = json.dumps(data, indent=2)
        else:
            data_str = data

        increment = 0
        attempts = 0
        success = False

        # Check for existing files based on duplication_match_condition_type
        files_matched_on_condition = []
        bucket = storage_client.bucket(bucket_name)
        base_file_name, ext = os.path.splitext(file_name)
        if duplication_match_condition_type_enum == MatchConditionType.PREFIX:
            files_matched_on_condition = list(bucket.list_blobs(prefix=duplication_match_condition))
        elif duplication_match_condition_type_enum == MatchConditionType.EXACT:
            duplication_match_condition = file_name if not duplication_match_condition else duplication_match_condition
            if bucket.blob(duplication_match_condition).exists():
                files_matched_on_condition = [bucket.blob(file_name)]

        matched_duplicates_count = len(files_matched_on_condition)
        response["matched_duplicates_count"] = matched_duplicates_count

        # Handle duplication based on duplication_handling
        if matched_duplicates_count:
            log_msg = f"Duplicate FOUND, matched_duplicates_count: {matched_duplicates_count}"
            if pipelinemon:
                    pipelinemon.add_log(ContextLog(LogLevel.NOTICE_ALREADY_EXISTS, subject="duplicate_found", description=log_msg))

            if duplication_handling_enum == DuplicationHandling.RAISE_ERROR:
                raise FileExistsError("File(s) matching the condition already exist.")

            if duplication_handling_enum == DuplicationHandling.SKIP:
                response["duplication_handling_status"] = DuplicationHandlingStatus.SKIPPED.value
                log_msg = f"SKIPPING, response: {response}"
                log_info(log_msg, logger=logger, print_out=print_out) ## only logsor prints if logger is provided and print_out is True
                return response

            if duplication_handling_enum == DuplicationHandling.OVERWRITE:
                if matched_duplicates_count > max_deletable_files:
                    raise ValueError(f"Error: Attempt to delete {matched_duplicates_count} matched files, but limit is {max_deletable_files}. Operation Cancelled.")

                for blob in files_matched_on_condition:
                    cloud_storage_path_to_delete = f"gs://{bucket_name}/{blob.name}"
                    blob.delete()
                    matched_duplicates_deleted.append(cloud_storage_path_to_delete)
                    log_msg = f"File deleted as part of overwrite: {cloud_storage_path_to_delete}"
                    if pipelinemon:
                        pipelinemon.add_system_impacted(f"delete: {cloud_storage_ref}_bucket_file: {cloud_storage_path_to_delete}")
                        pipelinemon.add_log(ContextLog(LogLevel.INFO_REMOTE_DELETE_COMPLETE, subject="delete_duplicate", description=log_msg))
                    log_info(log_msg, logger=logger, print_out=print_out)

                response["matched_duplicates_deleted"] = matched_duplicates_deleted
                response["duplication_handling_status"] = DuplicationHandlingStatus.OVERWRITTEN.value

            elif duplication_handling_enum == DuplicationHandling.INCREMENT:
                while bucket.blob(file_name).exists():
                    increment += 1
                    file_name = f"{base_file_name}_v{increment}{ext}"
                saved_to_path = f"gs://{bucket_name}/{file_name}"
                response["duplication_handling_status"] = DuplicationHandlingStatus.INCREMENTED.value
                log_msg = "INCREMENTING as Duplicate FOUND "
                log_info(log_msg, logger=logger, print_out=print_out) ## only logsor prints if logger is provided and print_out is True

        # GCS Upload
        saved_to_path = f"gs://{bucket_name}/{file_name}"
        while attempts < max_retries and not success:
            try:
                blob = bucket.blob(file_name)
                blob.upload_from_string(data_str, content_type='application/json')
                log_msg = f"File uploaded to GCS: {saved_to_path}"
                if pipelinemon:
                    pipelinemon.add_system_impacted(f"upload: {cloud_storage_ref}_bucket_file: {saved_to_path}")
                    pipelinemon.add_log(ContextLog(LogLevel.INFO_REMOTE_PERSISTNACE_COMPLETE, subject="file_upload", description=log_msg))
                log_info(log_msg, logger=logger, print_out=print_out)
                success = True
            except Exception as e:
                attempts += 1
                if attempts < max_retries:
                    time.sleep(2 ** attempts)
                else:
                    raise e

    except Exception as e:
        error_during_operation = f"Error occurred while writing JSON to GCS path: {saved_to_path} ; Error details: {type(e).__name__} - {str(e)}"
        response["error_during_operation"] = error_during_operation
        if pipelinemon:
            pipelinemon.add_log(ContextLog(LogLevel.ERROR_EXCEPTION, e=e, description="response: {response}"))
        log_error(response, logger=logger, print_out=print_out)
        if raise_e:
            raise e

    response["saved_to_path"] = saved_to_path if success else None
    return response

# def write_json_to_gcs_extended(storage_client: GCSClient, data: dict | list | str, bucket_name: str, file_name: str,
#                                duplication_handling: DuplicationHandling, duplication_match_condition_type: MatchConditionType,
#                                duplication_match_condition: str | List[str] = "", max_retries: int = 2, max_deletable_files: int = 1,
#                                logger=None, print_out=False, raise_e=False):

#     """Saves data to Google Cloud Storage.

#     Handles duplication with strategies: OVERWRITE, INCREMENT, SKIP, or RAISE_ERROR.
#     """

#     max_deletable_files_allowed = 3

#     # GCS-related metadata
#     saved_to_path = None
#     matched_duplicates_count = 0
#     matched_duplicates_deleted = []
#     duplication_handling_status = None
#     error_during_operation = None

#     response = {
#         "saved_to_path": saved_to_path,
#         "matched_duplicates_count": matched_duplicates_count,
#         "matched_duplicates_deleted": matched_duplicates_deleted,
#         "duplication_handling_status": duplication_handling_status,
#         "duplication_match_condition_type": duplication_match_condition_type,
#         "duplication_match_condition": duplication_match_condition,
#         "error_during_operation": error_during_operation
#     }

#     supported_match_condition_types = [MatchConditionType.EXACT, MatchConditionType.PREFIX]
#     supported_duplication_handling = [DuplicationHandling.RAISE_ERROR, DuplicationHandling.OVERWRITE, DuplicationHandling.INCREMENT, DuplicationHandling.SKIP]

#     try:
#         if max_deletable_files > max_deletable_files_allowed:
#             raise ValueError(f"max_deletable_files should be less than or equal to {max_deletable_files_allowed} for safety.")
#         if duplication_handling not in supported_duplication_handling:
#             msg = f"Error: Duplication handling not supported. Supported types: {supported_duplication_handling}"
#             raise ValueError(msg)
#         if duplication_match_condition_type not in supported_match_condition_types:
#             msg = f"Error: Match condition type not supported. Supported types: {supported_match_condition_types}"
#             raise ValueError(msg)
#         elif duplication_match_condition_type!=MatchConditionType.EXACT and not duplication_match_condition:
#             msg = f"Error: Match condition is required for match condition type: {duplication_match_condition_type}"
#             raise ValueError(msg)

#         # Prepare data
#         if isinstance(data, (list, dict)):
#             data_str = json.dumps(data, indent=2)
#         else:
#             data_str = data

#         increment = 0
#         attempts = 0
#         success = False

#         # Check for existing files based on duplication_match_condition_type
#         files_matched_on_condition = []
#         bucket = storage_client.bucket(bucket_name)
#         base_file_name, ext = os.path.splitext(file_name)
#         if duplication_match_condition_type == MatchConditionType.PREFIX:
#             files_matched_on_condition = list(bucket.list_blobs(prefix=duplication_match_condition))
#         elif duplication_match_condition_type == MatchConditionType.EXACT:
#             if bucket.blob(file_name).exists():
#                 files_matched_on_condition = [bucket.blob(file_name)]

#         matched_duplicates_count = len(files_matched_on_condition)
#         response["matched_duplicates_count"] = matched_duplicates_count

#         # Handle duplication based on duplication_handling
#         if matched_duplicates_count:
#             if duplication_handling == DuplicationHandling.RAISE_ERROR:
#                 raise FileExistsError("File(s) matching the condition already exist.")

#             if duplication_handling == DuplicationHandling.SKIP:
#                 log_warning("Skipping saving to GCS: file(s) matching the condition already exist.", logger=logger, print_out=print_out)
#                 response["duplication_handling_status"] = DuplicationHandlingStatus.SKIPPED.value
#                 return response

#             if duplication_handling == DuplicationHandling.OVERWRITE:
#                 if matched_duplicates_count > max_deletable_files:
#                     raise ValueError(f"Error: Attempt to delete {matched_duplicates_count} matched files, but limit is {max_deletable_files}. Operation Cancelled.")

#                 for blob in files_matched_on_condition:
#                     cloud_storage_path_to_delete = f"gs://{bucket_name}/{blob.name}"
#                     blob.delete()
#                     matched_duplicates_deleted.append(cloud_storage_path_to_delete)

#                 response["matched_duplicates_deleted"] = matched_duplicates_deleted
#                 response["duplication_handling_status"] = DuplicationHandlingStatus.OVERWRITTEN.value

#             elif duplication_handling == DuplicationHandling.INCREMENT:
#                 while bucket.blob(file_name).exists():
#                     increment += 1
#                     file_name = f"{base_file_name}_v{increment}{ext}"
#                 saved_to_path = f"gs://{bucket_name}/{file_name}"
#                 response["duplication_handling_status"] = DuplicationHandlingStatus.INCREMENTED.value

#         # GCS Upload
#         saved_to_path = f"gs://{bucket_name}/{file_name}"
#         while attempts < max_retries and not success:
#             try:
#                 blob = bucket.blob(file_name)
#                 blob.upload_from_string(data_str, content_type='application/json')
#                 success = True
#             except Exception as e:
#                 attempts += 1
#                 if attempts < max_retries:
#                     time.sleep(2 ** attempts)
#                 else:
#                     if raise_e:
#                         raise e

#     except Exception as e:
#         error_message = f"Error occurred while writing JSON to GCS path: {saved_to_path} : {type(e).__name__} - {str(e)}"
#         log_error(error_message, logger=logger, print_out=print_out)
#         response["error_during_operation"] = error_message
#         if raise_e:
#             raise e

#     response["saved_to_path"] = saved_to_path if success else None
#     return response


def write_csv_to_gcs(bucket_name:str, file_name:str, data:dict | list | str, storage_client:GCSClient, logger=None, print_out=False, raise_e=False):
    """ Helper function to write a CSV file to Google Cloud Storage """
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_file = StringIO()
        if data and isinstance(data, list) and isinstance(data[0], dict):
            fieldnames = data[0].keys()
            writer = csv.DictWriter(data_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        else:
            raise ValueError("Data should be a list of dictionaries")
        blob.upload_from_string(data_file.getvalue(), content_type='text/csv')
        log_info(msg=f"Successfully wrote CSV to {file_name} in bucket {bucket_name}.", logger=logger, print_out=print_out)
    except ValueError as e:
        log_error(msg=f"ValueError: {e}",logger=logger, print_out=print_out)
        if raise_e:
            raise e
    except Exception as e:
        log_error(msg=f"An unexpected error occurred while writing CSV to GCS: {e}", logger=logger, print_out=print_out, exc_info=True)
        if raise_e:
            raise e

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
import logging
import datetime
from typing import List, Dict, Any, Union, Optional, Tuple, Set
from google.api_core.exceptions import NotFound
from google.cloud import  bigquery
from google.cloud.storage import Client as GCSClient
from ipulse_shared_base_ftredge import (DuplicationHandling, DuplicationHandlingStatus, MatchConditionType,DataSourceType, LogLevel, log_debug, log_info, log_warning, log_error)
from ipulse_shared_data_eng_ftredge import (ContextLog,
                                            Pipelinemon)

############################################################################
##################### GOOGLE CLOUD STORAGE ##################################
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



###########################################################################################
#################################### GOOGLE BIGQUERY ######################################
###########################################################################################

def insert_batch_into_bigquery_extended(project_id: str,
                                    data: Union[Dict[str, Any], List[Dict[str, Any]]],
                                    data_table_full_path: str,
                                    records_ref:str="data", #can be metadata , etc.
                                    max_job_errors_to_log: int=7,
                                    create_table_if_not_exists: bool=False,
                                    bigquery_client: Optional[bigquery.Client] =None,
                                    schema: Optional[List[bigquery.SchemaField]]=None,
                                    pipelinemon: Pipelinemon=None,
                                    logger: Optional[logging.Logger] =None
                                )-> Dict[str, Any]:
    """Executes a BigQuery batch load job and logs the results.
    returns event_results: dict
    """
    if not bigquery_client:
        if not project_id:
            raise ValueError("project_id is required when bigquery_client is not provided.")
        bigquery_client = bigquery.Client(project=project_id)
    event_results={
        "event_operation_state": "NOT_STARTED",
        "event_details": "",
        "event_errors_count": 0,
        "event_exception": ""
    }
    try:
        # Handle single record case consistently
        if isinstance(data, dict):
            data = [data]

        job_config = bigquery.LoadJobConfig()
        if schema:
            job_config.schema = schema
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND  # Append to existing data
        if create_table_if_not_exists:
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED  # Create New table if not exists
        else:
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_NEVER  # Don't create Create New table if not exists

        event_results["event_operation_state"] = "INSERT_JOB_STARTED"
        job =bigquery_client.load_table_from_json(data, data_table_full_path, job_config=job_config,project=project_id)
        job.result()  # Wait for job completion
        event_results['event_operation_state'] = job.state
        event_results["event_errors_count"] = len(job.errors) if job.errors else 0
        event_results["event_details"]= json.dumps({
                                        "bigquery_job_id": job.job_id if job.job_id else "",
                                        "event_job_output_bytes": job.output_bytes if job.output_bytes else 0,
                                        "event_job_output_rows": job.output_rows if job.output_rows else 0,
                                        "event_job_user_email": job.user_email if job.user_email else "",
                                    })
        # Check job status
        if job.state == "DONE" and job.errors is None:
            msg=f"Successful LoadJob {job.job_id} for {records_ref}. Event Results: {event_results}"
            log_debug(msg=msg)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.INFO_REMOTE_PERSISTNACE_COMPLETE,subject="bigquery load_table_from_json",description=msg))
        else:
            limited_errors = job.errors[:max_job_errors_to_log]
            if len(job.errors) > max_job_errors_to_log:
                limited_errors.append({"message": f"and {len(job.errors) - max_job_errors_to_log} more errors..."})
            error_message = f"Errored Bigquery LoadJob {job.job_id} for {records_ref} for table {data_table_full_path}. Job Results: {event_results}. Errors: {limited_errors}"
            log_warning(msg=error_message, logger=logger)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_PERSISTANCE_WITH_ERRORS, subject="bigquery load_table_from_json",description=error_message))
    except Exception as e:
        event_results["event_exception"] = str(e)
        log_warning(msg=f"Exception occurred, Failed to execute event {event_results} for {records_ref}: {type(e).__name__} - {str(e)}", logger=logger)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))

    return event_results 




def query_existing_dates_for_object_from_timeseries_bigquery_table(
    project_id: str,
    data_table_full_path: str,
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    date_column: str,
    conditions: Dict[str, Any],
    start_value: Optional[Any] = None,
    end_value: Optional[Any] = None,
    bigquery_client: bigquery.Client = None,
    pipelinemon: Optional[Any] = None,
    logger: Optional[Any] = None
) -> Tuple[Dict[str, Any], Set[Any]]:
    """
    Queries existing records in BigQuery and returns a set of existing values from a specified column.

    Args:
        date_column (str): The column to check for existing records.
        conditions (Dict[str, Any]): Dictionary of fields and their corresponding values to check in the WHERE clause.

    Returns:
        Tuple[Dict[str, Any], Set[Any]]: A dictionary of event results and a set of existing values from the specified column.
    """

    # Ensure data is a list, even if a single record is passed
    if isinstance(data, dict):
        data = [data]

    event_results = {
        "event_operation_state": "NOT_STARTED",
        "event_details": "",
        "event_errors_count": 0,
        "event_exception": "",
    }

    # Infer the type of the column_to_check based on the data
    first_value = data[0][date_column]
    if isinstance(first_value, datetime.datetime):
        column_type = "TIMESTAMP"
    elif isinstance(first_value, datetime.date):
        column_type = "DATE"
    elif isinstance(first_value, str):
        try:
            # Try to parse as date, assume it's a date string if successful
            datetime.datetime.strptime(first_value, '%Y-%m-%d')
            column_type = "DATE"  # Treat string dates as STRING
        except ValueError:
            column_type = "STRING"  # It's just a regular string
    else:
        column_type = "STRING"  # Default to STRING for general use

    # Sort data based on column_to_check
    data = sorted(data, key=lambda x: x[date_column], reverse=True)
    recent_value = data[0][date_column]
    oldest_value = data[-1][date_column]

    try:
        # Build the WHERE clause dynamically
        where_clauses = []
        query_parameters = []

        for field, value in conditions.items():
            where_clauses.append(f"{field} = @{field}")
            param_type = "STRING" if isinstance(value, str) else "INTEGER"  # Adjust as needed
            query_parameters.append(bigquery.ScalarQueryParameter(field, param_type, value))

        # Handle the range filter based on start_value and end_value
        if start_value is not None and end_value is not None:
            where_clauses.append(f"{date_column} BETWEEN @start_value AND @end_value")
            query_parameters.extend([
                bigquery.ScalarQueryParameter("start_value", column_type, start_value),
                bigquery.ScalarQueryParameter("end_value", column_type, end_value),
            ])
        else:
            where_clauses.append(f"{date_column} BETWEEN @oldest_value AND @recent_value")
            query_parameters.extend([
                bigquery.ScalarQueryParameter("oldest_value", column_type, oldest_value),
                bigquery.ScalarQueryParameter("recent_value", column_type, recent_value),
            ])

        where_clause = " AND ".join(where_clauses)

        query = f"""
        SELECT {date_column} FROM `{data_table_full_path}`
        WHERE {where_clause}
        """
#### EXAMPLE
#  job_config = bigquery.QueryJobConfig(
#                   query_parameters=[bigquery.ScalarQueryParameter("object_id", "STRING", object_id),
                            #         bigquery.ScalarQueryParameter("records_recent_date", "DATE", sourced_records_recent_date),
                            #         bigquery.ScalarQueryParameter("records_oldest_date", "DATE", sourced_records_oldest_date))   
            
# query = f"""SELECT date_id FROM `{data_table_full_path}`
#              WHERE object_id = @object_id AND date_id BETWEEN @records_oldest_date AND @records_recent_date  """


        job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
        query_job = bigquery_client.query(query, job_config=job_config, project=project_id)
        event_results["event_operation_state"] = "QUERY_JOB_STARTED"
        results = query_job.result()
        event_results['event_operation_state'] = query_job.state
        event_results["event_errors_count"] = len(query_job.errors) if query_job.errors else 0
        event_results["event_details"]= json.dumps({"bigquery_job_id": query_job.job_id if query_job.job_id else "",
                                                    "total_bytes_billed": query_job.total_bytes_billed,  # Cost-relevant information
                                                    "total_bytes_processed": query_job.total_bytes_processed, # Data processed by the query
                                                    "user_email": query_job.user_email if query_job.user_email else "",
                                                    })
                                                    
        if query_job.state != 'DONE' or query_job.errors is not None:
            log_warning(msg=f"Failed to query existing records from BigQuery. Query Job State: {query_job.state}, Errors: {query_job.errors}", logger=logger)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_OPERATION_FAILED, subject="query_job", description="query_job.state != 'DONE' or query_job.errors is not None"))
            return event_results, set()

        # Keep received types as they are such as TIMESTAMP as datetime object but convert DATE to String
        if column_type == "DATE":
            existing_values = {row[date_column].strftime('%Y-%m-%d') for row in results}
        else:
            existing_values = {row[date_column] for row in results}

        log_debug(msg=f"Found {len(existing_values)} existing records.", logger=logger)
        return event_results, existing_values

    except Exception as e:
        log_warning(msg=f"Exception occurred during querying: {type(e).__name__} - {str(e)}", logger=logger)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))
        return event_results, set()
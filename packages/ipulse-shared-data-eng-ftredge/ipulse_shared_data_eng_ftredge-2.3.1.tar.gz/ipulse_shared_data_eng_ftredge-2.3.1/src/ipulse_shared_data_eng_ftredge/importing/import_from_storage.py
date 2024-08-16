# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=invalid-name

from typing import Dict, List
from ipulse_shared_base_ftredge import (LogLevel, DataSourceType, Frequency,
                                        log_warning, log_info, log_debug)

from ipulse_shared_data_eng_ftredge import (check_format_against_schema_template,
                                            read_json_from_cloud_storage_extended,
                                            ContextLog,
                                            Pipelinemon)



DATASET_FORMATTING_WARNINGS_AND_ERRORS_ALLOWED_DURING_CHECK=8
DATASET_WARNINGS_AND_ERRORS_TO_ALLOW_PERSISTANCE=0
METADATA_WARNINGS_AND_ERRORS_ALLOWED_TO_ALLOW_PERSISTANCE=0
def import_market_data_and_metadata_from_cloud_storage(
                                                       cloud_storage:DataSourceType,
                                                       storage_client,
                                                       file_name:str, source_bucket_name:str,
                                                       pipelinemon:Pipelinemon,
                                                       records_frequency:Frequency=None,
                                                       contains_metadata:bool=True,
                                                       data_schema:List[Dict]=None,
                                                       metadata_schema:List[Dict]=None,
                                                       logger=None):

    #####################################################################
    ##################### 1. IMPORT FILE CONTENT ########################
    try:
        with pipelinemon.context("importing_data"):
            try:
                json_data = read_json_from_cloud_storage_extended(cloud_storage=cloud_storage, storage_client=storage_client, file_name=file_name, bucket_name=source_bucket_name,logger=logger)
                if contains_metadata:
                    records_metadata = json_data.get('metadata')
                    records_json = json_data.get('data')
                    log_info( f'Successfully read file {file_name} from bucket {source_bucket_name}. Total {len(records_json)} records and metadata.', logger=logger)
                else:
                    log_info( f'Successfully read file {file_name} from bucket {source_bucket_name}. Total {len(json_data)} records.',logger=logger)
                    return json_data
            except Exception as e:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))
                log_warning(f"Exception when reading file {file_name}: {type(e).__name__} - {str(e)}", logger=logger)
                return None

        ################################################################
        ##################### 2. PERFORM CHECKS WITH METADATA ########################
        if data_schema:
            with pipelinemon.context("checking_dataset_schema_format"):
                try:
                    for record in records_json:
                        _, warnings_or_error = check_format_against_schema_template(schema=data_schema, data_to_check=record)
                        if warnings_or_error and len(warnings_or_error)>0:
                            pipelinemon.add_logs(warnings_or_error)
                            # Early stopping if warnings/errors exceed max allowed. Better to allow until max allowed, to get a better picture of dataset
                            if pipelinemon.count_warnings_and_errors_for_current_context()>DATASET_FORMATTING_WARNINGS_AND_ERRORS_ALLOWED_DURING_CHECK:
                                log_warning(f" Early_Stopping schema check, as nb of warnings/errors already exceeds max allowed : {DATASET_FORMATTING_WARNINGS_AND_ERRORS_ALLOWED_DURING_CHECK}.", logger=logger)
                                break
                    if pipelinemon.count_warnings_and_errors_for_current_context()>DATASET_WARNINGS_AND_ERRORS_TO_ALLOW_PERSISTANCE: # Still don't proceed if at leastr 1 warning is identified
                        msg=f"Data checked against Schema. With total Warnings+Errors/[to allow persistance ; allowed during dataset check]  : {pipelinemon.count_warnings_and_errors_for_current_and_nested_contexts()}/[{DATASET_WARNINGS_AND_ERRORS_TO_ALLOW_PERSISTANCE}; {DATASET_FORMATTING_WARNINGS_AND_ERRORS_ALLOWED_DURING_CHECK}]"
                        pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_DATA_QUALITY_THRESHOLD_REACHED,
                                        subject="sourced_data_preprocessed",
                                        description=msg))
                        log_debug(msg, logger=logger)
                        return None
                except Exception as e:
                    log_warning(f"ERROR: Exception occured in {pipelinemon.current_context} : {type(e).__name__} - {str(e)}", logger=logger)
                    pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))
                    return None

        if contains_metadata: 
            if metadata_schema: 
                with pipelinemon.context("checking_metadata_schema_format"):
                    try:
                        _, metadata_warnings_or_error = check_format_against_schema_template(schema=metadata_schema, data_to_check=records_metadata)
                        if metadata_warnings_or_error and len(metadata_warnings_or_error)>0:
                            pipelinemon.add_logs(metadata_warnings_or_error)
                            if len(metadata_warnings_or_error)>METADATA_WARNINGS_AND_ERRORS_ALLOWED_TO_ALLOW_PERSISTANCE:
                                log_warning(f"Early_Stopping. Metadata checked against Schema. With total Warnings/Errors: {len(metadata_warnings_or_error)}", logger=logger)
                                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_METADATA_QUALITY_THRESHOLD_REACHED,
                                                subject="sourcing_metadata",
                                                description=f"Metadata Schema Check finished with with Errors/Warnings : {len(metadata_warnings_or_error)}"))
                                return None
                        log_debug(msg="Metadata checked against Schema with 0  Warnings/Errors. ", logger=logger)
                    except Exception as e:
                        log_warning(f"ERROR: Exception occured in {pipelinemon.current_context} : {type(e).__name__} - {str(e)}", logger=logger)
                        pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))
                        return None

            with pipelinemon.context("consistency_checks"):
                if records_frequency:
                    frequency=records_metadata.get('sourced_records_frequency')
                    if records_frequency.value!=frequency:
                        log_warning(f"Didn't porcess file: {file_name}, {frequency} not acceptable RECORDS_FREQUENCY={records_frequency}", logger=logger)
                        pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_CUSTOM, subject="sourced_records_frequency", description=f"frequency mismatch. Expected {records_frequency}, found {frequency}"))
                        return None
        return json_data

            ############### SETTING SOME PARAMETERS #####################
    except Exception as e:
        log_warning(f"Exception when perfoming checks for file {file_name}: {type(e).__name__} - {str(e)}", logger=logger)
        pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))
        return None
    
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
import json
import uuid
from datetime import datetime, timezone
from contextlib import contextmanager
from typing import List
from ipulse_shared_base_ftredge import LogLevel
from .context_log import  ContextLog
############################################################################
##### PIPINEMON Collector for Logs and Statuses of running pipelines #######
class Pipelinemon:
    ERROR_START_CODE = LogLevel.ERROR.value
    WARNING_START_CODE = LogLevel.WARNING.value
    NOTICE_START_CODE = LogLevel.NOTICE.value
    SUCCESS_START_CODE = LogLevel.SUCCESS.value
    INFO_START_CODE = LogLevel.INFO.value

    def __init__(self,  base_context: str, execution_domain:str, logger,
                 max_log_field_size:int =10000,
                 max_log_dict_size:float=256 * 1024 * 0.80,
                 max_log_traceback_lines:int = 30):

        self._id = str(uuid.uuid4())
        self._logs = []
        self._early_stop = False
        self._errors_count = 0
        self._warnings_count = 0
        self._notices_count = 0
        self._successes_count = 0
        self._infos_count = 0
        self._systems_impacted = []
        self._by_level_counts = {level.name: 0 for level in LogLevel}
        self._execution_domain = execution_domain
        self._base_context = base_context
        self._context_stack = []
        self._logger = logger
        self._max_log_field_size = max_log_field_size
        self._max_log_dict_size = max_log_dict_size
        self._max_log_traceback_lines = max_log_traceback_lines


    @contextmanager
    def context(self, context):
        self.push_context(context)
        try:
            yield
        finally:
            self.pop_context()

    def push_context(self, context):
        self._context_stack.append(context)

    def pop_context(self):
        if self._context_stack:
            self._context_stack.pop()

    @property
    def current_context(self):
        return " >> ".join(self._context_stack)

    @property
    def base_context(self):
        return self._base_context
    
    @base_context.setter
    def base_context(self, value):
        self._base_context = value

    @property
    def execution_domain(self):
        return self._execution_domain
    
    @execution_domain.setter
    def execution_domain(self, value):
        self._execution_domain = value

    @property
    def id(self):
        return self._id

    @property
    def systems_impacted(self):
        return self._systems_impacted

    @systems_impacted.setter
    def systems_impacted(self, list_of_si: List[str]):
        self._systems_impacted = list_of_si

    def add_system_impacted(self, system_impacted: str):
        if self._systems_impacted is None:
            self._systems_impacted = []
        self._systems_impacted.append(system_impacted)

    def clear_systems_impacted(self):
        self._systems_impacted = []

    @property
    def max_log_dict_size(self):
        return self._max_log_dict_size

    @max_log_dict_size.setter
    def max_log_dict_size(self, value):
        self._max_log_dict_size = value

    @property
    def max_log_field_size(self):
        return self._max_log_field_size

    @max_log_field_size.setter
    def max_log_field_size(self, value):
        self._max_log_field_size = value

    @property
    def max_log_traceback_lines(self):
        return self._max_log_traceback_lines

    @max_log_traceback_lines.setter
    def max_log_traceback_lines(self, value):
        self._max_log_traceback_lines = value

    @property
    def early_stop(self):
        return self._early_stop

    def set_early_stop(self, max_errors_tolerance:int=0, max_warnings_tolerance:int=0, create_error_log=True, pop_context=False):
        self._early_stop = True
        if create_error_log:
            if pop_context:
                self.pop_context()
            if max_errors_tolerance > 0:
                self.add_log(ContextLog(level=LogLevel.ERROR_PIPELINE_THRESHOLD_REACHED,
                                        subject="EARLY_STOP",
                                        description=f"Total MAX_ERRORS_TOLERANCE of {max_errors_tolerance} has been reached."))
            elif max_warnings_tolerance > 0:
                self.add_log(ContextLog(level=LogLevel.ERROR_PIPELINE_THRESHOLD_REACHED,
                                        subject="EARLY_STOP",
                                        description=f"Total MAX_WARNINGS_TOLERANCE of {max_warnings_tolerance} has been reached."))
            else:
                self.add_log(ContextLog(level=LogLevel.ERROR_PIPELINE_THRESHOLD_REACHED,
                                        subject="EARLY_STOP",
                                        description="Early stop has been triggered."))

    def reset_early_stop(self):
        self._early_stop = False


    def add_log(self, log: ContextLog ):
        log.base_context = self.base_context
        log.execution_domain = self.execution_domain
        log.context = self.current_context if self.current_context else "root"
        log.collector_id = self.id
        log.systems_impacted = self.systems_impacted
        log_dict = log.to_dict(max_field_len=self.max_log_field_size, size_limit=self.max_log_dict_size, max_traceback_lines=self.max_log_traceback_lines)
        self._logs.append(log_dict)
        self._update_counts(log_dict)

        if self._logger:
            # We specifically want to avoid having an ERROR log level for this structured Pipelinemon reporting, to ensure Errors are alerting on Critical Application Services.
            # A single ERROR log level is usually added at the end of the entire pipeline
            if log.level.value >= self.WARNING_START_CODE:
                self._logger.warning(log_dict)
            else:
                self._logger.info(log_dict)

    def add_logs(self, logs: List[ContextLog]):
        for log in logs:
            self.add_log(log)

    def clear_logs_and_counts(self):
        self._logs = []
        self._errors_count = 0
        self._warnings_count = 0
        self._notices_count = 0
        self._successes_count = 0
        self._infos_count = 0
        self._by_level_counts = {level.name: 0 for level in LogLevel}

    def clear_logs(self):
        self._logs = []

    def get_all_logs(self,in_json_format=False):
        if in_json_format:
            return json.dumps(self._logs)
        return self._logs

    def get_logs_for_level(self, level: LogLevel):
        return [log for log in self._logs if log["level_code"] == level.value]

    def get_logs_by_str_in_context(self, context_substring: str):
        return [
            log for log in self._logs
            if context_substring in log["context"]
        ]

    def contains_errors(self):
        return self._errors_count > 0

    def count_errors(self):
        return self._errors_count

    def contains_warnings_or_errors(self):
        return self._warnings_count > 0 or self._errors_count > 0

    def count_warnings_and_errors(self):
        return self._warnings_count + self._errors_count

    def count_warnings(self):
        return self._warnings_count

    def count_notices(self):
        return self._notices_count

    def count_successes(self):
        return self._successes_count

    def count_successes_with_notice(self):
        return self.count_logs_by_level(LogLevel.SUCCESS_WITH_NOTICES)

    def count_successes_no_notice(self):
        return self.count_logs_by_level(LogLevel.SUCCESS)

    def count_infos(self):
        return self._infos_count

    def count_all_logs(self):
        return len(self._logs)

    def count_logs_by_level(self, level: LogLevel):
        return self._by_level_counts.get(level.name, 0)

    def _count_logs(self, context_substring: str, exact_match=False, level_code_min=None, level_code_max=None):
        return sum(
            1 for log in self._logs
            if (log["context"] == context_substring if exact_match else context_substring in log["context"]) and
               (level_code_min is None or log["level_code"] >= level_code_min) and
               (level_code_max is None or log["level_code"] <= level_code_max)
        )

    def count_logs_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True)

    def count_logs_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context)

    def count_logs_by_level_for_current_context(self, level: LogLevel):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=level.value, level_code_max=level.value)

    def count_logs_by_level_for_current_and_nested_contexts(self, level: LogLevel):
        return self._count_logs(self.current_context, level_code_min=level.value, level_code_max=level.value)

    def count_errors_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=self.ERROR_START_CODE)

    def count_errors_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context, level_code_min=self.ERROR_START_CODE)

    def count_warnings_and_errors_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=self.WARNING_START_CODE)

    def count_warnings_and_errors_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context, level_code_min=self.WARNING_START_CODE)

    def count_warnings_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=self.WARNING_START_CODE, level_code_max=self.ERROR_START_CODE - 1)

    def count_warnings_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context, level_code_min=self.WARNING_START_CODE, level_code_max=self.ERROR_START_CODE - 1)

    def count_notices_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=self.NOTICE_START_CODE, level_code_max=self.WARNING_START_CODE-1)

    def count_notices_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context, level_code_min=self.NOTICE_START_CODE, level_code_max=self.WARNING_START_CODE-1)

    def count_successes_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=self.SUCCESS_START_CODE, level_code_max=self.NOTICE_START_CODE-1)

    def count_successes_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context, level_code_min=self.SUCCESS_START_CODE, level_code_max=self.NOTICE_START_CODE-1)

    def count_infos_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=self.INFO_START_CODE, level_code_max=self.SUCCESS_START_CODE-1)

    def count_infos_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context, level_code_min=self.INFO_START_CODE, level_code_max=self.SUCCESS_START_CODE-1)
    
    def _update_counts(self, log, remove=False):
        level_code = log["level_code"]
        level_name = log["level_name"]

        if remove:
            if level_code >= self.ERROR_START_CODE:
                self._errors_count -= 1
            elif self.WARNING_START_CODE <= level_code < self.ERROR_START_CODE:
                self._warnings_count -= 1
            elif self.NOTICE_START_CODE <= level_code < self.WARNING_START_CODE:
                self._notices_count -= 1
            elif self.SUCCESS_START_CODE <= level_code < self.NOTICE_START_CODE:
                self._successes_count -= 1
            elif self.INFO_START_CODE <= level_code < self.SUCCESS_START_CODE:
                self._infos_count -= 1
            self._by_level_counts[level_name] -= 1
        else:
            if level_code >= self.ERROR_START_CODE:
                self._errors_count += 1
            elif self.WARNING_START_CODE <= level_code < self.ERROR_START_CODE:
                self._warnings_count += 1
            elif self.NOTICE_START_CODE <= level_code < self.WARNING_START_CODE:
                self._notices_count += 1
            elif self.SUCCESS_START_CODE <= level_code < self.NOTICE_START_CODE:
                self._successes_count += 1
            elif self.INFO_START_CODE <= level_code < self.SUCCESS_START_CODE:
                self._infos_count += 1
            self._by_level_counts[level_name] += 1

    def generate_file_name(self, file_prefix=None, include_base_context=True):
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        if not file_prefix:
            file_prefix = "pipelinelogs"
        if include_base_context:
            file_name = f"{file_prefix}_{timestamp}_{self.base_context}_len{len(self._logs)}.json"
        else:
            file_name = f"{file_prefix}_{timestamp}_len{len(self._logs)}.json"

        return file_name

    def import_logs_from_json(self, json_or_file, logger=None):
        def log_message(message):
            if logger:
                logger.info(message)

        def log_warning(message, exc_info=False):
            if logger:
                logger.warning(message, exc_info=exc_info)

        try:
            if isinstance(json_or_file, str):  # Load from string
                imported_logs = json.loads(json_or_file)
            elif hasattr(json_or_file, 'read'):  # Load from file-like object
                imported_logs = json.load(json_or_file)
            self.add_logs(imported_logs)
            log_message("Successfully imported logs from json.")
        except Exception as e:
            log_warning(f"Failed to import logs from json: {type(e).__name__} - {str(e)}", exc_info=True)


    def generate_final_log_message(self, subjectref: str, total_subjs: int) -> str:
        return f"""
            Pipeline for {self.base_context} with pipelinemon.id: {self.id},
            SUMMARY: Early_Stop= {self.early_stop} ;
            A)SUCCESSES: {self.count_successes()}/{total_subjs} {subjectref}(s) ; out of which SUCCESSES_WITH_NOTICES: {self.count_successes_with_notice()}/{total_subjs} {subjectref}(s) ;
            B)NOTICES: {self.count_notices()} ;
            C)WARNINGS: {self.count_warnings()} ;
            D)ERRORS: {self.count_errors()} ;
            E)INFOS: {self.count_infos()} ;
        """

    def log_final_message(self, subjectref: str, total_subjs: int, generallogger):
        final_log_message = self.generate_final_log_message(subjectref=subjectref, total_subjs=total_subjs)
        if self.count_warnings_and_errors() > 0:
            generallogger.error(final_log_message)
        else:
            generallogger.info(final_log_message)

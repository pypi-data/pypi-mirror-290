from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from functools import partial
from logging import Logger
from math import isnan
from typing import Any

from ngs_pipeline_lib.tools.tools import to_camel_case


class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class ExecutionReport:
    start: datetime
    stop: datetime | None = None
    status: ExecutionStatus = ExecutionStatus.SUCCESS
    duration: int = field(init=False)

    @property
    def duration(self) -> int:
        if not self.stop:
            return 0
        else:
            delta = self.stop - self.start
            return int(delta.total_seconds() * 1000)

    @duration.setter
    def duration(self, value: int) -> None:
        """
        This setter does nothing as duration must be calculated
        """

    def to_logger(self, logger: Logger) -> None:
        if self.status == ExecutionStatus.SUCCESS:
            log_status = logger.info
        else:
            log_status = partial(logger.exception, exc_info=False)
        log_status(f"Execution status: {self.status.value}")


@dataclass
class Report:
    name: str
    version: str
    inputs: dict[str, Any]
    kbs: dict[str, Any]
    outputs: list[str]
    execution: ExecutionReport | None = None


class QCResult(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    NA = "NA"


@dataclass
class QCReportIssue:
    sectionName: str
    organismName: str
    name: str
    status: QCResult
    rules: list[dict[str, Any]]
    description: str


@dataclass
class QCReport:
    result: QCResult = QCResult.PASS
    metrics: dict[str, str | int | float | bool | None] = field(default_factory=dict)
    issues: list[QCReportIssue] = field(default_factory=list)

    def add_metrics(self, metrics: dict[str, str | int | float | bool]):
        for name, value in metrics.items():
            self.add_metric(metric_name=name, metric_value=value)

    def add_metric(self, metric_name: str, metric_value: str | int | float | bool):
        formatted_metric_name = to_camel_case(metric_name)

        if formatted_metric_name in self.metrics:
            raise ValueError(
                f"The metric {formatted_metric_name} is already set in the report metrics with the value {self.metrics[formatted_metric_name]}."
            )

        try:
            if isnan(metric_value):
                metric_value = None
        except TypeError:
            ...
        self.metrics[formatted_metric_name] = metric_value

    def to_logger(self, logger: Logger) -> None:
        log_result = {
            QCResult.PASS: logger.info,
            QCResult.WARN: logger.warning,
            QCResult.FAIL: partial(logger.exception, exc_info=False),
        }
        if self.result not in log_result:
            # not need to log "NA"
            return

        log_result[self.result](f"QC result: {self.result.value}")
        for issue in self.issues:
            log_result[issue.status](
                f"QC {issue.status.value} {issue.name}: {issue.description}"
            )

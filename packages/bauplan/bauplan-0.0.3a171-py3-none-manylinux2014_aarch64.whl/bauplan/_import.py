import os
from io import StringIO
from pathlib import Path
from typing import Dict, Optional

import grpc
import yaml  # type: ignore

from . import exceptions
from ._common import _OperationContainer, _print_debug
from ._protobufs.bauplan_pb2 import (
    JobId,
    RunnerInfo,
)
from .bpln_proto.commander.service.v2.service_pb2 import (
    ApplyImportPlanRequest,
    ApplyImportPlanResponse,
    CreateImportPlanRequest,
    CreateImportPlanResponse,
)
from .state import ApplyPlanState, PlanImportState

JOB_STATUS_FAILED = 'FAILED'
JOB_STATUS_SUCCESS = 'SUCCESS'
JOB_STATUS_CANCELLED = 'CANCELLED'


def _validate_plan_yaml(plan_yaml: str) -> None:
    if not isinstance(plan_yaml, str):
        raise exceptions.InvalidPlanError('invalid plan YAML; plan YAML string is required')
    if not plan_yaml or plan_yaml.strip() == '':
        raise exceptions.InvalidPlanError('invalid plan YAML; plan YAML string is required')

    try:
        yaml.safe_load(StringIO(plan_yaml))
    except yaml.YAMLError as e:
        raise e


def _handle_apply_import_log(log: RunnerInfo, state: ApplyPlanState) -> bool:
    if log.runner_event.apply_plan_done.error_message:
        state.error = log.runner_event.apply_plan_done.error_message
        state.job_status = JOB_STATUS_FAILED
        _print_debug(f'Apply plan failed, error is: {state.error}')
        return True
    if log.runner_event.apply_plan_done.success:
        state.job_status = JOB_STATUS_SUCCESS
        _print_debug('Apply plan successful')
        return True
    return False


def _handle_plan_import_log(log: RunnerInfo, state: PlanImportState) -> bool:
    if log.runner_event.import_plan_created.error_message:
        state.error = log.runner_event.import_plan_created.error_message
        state.job_status = JOB_STATUS_FAILED
        _print_debug(f'Create import plan failed, error is: {state.error}')
        return True
    if log.runner_event.import_plan_created.success:
        state.job_status = JOB_STATUS_SUCCESS
        state.plan_yaml = log.runner_event.import_plan_created.plan_as_yaml
        _print_debug('Create import plan success')
        return True
    return False


class _Import(_OperationContainer):
    def plan(
        self,
        search_string: str,
        table: str,
        branch: str,
        args: Optional[Dict[str, str]] = None,
        output_file: str = 'bauplan_import_plan.yaml',
        append: bool = False,
        replace: bool = False,
        no_cache: bool = False,
        timeout: int = 60,
    ) -> PlanImportState:
        """
        Create a table import plan from an S3 location.
        This is the equivalent of running through the CLI the ``bauplan import plan`` command.
        """
        if not isinstance(search_string, str) or not search_string.strip():
            raise ValueError('search_string is required')
        if not search_string.startswith('s3://'):
            raise ValueError('search_string must be an S3 path, e.g., s3://bucket-name/*.parquet')
        if not isinstance(table, str) or not table.strip():
            raise ValueError('table is required')
        if not isinstance(branch, str) or not branch.strip():
            raise ValueError('branch is required')

        client_v1, metadata_v1 = self._common.get_commander_and_metadata(args)
        client_v2, metadata_v2 = self._common.get_commander_v2_and_metadata(args)

        _print_debug(
            'Create import plan',
            'search_string',
            search_string,
            'output_file',
            output_file,
            'branch',
            branch,
            'table',
            table,
            'append',
            append,
            'replace',
            replace,
            'no_cache',
            no_cache,
            'timeout',
            timeout,
        )

        response: CreateImportPlanResponse = client_v2.CreateImportPlan(
            CreateImportPlanRequest(
                search_string=search_string,
                trigger_run_opts={'cache': not no_cache},
                args=args or {},
                branch=branch,
                table=table,
                append=append,
                replace=replace,
            ),
            metadata=metadata_v2,
        )
        job_id = JobId(id=response.job_id)
        _print_debug('Create import plan job_id', response.job_id)

        log_stream: grpc.Call = client_v1.SubscribeLogs(job_id, metadata=metadata_v1)
        state = PlanImportState(job_id=job_id.id)

        for log in log_stream:
            if _handle_plan_import_log(log, state):
                break

        if state.plan_yaml:
            Path(output_file).write_text(state.plan_yaml)

        return state

    def apply(
        self,
        plan_file: str,
        branch: str,
        args: Optional[Dict[str, str]] = None,
        merge: bool = False,
        no_cache: bool = False,
        timeout: int = 300,
    ) -> ApplyPlanState:
        """
        Apply a Bauplan table import plan for a given branch.
        This is the equivalent of running through the CLI the ``bauplan import apply`` command.
        """
        if not os.path.exists(plan_file):
            raise ValueError(f"Plan file '{plan_file}' does not exist")
        if not isinstance(branch, str) or not branch.strip():
            raise ValueError("branch is required, e.g. 'myname.mybranch'")

        plan_yaml = Path(plan_file).read_text()

        _validate_plan_yaml(plan_yaml)

        client_v1, metadata_v1 = self._common.get_commander_and_metadata(args)
        client_v2, metadata_v2 = self._common.get_commander_v2_and_metadata(args)

        _print_debug(
            'Apply import plan',
            'plan_file',
            plan_file,
            'branch',
            branch,
            'merge',
            merge,
            'no_cache',
            no_cache,
            'timeout',
            timeout,
        )

        response: ApplyImportPlanResponse = client_v2.ApplyImportPlan(
            ApplyImportPlanRequest(
                plan_yaml=plan_yaml,
                trigger_run_opts={'cache': not no_cache},
                args=args or {},
                write_branch=branch,
                merge=merge,
            ),
            metadata=metadata_v2,
        )

        job_id = JobId(id=response.job_id)
        _print_debug('Apply import plan job_id', response.job_id)

        log_stream: grpc.Call = client_v1.SubscribeLogs(
            job_id,
            metadata=metadata_v1,
        )
        state = ApplyPlanState(job_id=job_id.id)

        for log in log_stream:
            if _handle_apply_import_log(log, state):
                break

        return state

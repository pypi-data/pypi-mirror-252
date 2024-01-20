from typing import Optional
from ..repositories.project.project import JobStage
from .execution import Execution, RequestData
from ..repositories.execution_logs import ExecutionLogsRepository
from ..repositories.execution import ExecutionRepository
from ..repositories.stage_run import StageRunRepository


class JobExecution(Execution):
    def __init__(
        self,
        stage: JobStage,
        stage_run_repository: StageRunRepository,
        execution_repository: ExecutionRepository,
        execution_logs_repository: ExecutionLogsRepository,
    ):
        request = RequestData(
            headers={},
            body="",
            method="GET",
            query_params={},
        )

        super().__init__(
            stage=stage,
            is_initial=True,
            request=request,
            execution_repository=execution_repository,
            execution_logs_repository=execution_logs_repository,
            stage_run_repository=stage_run_repository,
        )

    def handle_start(self) -> None:
        pass

    def handle_success(self) -> None:
        pass

    def handle_failure(self, e: Exception) -> None:
        pass

    def handle_lock_failed(self) -> None:
        pass

    def received_stage_run_id(self) -> Optional[str]:
        return None

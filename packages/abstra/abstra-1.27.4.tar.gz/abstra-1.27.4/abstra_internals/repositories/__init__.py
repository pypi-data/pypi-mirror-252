from .connectors import connectors_api_http_client_factory
from .stage_run import stage_run_repository_factory
from .tables import tables_api_http_client_factory
from .execution import execution_repository_factory
from .execution_logs import execution_logs_repository_factory

connectors_api_http_client = connectors_api_http_client_factory()
tables_api_http_client = tables_api_http_client_factory()
stage_run_repository = stage_run_repository_factory()
execution_repository = execution_repository_factory()
execution_logs_repository = execution_logs_repository_factory()

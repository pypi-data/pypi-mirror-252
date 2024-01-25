from cirro_api_client.api.billing_api import BillingApi
from cirro_api_client.api.dashboards_api import DashboardsApi
from cirro_api_client.api.datasets_api import DatasetsApi
from cirro_api_client.api.execution_api import ExecutionApi
from cirro_api_client.api.file_api import FileApi
from cirro_api_client.api.metadata_api import MetadataApi
from cirro_api_client.api.metrics_api import MetricsApi
from cirro_api_client.api.notebooks_api import NotebooksApi
from cirro_api_client.api.processes_api import ProcessesApi
from cirro_api_client.api.projects_api import ProjectsApi
from cirro_api_client.api.references_api import ReferencesApi
from cirro_api_client.api.system_api import SystemApi
from cirro_api_client.api.users_api import UsersApi
from cirro_api_client.api_client import ApiClient
from cirro_api_client.configuration import Configuration


class CirroApiClient:
    """
    A client for interacting with the Cirro platform
    """
    def __init__(self,
                 configuration: Configuration):
        self._api_client = ApiClient(configuration=configuration)

        self.projects = ProjectsApi(self._api_client)
        self.billing = BillingApi(self._api_client)
        self.dashboards = DashboardsApi(self._api_client)
        self.datasets = DatasetsApi(self._api_client)
        self.execution = ExecutionApi(self._api_client)
        self.file = FileApi(self._api_client)
        self.metadata = MetadataApi(self._api_client)
        self.metrics = MetricsApi(self._api_client)
        self.notebooks = NotebooksApi(self._api_client)
        self.processes = ProcessesApi(self._api_client)
        self.projects = ProjectsApi(self._api_client)
        self.references = ReferencesApi(self._api_client)
        self.system = SystemApi(self._api_client)
        self.users = UsersApi(self._api_client)

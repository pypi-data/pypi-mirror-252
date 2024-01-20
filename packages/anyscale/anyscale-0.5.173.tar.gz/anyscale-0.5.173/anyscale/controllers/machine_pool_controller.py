from typing import Optional

from rich.console import Console

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    CreateMachinePoolRequest,
    CreateMachinePoolResponse,
    DeleteMachinePoolRequest,
    ListMachinePoolsResponse,
)
from anyscale.controllers.base_controller import BaseController


class MachinePoolController(BaseController):
    def __init__(
        self, log: Optional[BlockLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log
        self.console = Console()

    def create_machine_pool(self, machine_pool_name: str,) -> CreateMachinePoolResponse:
        response: CreateMachinePoolResponse = self.api_client.create_machine_pool_api_v2_machine_pools_create_post(
            CreateMachinePoolRequest(machine_pool_name=machine_pool_name)
        ).result
        return response

    def delete_machine_pool(
        self, machine_pool_name: str,
    ):
        self.api_client.delete_machine_pool_api_v2_machine_pools_delete_post(
            DeleteMachinePoolRequest(machine_pool_name=machine_pool_name)
        )

    def list_machine_pools(self,) -> ListMachinePoolsResponse:
        response = self.api_client.list_machine_pools_api_v2_machine_pools_get().result
        return response

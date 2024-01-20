from unittest.mock import Mock

from anyscale.client.openapi_client.models import (
    CreateMachinePoolResponse,
    DeleteMachinePoolRequest,
    ListMachinePoolsResponse,
    MachinePool,
)
from frontend.cli.anyscale.controllers.machine_pool_controller import (
    MachinePoolController,
)


def test_create_machine_pool(mock_auth_api_client) -> None:
    response = CreateMachinePoolResponse(
        machine_pool=MachinePool(
            machine_pool_name="pool1",
            machine_pool_id="mp-123",
            organization_id="org-123",
            cloud_ids=[],
        )
    )
    api_response = Mock()
    api_response.result = response

    machine_pool_controller = MachinePoolController()
    machine_pool_controller.api_client.create_machine_pool_api_v2_machine_pools_create_post = Mock(
        return_value=api_response
    )
    output = machine_pool_controller.create_machine_pool(machine_pool_name="pool1")
    assert output == response


def test_delete_machine_pool(mock_auth_api_client) -> None:
    api_response = Mock()
    api_response.result = ""

    machine_pool_controller = MachinePoolController()
    machine_pool_controller.api_client.delete_machine_pool_api_v2_machine_pools_delete_post = Mock(
        return_value=api_response
    )
    machine_pool_controller.delete_machine_pool(machine_pool_name="pool1")
    machine_pool_controller.api_client.delete_machine_pool_api_v2_machine_pools_delete_post.assert_called_once_with(
        DeleteMachinePoolRequest(machine_pool_name="pool1")
    )


def test_list_machine_pool(mock_auth_api_client) -> None:
    response = ListMachinePoolsResponse(
        machine_pools=[
            MachinePool(
                machine_pool_name="pool1",
                machine_pool_id="mp-123",
                organization_id="org-123",
                cloud_ids=[],
            )
        ]
    )

    api_response = Mock()
    api_response.result = response

    machine_pool_controller = MachinePoolController()
    machine_pool_controller.api_client.list_machine_pools_api_v2_machine_pools_get = Mock(
        return_value=api_response
    )
    output = machine_pool_controller.list_machine_pools()
    assert output == response

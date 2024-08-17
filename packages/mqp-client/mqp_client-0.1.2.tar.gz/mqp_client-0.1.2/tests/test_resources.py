from mqp.client import MQPClient
from mqp.client.resource_info import ResourceInfo

from .config import URL, TOKEN, CURRENT_RESOURCES


def test_get_specific_resource():
    client = MQPClient(url=URL, token=TOKEN)
    resource_names = CURRENT_RESOURCES.keys()
    for name in resource_names:
        info = client.resource_info(name)
        assert info == CURRENT_RESOURCES[name]


def test_get_all_resources():
    client = MQPClient(url=URL, token=TOKEN)
    resources = client.resources()
    assert resources == CURRENT_RESOURCES


def test_get_non_existing_resource():
    client = MQPClient(url=URL, token=TOKEN)
    try:
        client.resource_info("non_existing")
        assert False
    except Exception as e:
        assert True

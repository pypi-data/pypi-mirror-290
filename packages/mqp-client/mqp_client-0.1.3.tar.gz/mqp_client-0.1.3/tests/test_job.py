from mqp.client import MQPClient, JobStatus

from .config import URL, TOKEN, CURRENT_RESOURCES, get_qasm


def test_job():
    client = MQPClient(url=URL, token=TOKEN)
    some_resource_name = list(CURRENT_RESOURCES.keys())[0]
    uuid = client.submit_job(some_resource_name, get_qasm(), 1000)
    assert client.status(uuid) == JobStatus.PENDING
    assert client.result(uuid) is None
    client.cancel(uuid)
    assert client.status(uuid) == JobStatus.CANCELLED

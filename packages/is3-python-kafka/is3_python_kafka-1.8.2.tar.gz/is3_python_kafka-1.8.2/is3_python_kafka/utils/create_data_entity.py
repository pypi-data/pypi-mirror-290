import json

from is3_python_kafka.domain.data_dto import DataEntity
from is3_python_kafka.utils.config_util import get_header
from is3_python_kafka.utils.config_util import get_server_name


def create_data_entity(filePath, jsonData):
    serverName = get_server_name(filePath, 'server')
    headers = get_header(filePath, 'key')
    dataDto = DataEntity(
        preData=jsonData['data'],
        pluginDataConfig=json.dumps(jsonData['pluginDataConfig']),
        taskInstanceId=1111,
        taskId=1,
        nodeId=1,
        logId=1,
        serverName=serverName,
        headers=headers,
        prjId=1744555702386843650,
        tenantId=1,
        bootstrapServers='1',
    )
    return dataDto

import logging
import os

import requests
from is3_python_sync_plugin.utils import Logging

from is3_python_kafka.domain import DataEntity

Logging()


def upload_file(filePath, dataDto: DataEntity):
    file_name = os.path.basename(filePath)
    headers = dataDto.headers
    headers['Content-Type'] = 'multipart/form-data'
    print(headers)
    with open(filePath, 'rb') as file:
        # 构建 files 字典
        files = {'file': (file_name, file)}

        try:
            response = requests.post("http://129.211.174.77:31991/iS3Server/is3-modules-file/inner/upload",
                                     file, headers)
            if response.status_code != 200:
                logging.info('接口调用失败，状态码：', response.status_code)
            return response.json()
        except requests.RequestException as e:
            logging.error(f'请求失败：{e}')
            return None

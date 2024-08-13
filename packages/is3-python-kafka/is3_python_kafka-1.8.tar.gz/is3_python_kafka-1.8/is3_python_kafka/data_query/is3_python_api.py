import logging
import mimetypes
from urllib.parse import urlparse

import requests

from is3_python_kafka.utils import Logging, get_header, get_property
from is3_python_kafka.utils.is3_request_util import RequestUtil

Logging()


class iS3PythonApi:
    def __init__(self, configPath, prjId):
        self.configPath = configPath,
        self.prjId = prjId
        self.headers = get_header(configPath, 'key')
        self.server_url = get_property(configPath, 'is3', 'is3-addr')

    '''根据自定义编码查询任务流编码'''

    def getProcessCode(self, customCode):

        url = f'{self.server_url}/is3-modules-open/scheduling/process-definition-code/custom?customCode={customCode}'
        try:
            response = RequestUtil.get(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''获取metatable列表数据'''

    def getMetaTableList(self, json):
        url = f'{self.server_url}/data-main/operation/getDataByCondition'
        json['prjId'] = self.prjId
        return RequestUtil.post(url, json, self.headers)

    '''文件上传'''

    def uploadFile(self, filePath):
        content_type, _ = mimetypes.guess_type(filePath)
        content_type = content_type or 'application/octet-stream'
        file_name = filePath.split('\\')[-1]
        files = {'file': (file_name, open(filePath, 'rb'), content_type)}
        self.headers.pop('Content-Type', None)
        url = f'{self.server_url}/is3-modules-file/inner/upload'

        try:
            response = RequestUtil.post_with_file(url=url, headers=self.headers, files=files)  # 检查请求是否成功
            if response['code'] == 200:
                logging.info('文件上传成功')
                return response  # 返回响应的 JSON 数据
            else:
                logging.error('文件上传失败，状态码：' + str(response['code']))
                return None
        except requests.RequestException as e:
            logging.error(f'请求过程中发生异常: {e}')
            return None

    '''文件下载'''

    def downloadFile(self, localPath, url):
        # url = "http://43.137.38.138:19000/is3/2024/08/12/GPR892侧线1_89657b87b8734f988e4fc189a174cf5d.png"
        parsed_url = urlparse(url)
        path = parsed_url.path
        path_parts = path.split('/')
        path = '/'.join(path_parts[2:])
        url = f'{self.server_url}/is3-modules-file/inner/download/?localFilePath={localPath}&filePath={path}'
        try:
            response = RequestUtil.post(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''获取对象组列表'''

    def getObjectList(self):
        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsList?prjId={self.prjId}'
        try:
            response = RequestUtil.get(url=url, headers=headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''获取对象组的对象实例列表'''

    def getObjsInstanceList(self, objsCode):

        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsInstanceList/{objsCode}?prjId={self.prjId}'
        try:
            response = RequestUtil.get(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''获取列表'''

    def getObjsSubTypeList(self, objsCode):

        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsSubTypeList/{objsCode}?prjId={self.prjId}'
        try:
            response = RequestUtil.get(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''获取列表'''

    def getObjsSubDataList(self, objsCode, objCode, subMetaCode, json):
        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsSubDataList/{objsCode}/{objCode}?prjId={self.prjId}&subMetaCode={subMetaCode}'
        try:
            response = RequestUtil.post(url=url, json=json, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

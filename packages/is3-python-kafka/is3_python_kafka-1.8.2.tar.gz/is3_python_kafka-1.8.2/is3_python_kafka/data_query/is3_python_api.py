import logging
import mimetypes

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


    '''获取元数据列表'''

    def get_meta_table_list(self, json):
        url = f'{self.server_url}/data-main/operation/getDataByCondition'
        json['prjId'] = self.prjId
        return RequestUtil.post(url, json, self.headers)

    '''
            根据自定义编码查询任务流编码。

            参数:
            customCode (str): 自定义任务流编码。
    '''

    def getProcessCode(self, customCode):

        url = f'{self.server_url}/is3-modules-open/scheduling/process-definition-code/custom?customCode={customCode}'
        try:
            response = RequestUtil.get(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    def runProcessDefinition(self, json):
        url = f'{self.server_url}/is3-modules-open/scheduling/start/process-instance'
        customCode = json['customCode']
        result = self.getProcessCode(customCode)
        if result['code'] != 200:
            logging.error("查询异常，结果为：", result)
        processDefinitionCode = result['data']

        initData = {
            'data': json['data']
        }
        temp = {'params': initData}
        # 任务流实例请求参数
        payload = {
            # 任务流编码
            "processDefinitionCode": processDefinitionCode,
            # 实例启动参数
            "startParams": str(temp),
        }
        # payload_json = json.dumps(payload)

        print(payload)

        try:
            response = RequestUtil.post(url=url, json=str(payload), headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            print(response)
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            查询metatable列表数据。

            参数:
            filePath (str): 需要上传的文件路径，包括文件名和扩展名。例如 'E:/uploads/myfile.png'。
    '''

    def getMetaTableList(self, json):
        url = f'{self.server_url}/data-main/operation/getDataByCondition'
        json['prjId'] = self.prjId
        return RequestUtil.post(url, json, self.headers)

    '''
            Minio 文件上传。

            参数:
            filePath (str): 需要上传的文件路径，包括文件名和扩展名。例如 'E:/uploads/myfile.png'。
    '''

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

    # '''
    #         Minio 文件下载
    #
    #         参数:
    #         localPath (str): 文件保存的本地路径，包括文件名和扩展名。例如 'E:/downloads/myfile.png'。
    #         url (str): 文件下载的 URL 地址。例如 'http://example.com/file.png'。
    # '''
    #
    # def downloadFile(self, localPath, url):
    #     parsed_url = urlparse(url)
    #     path = parsed_url.path
    #     path_parts = path.split('/')
    #     path = '/'.join(path_parts[2:])
    #     url = f'{self.server_url}/is3-modules-file/inner/download/?localFilePath={localPath}&filePath={path}'
    #     try:
    #         response = RequestUtil.post(url=url, headers=self.headers)
    #         if response['code'] != 200:
    #             logging.error(f'请求失败，状态码：', response['code'])
    #         print(response)
    #         return response
    #     except Exception as e:
    #         logging.error(f'请求异常：{e}')

    '''
            查询对象组列表 (查询iS3PythonAPi实例化时项目下的数据)
    '''

    def getObjectList(self):
        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsList?prjId={self.prjId}'
        try:
            response = RequestUtil.get(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            查询对象组的对象实例列表。

            参数:
            objsCode (str): 对象组编码。
    '''

    def getObjsInstanceList(self, objsCode):

        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsInstanceList/{objsCode}?prjId={self.prjId}'
        try:
            response = RequestUtil.get(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            查询子类型列表

            参数:
            objsCode (str): 对象组编码。
    '''

    def getObjsSubTypeList(self, objsCode):

        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsSubTypeList/{objsCode}?prjId={self.prjId}'
        try:
            response = RequestUtil.get(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            查询子类型数据
            参数:
                objsCode (str): 对象组代码。
                objCode (str): 对象编码。
                subMetaCode (str): 子类型元数据编码。
                json (dict): 额外的请求参数，以 JSON 格式传递。包括分页、时间范围、比较条件等。
    
                示例 json:
                {
                    "pageNumber": 1,  # 当前页码
                    "pageSize": 10,  # 每页显示的数据条数
                    "startTime": "2024-07-01 15:53:32",  # 查询开始时间
                    "endTime": "2024-09-01 15:53:32",  # 查询结束时间
                    "keyValueCompareEnum": [],  # 关键值比较条件
                    "desc": True  # 是否按降序排列
                }
    '''

    def getObjsSubDataList(self, objsCode, objCode, subMetaCode, json):
        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsSubDataList/{objsCode}/{objCode}?prjId={self.prjId}&subMetaCode={subMetaCode}'
        try:
            response = RequestUtil.post(url=url, json=json, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')
if __name__ == '__main__':
    configPath = r'E:\python_workspace\pycharm_workspace\is3-python-kafka-sdk\is3_python_kafka\config\config.ini'

    is3Api = iS3PythonApi(configPath=configPath, prjId='1821553930207760386')
    res = is3Api.getProcessCode('liefeng')
    print(res)
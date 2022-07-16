import paramiko
import json
import traceback
import logging
import requests
from celery import shared_task
from app01.utils.task_status import TaskHook


"""配置文件"""
ANSIBLE_HOST = '192.168.31.141'
SSH_USER = 'root'
SSH_PORT = 22
SSH_PASSWORD = 'Welcome1234'
LOGGING_PATH = 'cmdb.log'


class BaseResponse(object):
    def __init__(self, status=True, data=None, error=None):
        self.status = status
        self.data = data
        self.error = error

    @property
    def dict(self):
        return self.__dict__


class Logger(object):
    def __init__(self, file_path, level):
        file_handler = logging.FileHandler(file_path, 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s: %(message)s")
        file_handler.setFormatter(fmt)

        self.logger = logging.Logger('CMDB', level=level)
        self.logger.addHandler(file_handler)

    def error(self, msg):
        self.logger.error(msg)


logger = Logger(LOGGING_PATH, logging.DEBUG)


def execute(hostname, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=hostname,
        port=SSH_PORT,
        username=SSH_USER,
        password=SSH_PASSWORD
    )
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read()
    ssh.close()
    return result.decode('utf-8').strip('\n')


@shared_task(base=TaskHook, bind=True)
def process(self):
    result = BaseResponse()
    result.data = {}

    try:
        res = execute(ANSIBLE_HOST, 'ansible all -m setup')
        res_json = json.loads(res)
        asset_obj = res_json['plays'][0]['tasks'][0]['hosts']
        for key in res_json['stats']:
            # print(key, ":", res_json['stats'][key]['ok'])
            # print(res_json['stats'][key])
            if res_json['stats'][key]['ok'] == 1:
                result.data[key] = {}
                sn = {'sn': asset_obj[key]['ansible_facts']['ansible_product_serial']}
                ipv4 = {'ipv4': asset_obj[key]['ansible_facts']['ansible_all_ipv4_addresses'][0]}
                # ipv6_addr = {'ipv6_addr': asset_obj[key]['ansible_facts']['ansible_all_ipv6_addresses']}
                core_num = {'core_num': asset_obj[key]['ansible_facts']['ansible_processor_cores']}
                mem = {'mem': asset_obj[key]['ansible_facts']['ansible_memtotal_mb']}
                disk = {'disk': str(asset_obj[key]['ansible_facts']['ansible_lvm']['vgs'])}
                status = {'status': 1}
                result.data[key].update(sn)
                result.data[key].update(ipv4)
                result.data[key].update(core_num)
                result.data[key].update(mem)
                result.data[key].update(disk)
                result.data[key].update(status)
            else:
                result.data[key] = {"ipv4": key, "status": 2}

    except Exception as e:
        logger.error(traceback.format_exc())
        result.status = False
        result.error = traceback.format_exc()

    post_data = result.dict['data']
    print(post_data)
    for key, value in post_data.items():
        response = requests.post("http://127.0.0.1:8000/api/assets/", data=value)
        print(response.content.decode('utf-8'))

# process()


if __name__ == '__main__':
    process()

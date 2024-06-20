import logging
from datetime import datetime
import requests
import time
import hmac
import json
import yaml
import hashlib
import base64
import urllib.parse
import platform

logging.basicConfig(filename='monitor.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def get_key(secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


def send_to_dingding(access_token, secret, reminders, event, msgtype="text"):
    timestamp, sign = get_key(secret)
    url = "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(access_token,
                                                                                             timestamp, sign)
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    if len(",".join(reminders)) >= 11:
        isAtAll = False
    else:
        isAtAll = True
    if msgtype == "markdown":
        data = {
            "msgtype": msgtype,
            "at": {
                "atMobiles": reminders,
                "isAtAll": isAtAll,
            },
            msgtype: str(event)
        }
    else:
        data = {
            "msgtype": msgtype,
            "at": {
                "atMobiles": reminders,
                "isAtAll": isAtAll,
            },
            msgtype: {
                "content": str(event),
            }
        }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    res_msg = res.json()
    if res_msg["errmsg"] == "ok":
        return "钉钉消息成功推送"
    else:
        return "钉钉消息推送失败，原因:" + res.text


def send_to_server(server_url, PassCard, event):
    headers = {'Content-Type': 'application/json', 'PassCard': base64.b64encode(PassCard.encode('utf-8'))}
    event = {"log": event}
    response = requests.post(server_url, headers=headers, data=json.dumps(event))
    if response.text == "OK":
        ct = "{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logging.info("[{}]告警日志已成功推送到服务器".format(ct))
        return "[{}]告警日志已成功推送到服务器".format(ct)
    else:
        ct = "{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logging.info("[{}]告警日志推送到服务器失败".format(ct))
        return "[{}]告警日志推送到服务器失败".format(ct)


def monitor_linux_events(log_key, access_token, secret):
    notification_list = []
    v_time = time.time()
    os_version = platform.platform()
    max_length = 20
    print("当前操作系统版本[{}]，监控脚本启动成功，正在监控中······".format(os_version))
    while True:
        with open(logPath) as f:
            logs = f.readlines()[-20:]
        for log in logs:
            log_items = log.split()
            log_time_str = ' '.join(log_items[:3])
            log_time = datetime.strptime(log_time_str, '%b %d %H:%M:%S')
            log_time = log_time.replace(year=datetime.now().year)  # 添加年份信息
            if log_time.timestamp() > v_time:
                log_msg = None
                if log_items[5] in log_key:
                    log_msg = '[{}][系统监测到一条告警行为][{}]{}'.format(log_time, os_version, log)
                    logging.info('[{}][系统监测到一条告警行为][{}]{}'.format(log_time, os_version, log))
                if log_msg not in notification_list and log_msg is not None:
                    print(log_msg)
                    notification_list.append(log_msg)
                    if switch == 0:
                        print(send_to_dingding(access_token, secret, "", log_msg))
                    else:
                        print(send_to_server(server_url, PassCard, log_msg))
                if len(notification_list) > max_length:
                    notification_list = notification_list[int(max_length / 2):]
        v_time = time.time()
        time.sleep(1)


if __name__ == '__main__':
    print("""
     _____ For Linux           _           __  __             _ _     V1.0          
    | ____|_   _____ _ __ | |_ ___    |  \/  | ___  _ __ (_) |_ ___  _ __ 
    |  _| \ \ / / _ \ '_ \| __/ __|   | |\/| |/ _ \| '_ \| | __/ _ \| '__|
    | |___ \ V /  __/ | | | |_\__ \   | |  | | (_) | | | | | || (_) | |   
    |_____| \_/ \___|_| |_|\__|___/___|_|  |_|\___/|_| |_|_|\__\___/|_|   
                                 |_____|     
    #Coded By Asaotomo                                   Update:2024.06.20    
                             """)
    with open("monitor_linux_config.yaml", 'r+', encoding='utf-8') as config:
        data = yaml.safe_load(config)
    logPath = data['logPath']
    log_key = data['log_key']
    access_token = data['access_token']
    secret = data['secret']
    server_url = data['server_url']
    PassCard = data['PassCard']
    if access_token is None:
        print("请先在monitor_linux_config.yaml中配置钉钉机器人Webhook中的access_token值！")
        exit()
    if secret is None:
        print("请先在monitor_linux_config.yaml中配置钉钉机器人的加签密钥！")
        exit()
    if server_url is not None and PassCard is not None:
        switch = 1
    else:
        switch = 0
    monitor_linux_events(log_key, access_token, secret)

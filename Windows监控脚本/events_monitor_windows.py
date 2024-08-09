import logging
import win32evtlog
import json
import requests
import time
import hmac
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
    response = requests.post(server_url, headers=headers, data=json.dumps(event))
    if response.text == "OK":
        ct = "{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logging.info("[{}]告警日志已成功推送到服务器".format(ct))
        return "[{}]告警日志已成功推送到服务器".format(ct)
    else:
        ct = "{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logging.info("[{}]告警日志推送到服务器失败".format(ct))
        return "[{}]告警日志推送到服务器失败".format(ct)


def monitor_windows_events(eventid_info, access_token, secret):
    server = 'localhost'
    os_version = platform.platform()
    last_event_time = time.time()  # 记录上一个事件的时间戳
    notification_list = []
    max_length = 20
    print("当前操作系统版本[{}]，监控脚本启动成功，正在监控中······".format(os_version))
    while True:
        hand = win32evtlog.OpenEventLog(server, logtype)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand, flags, 0, 0)
        if events:
            for event in reversed(events):
                event_timestamp = time.mktime(event.TimeGenerated.timetuple())
                if event_timestamp >= last_event_time:  # 只处理新的事件
                    if event.EventID in eventid_info.keys() and event.RecordNumber not in notification_list:
                        print("[{}]系统监测到{}事件".format(event.TimeGenerated, eventid_info[event.EventID]))
                        logging.info("[{}]系统监测到{}事件".format(event.TimeGenerated, eventid_info[event.EventID]))
                        event_data = {
                            "操作系统版本": os_version,
                            "事件记录序号": event.RecordNumber,
                            "事件ID": event.EventID,
                            "事件内容": eventid_info[event.EventID],
                            "任务类别": event.EventType,
                            "日期和时间": str(event.TimeGenerated),
                            "事件源名称": event.SourceName,
                            "计算机名称": event.ComputerName,
                            "事件记录": event.StringInserts
                        }
                        logging.info("事件日志：{}".format(event_data))
                        if switch == 0:
                            print(send_to_dingding(access_token, secret, "", event_data))
                        else:
                            print(send_to_server(server_url, PassCard, event_data))
                        notification_list.append(event.RecordNumber)
                        if len(notification_list) > max_length:
                            notification_list = notification_list[int(max_length / 2):]
                        last_event_time = event_timestamp  # 更新最后一个事件的时戳
        time.sleep(1)  # 添加延迟，避免过于频繁的读取事件日志


if __name__ == '__main__':
    print("""
     _____For Windows          _           __  __             _ _     V1.0          
    | ____|_   _____ _ __ | |_ ___    |  \/  | ___  _ __ (_) |_ ___  _ __ 
    |  _| \ \ / / _ \ '_ \| __/ __|   | |\/| |/ _ \| '_ \| | __/ _ \| '__|
    | |___ \ V /  __/ | | | |_\__ \   | |  | | (_) | | | | | || (_) | |   
    |_____| \_/ \___|_| |_|\__|___/___|_|  |_|\___/|_| |_|_|\__\___/|_|   
                                 |_____|     
    #Coded By Asaotomo                                   Update:2024.08.01    
                             """)
    with open("monitor_windows_config.yaml", 'r+', encoding='utf-8') as config:
        data = yaml.safe_load(config)
    logtype = data['logtype']
    eventid_info = data['eventid_info']
    access_token = data['access_token']
    secret = data['secret']
    server_url = data['server_url']
    PassCard = data['PassCard']
    if access_token is None:
        print("请先在monitor_windows_config.yaml中配置钉钉机器人Webhook中的access_token值！")
        exit()
    if secret is None:
        print("请先在monitor_windows_config.yaml中配置钉钉机器人的加签密钥！")
        exit()
    if server_url is not None and PassCard is not None:
        switch = 1
    else:
        switch = 0
    monitor_windows_events(eventid_info, access_token, secret)

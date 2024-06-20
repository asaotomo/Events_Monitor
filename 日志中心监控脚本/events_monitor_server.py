import base64
from flask import Flask, request
import logging
import json
import requests
import time
import hmac
import yaml
import hashlib
import urllib.parse
import SparkApi

app = Flask(__name__)

logging.basicConfig(filename='monitor_server.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


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


@app.route('/monitor_api', methods=['POST'])
def monitor_api():
    # 校验请求头是否包含 PassCard 参数
    ct = "{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    remote_addr = request.remote_addr
    if 'PassCard' in request.headers:
        # 获取 PassCard 参数的值并进行 base64 解码
        passcard_value = request.headers['PassCard']
        decoded_passcard = base64.b64decode(passcard_value).decode('utf-8')
        # 判断解码后的值是否等于 Hx0@2023
        if decoded_passcard == PassCard:
            event = request.get_json()
            event["告警客户端"] = remote_addr
            print("[{}][收到来自{}的消息]{}".format(ct, remote_addr, event))
            logging.info("[{}][收到来自{}消消息]{}".format(ct, remote_addr, event))
            if spark_switch == "on":
                question = checklen(getText("user", "我收到了一条告警日志，请帮我分析：{}".format(event)))
                SparkApi.answer = ""
                SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
                SparkAnswer = SparkApi.answer
                send_to_dingding(access_token, secret, "",
                                 "【告警日志】\n{}\n\n【以下来自星火大模型的分析】\n{}".format(event, str(SparkAnswer)))
            else:
                send_to_dingding(access_token, secret, "",
                                 "【告警日志】\n{}\n".format(event))
            return 'OK'
        else:
            print("[{}][{}触发了告警]PassCard输入错误".format(ct, remote_addr, ))
            logging.info("[{}][{}触发了告警]PassCard输入错误".format(ct, remote_addr, ))
            return 'Invalid PassCard parameter', 403
    else:
        print("[{}][{}触发了告警]缺少PassCard参数".format(ct, remote_addr, ))
        logging.info("[{}][{}触发了告警]缺少PassCard参数".format(ct, remote_addr, ))
        return 'Missing parameter', 403


if __name__ == '__main__':
    with open("events_monitor_server.yaml", 'r+', encoding='utf-8') as config:
        data = yaml.safe_load(config)
    for key in data.keys():
        if data[key] is None:
            print("[系统监测到配置异常]请先在events_monitor_server.yaml中配置{}值".format(key))
            exit()
    PassCard = data['PassCard']
    server_host = data['server_host']
    server_port = data['server_port']
    access_token = data['access_token']
    secret = data['secret']
    spark_switch = data['spark_switch']
    appid = data["appid"]
    api_secret = data["api_secret"]  # 填写控制台中获取的 APISecret 信息
    api_key = data["api_key"]  # 填写控制台中获取的 APIKey 信息
    domain = data["domain"]  # v1.5版本
    Spark_url = data["Spark_url"]
    Prompt = data["Prompt"]
    text = []
    init_time = 0
    if spark_switch == "on":
        question = checklen(getText("user", Prompt))
        SparkApi.answer = ""
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    app.run(host=server_host, port=server_port, debug=False)

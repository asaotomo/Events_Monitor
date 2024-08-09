## 一、**概述**
   随着网络安全问题日益严峻，各单位的系统每时每刻都面临着各种潜在的风险和挑战。我们经过调研，发现目前市场上很少有针对服务器高危行为的实时监控告警工具。为了增强网络安全和监控能力，我们设计了一个全场景的"events_monitor"服务器高危行为监控工具。该脚本的目标是实时监控和告警服务器上的高危行为，例如账号登录、登出、新增、删除等操作。通过实时监测服务器端的高危行为，我们能够及时感知潜在的安全威胁，并增强对安全事件的监控能力。
   在HW期间，系统的安全性可能更易受到威胁，因此我们需要建立实时的告警机制，及时通知相关人员。为此，我们通过与钉钉机器人的WebHook接口实现联动，"events_monitor"工具能够在发现异常登录或登出行为时立即发送告警通知。这样，安全管理员和相关人员能够迅速响应并采取适当的安全措施。
   另外，为了增强日志分析能力，我们在脚本中创新地引入了星火大模型。通过分析和评估监测到的日志，我们能够更好地理解和评估安全事件的风险和威胁，并采取相应的反应和对策。这种联动提供了更全面的安全智能功能，有助于在HW期间快速定位问题，并进行紧急处理措施。
   考虑到服务器操作系统和网络环境的差异，我们针对Windows和Linux系统分别设计了不同的客户端，并引入了YAML配置文件。用户可以根据自身需求自定义要监控的日志和需要进行告警的内容。此外，我们还考虑到了不出网设备的情况，为此提供了日志监控中心的脚本。该脚本能够收集来自Windows和Linux平台的日志，并经过汇总分析后统一转发给钉钉群。
通过优化脚本设计，我们提高了网络安全监控能力，使系统能够快速响应潜在风险和挑战。这个脚本的开发和实施旨在确保系统安全、保障业务连续性，在HW期间有效地管理和应对安全问题。

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/4200a3fc-d093-4e83-b741-de5ef8e7ee16)

工作原理图

## 二、**实现原理**
基于以上概述，Hx0战队根据实际工作场景和需求，拟出了如下的高危行为监控脚本的设计思路：

**平台适配性：** 工具提供了适用于Windows和Linux操作系统的不同版本，确保在不同的操作系统上都能进行日志监控。这使得企业可以在混合操作系统环境下统一使用该工具进行安全监控，而无须依赖不同的工具或方法。

**实时监测功能：** 工具通过轮询的方式实时监测安全日志文件，对用户的登录和登出行为进行持续监控。在Windows系统中，工具解析Security日志；而在Linux系统中，工具针对不同内核的操作系统监测/var/log/secure或/var/log/auth.log文件。这种实时监测的机制使得用户可以及时感知到潜在的安全威胁，从而能够迅速采取必要的应对措施。

**告警机制：** 一旦工具检测到新的登录或登出等高危行为，它会通过钉钉群聊机器人进行告警通知，同时在本地和日志中心都会记录该告警日志。这样，安全管理员和相关人员可以及时收到告警消息，快速了解到发生的安全事件，并采取适当的响应措施。告警机制的实施有助于提高安全事件的响应效率和准确性。

**星火大模型联动：** 工具与星火大模型进行联动，可以对监测到的日志进行更深入的分析和评估。星火大模型是一个强大的安全分析工具，能够识别异常模式、发现隐藏的威胁，并提供高级的安全智能功能。通过与星火大模型的联动，工具可以进一步提升对日志的审计和威胁评估能力。

**灵活的告警推送方式：** 工具考虑到服务器的网络连通性，提供了灵活的告警推送方式。如果服务器可以访问外网，告警信息将直接发送给钉钉群聊机器人，以确保及时地通知；如果服务器无法访问外网，工具将把告警信息统一推送给日志监控中心，再由日志监控中心进行二次推送。这种灵活的推送方式，确保了告警信息的可靠传递，无论服务器是否能够与外部网络进行通信。

根据以上思路，Hx0战队组织编译了一套全平台的服务器高危行为监控告警工具，用于HW和日常服务器行为监测工作，具体工具清单如下:

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/dc96f292-f291-4992-a64e-2ea4e2fd8374)


(1)events_monitor_linux.py：Linux平台监测脚本

(2)monitor_linux_config.yaml：Linux脚本监控配置文件

(3)events_monitor_windows.py：Windows平台监测脚本

(4)monitor_windows_config.yaml：Windows平台脚本配置文件

(5)events_monitor_server.py：日志监控中心脚本

(6)events_monitor_server.yaml：日志监控中心配置文件

(7)SparkApi.yaml：星火大模型API文件

(8)requirements.txt：用于记录所有脚本运行所需的依赖包

events_monitor_linux.py作为Linux平台的监控脚本，是通过对指定的Linux日志进行轮询，并监测是否存在yaml文件中设置的文件来判断高危告警行为。

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/d41e1107-2d5e-46df-b448-7c26bdc8acde)

我们可以通过修改monitor_linux_config.yaml中的log_key和logPath来对不同日志类型和内容进行监控。若在配置文件中配置了server_url和PassCard系统则默认将日志转发给日志监控中心而不是直接推送给钉钉群聊机器人。

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/fbf2e1ac-55f7-459b-8420-958ece21aeaa)

events_monitor_windows.py作为Windows平台的监控脚本，是通过对指定的Windows系统日志进行轮询，并监测是否存在yaml文件中设置的文件来判断是否存在高危告警行为。

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/dbdb4007-8677-43a5-87a3-451107a6c347)

我们可以通过修改monitor_windows_config.yaml中的logtype和eventid—_info来对不同日志类型和内容进行监控。若在配置文件中配置了server_url和PassCard系统则默认将日志转发给日志监控中心而不是直接推送给钉钉群聊机器人。

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/99f64602-3b5b-4dc1-8dbe-2c1e9a5eee78)

events_monitor_windows.py作为Windows平台的监控脚本，是通过对指定的Windows系统日志进行轮询，并监测是否存在yaml文件中设置的文件来判断是否存在高危告警行为。
events_monitor_server.py作为日志监控中心可以接收来自不同平台的监控日志，并将日志推送给钉钉聊天机器人，日志监控中心可以部署在Windows服务器上也可部署在Linux服务器上，但是请确保该服务器可以出网，同时为了安全我们设计了安全密钥，来自其他平台的POST请求包必须包含安全密钥日志监控中心才会进行接收和转发，否则会将该日志直接丢弃。

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/58dec97d-32f4-4324-96fc-14d0f683715b)

我们可以通过events_monitor_server.yaml来设置日志监控中心的监听地址、端口、安全密钥，以及大模型的开关、API等信息，需注意一个好的Prompt能够对日志分析起到一个关键性的作用，用户可以更具自己的需求来修改自己的Prompt。

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/fb5b70ce-334e-4a72-9b6b-08e938879ab2)

## 三、**工具部署**
首先安装日志监控中心requirements.txt依赖

```pip3 install -r requirements.txt```

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/45b233d9-f474-4f31-8395-b3d94d1006bc)

为了保持脚本可以稳定在后台运行，我们通过screen命令来创建一个终端。
```
创建：screen -S ###
查看有多少会话：screen -ls
恢复：screen -r ###
如果不能恢复：先screen -d ###
再screen -r ###
删除screen -S ### -X quit
```

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/d66372f1-0f4a-4b2e-b78c-a0b6086cecef)


配置好yaml文件后直接运行```python3 events_monitor_server.py```

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/da932ddb-2c36-4f28-8688-8ea326ad2e52)

然后我们在一台Windows服务器上启动events_monitor_windows.py脚本。

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/2d85a8e2-02d0-4df7-8af8-55843d8ea115)

在Linux服务器上启动monitor_linux_config.yaml脚本。

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/f7799013-5f12-4c59-90d5-4b1293a702ff)

例如当我们模仿黑客远程桌面登录Windows服务器时，Windows监测脚本会监测到登录行为并推送给日志中心，日志中心收到来自Windows服务器的告警后联动星火大模型进行分析，之后将分析结果推送给钉钉群。

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/bd8ece37-f742-4e05-b4ae-7271ee2b0a12)

Windows服务器截图

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/5adc1826-adcd-4510-8a97-7ec192cb90f9)

Windows服务器本地日志截图

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/83fdec56-3442-4c91-adf8-4990ee316369)

日志中心截图

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/ddbe2c3c-154f-439e-b354-297c3c9c8488)

日志中心本地日志截图

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/046a14b4-b364-44e5-b74f-6f9ab94f4ef5)

钉钉群推送信息
再例如当我们模仿黑客SSH暴力破解登录Linux服务器时，Linux监测脚本会监测到登录行为并推送给日志中心，日志中心收到来自Linux服务器的告警后联动星火大模型进行分析，之后将分析结果推送给钉钉群。

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/417bf6a6-a79d-466e-b8c5-f60111805d84)

Linux服务器截图

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/2dd91ff8-7ace-461f-8dda-a975f78aa1f3)

Linux服务器本地日志截图

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/93e26ac2-6eac-4800-91e0-29594daea1bb)

日志中心截图

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/0055650d-9348-4cc5-bd74-bf66cb81ad52)

日志中心本地LOG截图

![image](https://github.com/asaotomo/Events_Monitor/assets/67818638/d0512406-a982-43bc-8721-a24c0f127764)

钉钉群推送信息

## 四、**总结**
从实战过程我们发现，通过在HW期间设计和使用"events_monitor"脚本，我们增强了防守单位服务器的高危行为监控能力，提高对安全事件的感知和响应能力，减少潜在的安全风险。这个脚本的开发与实施，旨在保障系统的安全性，确保在HW期间能够有效管理和应对可能出现的安全挑战，同时大模型的引入也进一步提升我们对日志的审计和威胁评估能力。

---

**本工具仅提供给安全测试人员进行安全自查使用**，**用户滥用造成的一切后果与作者无关**，**使用者请务必遵守当地法律** **本程序不得用于商业用途，仅限学习交流。**

---

**扫描关注战队公众号，获取最新动态**

<img width="318" alt="image" src="https://user-images.githubusercontent.com/67818638/149507366-4ada14db-a972-4071-bbb6-197659f61ced.png">

**【知识星球】福利大放送**

<img width="318" alt="image" src="https://github.com/asaotomo/ZipCracker/assets/67818638/659b508c-12ad-47a9-8df5-f2c36403c02b">


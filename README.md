## 一、**概述**
随着网络安全问题日益严峻，各单位的系统每时每刻都面临着各种潜在的风险和挑战。我们经过调研，发现目前市场上很少有针对服务器高危行为的实时监控告警工具。为了增强网络安全和监控能力，我们设计了一个全场景的"events_monitor"服务器高危行为监控工具。该脚本的目标是实时监控和告警服务器上的高危行为，例如账号登录、登出、新增、删除等操作。通过实时监测服务器端的高危行为，我们能够及时感知潜在的安全威胁，并增强对安全事件的监控能力。
在HW期间，系统的安全性可能更易受到威胁，因此我们需要建立实时的告警机制，及时通知相关人员。为此，我们通过与钉钉机器人的WebHook接口实现联动，"events_monitor"工具能够在发现异常登录或登出行为时立即发送告警通知。这样，安全管理员和相关人员能够迅速响应并采取适当的安全措施。
另外，为了增强日志分析能力，我们在脚本中创新地引入了星火大模型。通过分析和评估监测到的日志，我们能够更好地理解和评估安全事件的风险和威胁，并采取相应的反应和对策。这种联动提供了更全面的安全智能功能，有助于在HW期间快速定位问题，并进行紧急处理措施。
考虑到服务器操作系统和网络环境的差异，我们针对Windows和Linux系统分别设计了不同的客户端，并引入了YAML配置文件。用户可以根据自身需求自定义要监控的日志和需要进行告警的内容。此外，我们还考虑到了不出网设备的情况，为此提供了日志监控中心的脚本。该脚本能够收集来自Windows和Linux平台的日志，并经过汇总分析后统一转发给钉钉群。
通过优化脚本设计，我们提高了网络安全监控能力，使系统能够快速响应潜在风险和挑战。这个脚本的开发和实施旨在确保系统安全、保障业务连续性，在HW期间有效地管理和应对安全问题。
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850529185-f1be492b-0c36-459c-9af3-478d50013974.png#averageHue=%230f497f&clientId=uee402815-e759-4&from=paste&height=360&id=u6545f96e&originHeight=720&originWidth=1108&originalType=binary&ratio=2&rotation=0&showTitle=false&size=3196997&status=done&style=none&taskId=u8ff28242-e356-4455-8e97-13c1d5bba8f&title=&width=554)
工作原理图

## 二、**实现原理**
基于以上概述，Hx0战队根据实际工作场景和需求，拟出了如下的高危行为监控脚本的设计思路：

**平台适配性：** 工具提供了适用于Windows和Linux操作系统的不同版本，确保在不同的操作系统上都能进行日志监控。这使得企业可以在混合操作系统环境下统一使用该工具进行安全监控，而无须依赖不同的工具或方法。

**实时监测功能：** 工具通过轮询的方式实时监测安全日志文件，对用户的登录和登出行为进行持续监控。在Windows系统中，工具解析Security日志；而在Linux系统中，工具针对不同内核的操作系统监测/var/log/secure或/var/log/auth.log文件。这种实时监测的机制使得用户可以及时感知到潜在的安全威胁，从而能够迅速采取必要的应对措施。

**告警机制：** 一旦工具检测到新的登录或登出等高危行为，它会通过钉钉群聊机器人进行告警通知，同时在本地和日志中心都会记录该告警日志。这样，安全管理员和相关人员可以及时收到告警消息，快速了解到发生的安全事件，并采取适当的响应措施。告警机制的实施有助于提高安全事件的响应效率和准确性。

**星火大模型联动：** 工具与星火大模型进行联动，可以对监测到的日志进行更深入的分析和评估。星火大模型是一个强大的安全分析工具，能够识别异常模式、发现隐藏的威胁，并提供高级的安全智能功能。通过与星火大模型的联动，工具可以进一步提升对日志的审计和威胁评估能力。

**灵活的告警推送方式：** 工具考虑到服务器的网络连通性，提供了灵活的告警推送方式。如果服务器可以访问外网，告警信息将直接发送给钉钉群聊机器人，以确保及时地通知；如果服务器无法访问外网，工具将把告警信息统一推送给日志监控中心，再由日志监控中心进行二次推送。这种灵活的推送方式，确保了告警信息的可靠传递，无论服务器是否能够与外部网络进行通信。

根据以上思路，Hx0战队组织编译了一套全平台的服务器高危行为监控告警工具，用于HW和日常服务器行为监测工作，具体工具清单如下:
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850536796-6886e538-8d96-4dba-b913-fe1aaa6a55f2.png#averageHue=%23f1f2f2&clientId=uee402815-e759-4&from=paste&height=187&id=ud4c1e276&originHeight=374&originWidth=1280&originalType=binary&ratio=2&rotation=0&showTitle=false&size=1918424&status=done&style=none&taskId=u65ca4633-3c3b-4d25-8f6e-d3917182d6d&title=&width=640)

(1)events_monitor_linux.py：Linux平台监测脚本

(2)monitor_linux_config.yaml：Linux脚本监控配置文件

(3)events_monitor_windows.py：Windows平台监测脚本

(4)monitor_windows_config.yaml：Windows平台脚本配置文件

(5)events_monitor_server.py：日志监控中心脚本

(6)events_monitor_server.yaml：日志监控中心配置文件

(7)SparkApi.yaml：星火大模型API文件

(8)requirements.txt：用于记录所有脚本运行所需的依赖包

events_monitor_linux.py作为Linux平台的监控脚本，是通过对指定的Linux日志进行轮询，并监测是否存在yaml文件中设置的文件来判断高危告警行为。
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850588148-174779fc-2b5c-4b66-a0c1-8d50df6820ff.png#averageHue=%23343d47&clientId=uee402815-e759-4&from=paste&height=302&id=u9c8f8186&originHeight=603&originWidth=1280&originalType=binary&ratio=2&rotation=0&showTitle=false&size=3093041&status=done&style=none&taskId=u278742f0-1059-4542-89dd-950435324e7&title=&width=640)
我们可以通过修改monitor_linux_config.yaml中的log_key和logPath来对不同日志类型和内容进行监控。若在配置文件中配置了server_url和PassCard系统则默认将日志转发给日志监控中心而不是直接推送给钉钉群聊机器人。
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850594350-6b9b76e2-d780-46eb-9520-2de71880c24c.png#averageHue=%233b434d&clientId=uee402815-e759-4&from=paste&height=349&id=uc4090eef&originHeight=697&originWidth=1280&originalType=binary&ratio=2&rotation=0&showTitle=false&size=3575181&status=done&style=none&taskId=uc4122cfc-cb5c-4fc6-b12b-108063f6e5d&title=&width=640)
events_monitor_windows.py作为Windows平台的监控脚本，是通过对指定的Windows系统日志进行轮询，并监测是否存在yaml文件中设置的文件来判断是否存在高危告警行为。
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850601941-eb4d6f7b-7cec-40ea-b4e5-144973abe777.png#averageHue=%23373f49&clientId=uee402815-e759-4&from=paste&height=360&id=ude61e054&originHeight=720&originWidth=1087&originalType=binary&ratio=2&rotation=0&showTitle=false&size=3136423&status=done&style=none&taskId=u3e947828-504b-4d9a-840c-7c32f109c7d&title=&width=543.5)
我们可以通过修改monitor_windows_config.yaml中的logtype和eventid—_info来对不同日志类型和内容进行监控。若在配置文件中配置了server_url和PassCard系统则默认将日志转发给日志监控中心而不是直接推送给钉钉群聊机器人。
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850608600-1c7a3d26-105d-48db-a3c9-082a03ec8143.png#averageHue=%2338404a&clientId=uee402815-e759-4&from=paste&height=360&id=ud54b55dc&originHeight=720&originWidth=1180&originalType=binary&ratio=2&rotation=0&showTitle=false&size=3404687&status=done&style=none&taskId=ucc52f9ed-5201-43ba-a826-c9e2e3e8aa0&title=&width=590)
events_monitor_windows.py作为Windows平台的监控脚本，是通过对指定的Windows系统日志进行轮询，并监测是否存在yaml文件中设置的文件来判断是否存在高危告警行为。
events_monitor_server.py作为日志监控中心可以接收来自不同平台的监控日志，并将日志推送给钉钉聊天机器人，日志监控中心可以部署在Windows服务器上也可部署在Linux服务器上，但是请确保该服务器可以出网，同时为了安全我们设计了安全密钥，来自其他平台的POST请求包必须包含安全密钥日志监控中心才会进行接收和转发，否则会将该日志直接丢弃。
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850611261-edb7fc24-9fb7-443c-83cb-53fdebf02032.png#averageHue=%23232427&clientId=uee402815-e759-4&from=paste&height=360&id=uc8b4e8fc&originHeight=720&originWidth=916&originalType=binary&ratio=2&rotation=0&showTitle=false&size=2643153&status=done&style=none&taskId=u462508f1-288f-433f-9ba4-7de1814bf78&title=&width=458)
我们可以通过events_monitor_server.yaml来设置日志监控中心的监听地址、端口、安全密钥，以及大模型的开关、API等信息，需注意一个好的Prompt能够对日志分析起到一个关键性的作用，用户可以更具自己的需求来修改自己的Prompt。

## 三、**工具部署**
首先安装日志监控中心requirements.txt依赖
pip3 install -r requirements.txt 
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850687367-9e12ff4e-10b1-41db-9e08-818854583bef.png#averageHue=%23141829&clientId=uee402815-e759-4&from=paste&height=360&id=u6fd40bb1&originHeight=720&originWidth=1229&originalType=binary&ratio=2&rotation=0&showTitle=false&size=3546048&status=done&style=none&taskId=ufc81d3cb-229f-457d-8907-fbc61a749dd&title=&width=614.5)
为了保持脚本可以稳定在后台运行，我们通过screen命令来创建一个终端。
创建：screen -S ###
查看有多少会话：screen -ls
恢复：screen -r ###
如果不能恢复：先screen -d ###
再screen -r ###
删除screen -S ### -X quit
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850686313-b29d5122-85e6-483c-99ad-46ead760d18c.png#averageHue=%23151c2c&clientId=uee402815-e759-4&from=paste&height=55&id=ucf2896a1&originHeight=109&originWidth=1280&originalType=binary&ratio=2&rotation=0&showTitle=false&size=559174&status=done&style=none&taskId=ueb27fbc6-9bd8-4571-ad6e-18d98d797a5&title=&width=640)
配置好yaml文件后直接运行python3 events_monitor_server.py
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850699227-e4356276-eef9-4887-8245-c420479cad8d.png#averageHue=%23141829&clientId=uee402815-e759-4&from=paste&height=115&id=u06a439e2&originHeight=230&originWidth=1280&originalType=binary&ratio=2&rotation=0&showTitle=false&size=1179805&status=done&style=none&taskId=uc1783699-7ea2-463b-aac6-31b87630d9e&title=&width=640)
然后我们在一台Windows服务器上启动events_monitor_windows.py脚本。
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850709450-2d2f53d8-e8cc-4eff-8267-b1ed84b2fba8.png#averageHue=%23161616&clientId=uee402815-e759-4&from=paste&height=213&id=uca8a76d4&originHeight=426&originWidth=1280&originalType=binary&ratio=2&rotation=0&showTitle=false&size=2185152&status=done&style=none&taskId=ud46ae54a-0800-4fea-996c-eab18bc7341&title=&width=640)
在Linux服务器上启动monitor_linux_config.yaml脚本。
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850722318-6c26b77d-b37b-485c-bd4f-38a48069cb66.png#averageHue=%23141729&clientId=uee402815-e759-4&from=paste&height=360&id=u75de85a5&originHeight=720&originWidth=1167&originalType=binary&ratio=2&rotation=0&showTitle=false&size=3367194&status=done&style=none&taskId=u6054abb8-0b97-471a-8311-c424a17ca94&title=&width=583.5)
例如当我们模仿黑客远程桌面登录Windows服务器时，Windows监测脚本会监测到登录行为并推送给日志中心，日志中心收到来自Windows服务器的告警后联动星火大模型进行分析，之后将分析结果推送给钉钉群。
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850723935-8a8b75bf-ff26-4086-b0ef-05ef68653f82.png#averageHue=%23161616&clientId=uee402815-e759-4&from=paste&height=264&id=ub44f7816&originHeight=528&originWidth=1280&originalType=binary&ratio=2&rotation=0&showTitle=false&size=2708342&status=done&style=none&taskId=u6027ce08-a187-42ef-a135-443be820d03&title=&width=640)
Windows服务器截图
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850734060-8f0658b1-8a54-472b-b7d9-d742df08aaaf.png#averageHue=%23f4f1ee&clientId=uee402815-e759-4&from=paste&height=360&id=ua810270c&originHeight=720&originWidth=1251&originalType=binary&ratio=2&rotation=0&showTitle=false&size=3609497&status=done&style=none&taskId=uda9e9a05-b102-4307-9240-536cf26cc1d&title=&width=625.5)
Windows服务器本地日志截图
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850739464-468fefba-eab5-443b-a9b7-f383d8a1a07a.png#averageHue=%23141829&clientId=uee402815-e759-4&from=paste&height=360&id=ubeac0dd8&originHeight=720&originWidth=1051&originalType=binary&ratio=2&rotation=0&showTitle=false&size=3032572&status=done&style=none&taskId=u4ce2d724-cb76-495e-8d61-69543c8b3ca&title=&width=525.5)
日志中心截图
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850741673-ad2b38c4-4b6e-433e-821e-a2331403e27d.png#averageHue=%2314192a&clientId=uee402815-e759-4&from=paste&height=262&id=uec4a484a&originHeight=523&originWidth=1280&originalType=binary&ratio=2&rotation=0&showTitle=false&size=2682684&status=done&style=none&taskId=u718b9e46-6467-47c5-b607-33361c109b4&title=&width=640)
日志中心本地日志截图

钉钉群推送信息
再例如当我们模仿黑客SSH暴力破解登录Linux服务器时，Linux监测脚本会监测到登录行为并推送给日志中心，日志中心收到来自Linux服务器的告警后联动星火大模型进行分析，之后将分析结果推送给钉钉群。
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850761473-f1ba39b9-00eb-4c96-b39b-4d4e5241685f.png#averageHue=%2314182a&clientId=uee402815-e759-4&from=paste&height=360&id=uae7e9fb4&originHeight=720&originWidth=1019&originalType=binary&ratio=2&rotation=0&showTitle=false&size=2940265&status=done&style=none&taskId=u578db1d0-d0f5-45a9-9fe3-5dc1be23b63&title=&width=509.5)
Linux服务器截图
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850764729-a00a6cd3-38f9-4492-a480-3bf831a50304.png#averageHue=%2314182a&clientId=uee402815-e759-4&from=paste&height=248&id=u7a47b12e&originHeight=495&originWidth=1280&originalType=binary&ratio=2&rotation=0&showTitle=false&size=2539072&status=done&style=none&taskId=u4a224f83-7902-4711-a2be-22816433b0f&title=&width=640)
Linux服务器本地日志截图
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850768045-4560611f-f56b-477e-816a-55f27ef4ea98.png#averageHue=%23141829&clientId=uee402815-e759-4&from=paste&height=216&id=ue0eac6ff&originHeight=431&originWidth=1280&originalType=binary&ratio=2&rotation=0&showTitle=false&size=2210798&status=done&style=none&taskId=ub3a63410-4482-4bfa-9af0-ce935b9d5e6&title=&width=640)
日志中心截图
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850773617-9cc766de-8425-4c36-aa89-ee9c9136ddb1.png#averageHue=%2314192a&clientId=uee402815-e759-4&from=paste&height=360&id=u9ef85483&originHeight=720&originWidth=1077&originalType=binary&ratio=2&rotation=0&showTitle=false&size=3107570&status=done&style=none&taskId=u2e996ebd-ed09-4b8c-b580-d8a3998f775&title=&width=538.5)
日志中心本地LOG截图
![image.png](https://cdn.nlark.com/yuque/0/2024/png/12839102/1718850776819-bf6775df-9355-4bfd-95a1-44eeb7d944ca.png#averageHue=%23f5e1cc&clientId=uee402815-e759-4&from=paste&height=360&id=u8583c186&originHeight=720&originWidth=1007&originalType=binary&ratio=2&rotation=0&showTitle=false&size=2905652&status=done&style=none&taskId=uec682e61-cd20-4265-9236-d3ea4691c28&title=&width=503.5)
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


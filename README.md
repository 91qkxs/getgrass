# getgrass.io脚本

### 本项目为grass运行脚本

目前市面上很多代挂工作室或者，本脚本主要服务需要的人

项目官网https://app.getgrass.io/register/?referralCode=xv4tsqSC9SftAXJ

为什么浏览器可以挖要用脚本？在浏览器环境必须打开浏览器才能挖，很多人想多号或者在linux等环境下运行，此时这个脚本就发挥用武之地

### 使用教程

- 安装python

  ​	环境要求python 3.9以上,具体操作百度一下

- 导包

  单独导包：grass.py文件都复制到你的服务器某个目录下依次运行pip3 install websockets  、pip3 install websockets_proxy、pip3 install Faker 、pip3 install async_timeout

  批量导包：把 requirements.txt文件、grass.py文件都复制到你的服务器某个目录下，pip3 install -r requirements.txt

- 将main方法参数换成你的

  ~~~python
      user_id = '5b62d235-273c-4707-85df-9bcca26a5306' #你自己的user_id
      use_proxy = False  # 设置为 True 则使用代理，False 则不使用,根据自己需求
      # socks5代理账号密码模式 格式'socks5://username:password@address:port'
      # socks5代理无密码模式格式 'socks5://address:port'
      proxies = [Proxy.from_url("socks5://192.168.124.20:1082"),Proxy.from_url("socks5://udk390:32384@182.44.113.41:16790")]#如果使用代理把这里改成你的，使用几个改几个
  
  
  ~~~

  

  user_id改为你的user_id

  如果不用代理不用动，如果使用代理就use_proxy设置为True，然后在下面addr和port填写的代理ip和密码

  如果代理有用户名密码下面接着填。没有就把username和password删了即可
  
  然后运行：python3 grass.py即可

  如何配置多号？

  多号你就在这里多配置几个代理信息，然后遍历循环，开启多线程，保障每个线程一个单独ip即可。

- 如何获取user_id

  打开链接登录https://app.getgrass.io/dashboard,  然后浏览器按F12打开开发者工具 在控制台（console）输入下面代码

  ```
  localStorage.userId
  ```

  打印的就是你目前的user_id

  ![image-20240206145338215](https://raw.githubusercontent.com/91qkxs/tc/file/uPic/image-20240206145338215.png)

  如果第一次用出现这样警告，就按提示输入allow pasting即可粘贴

  ![image-20240206145444725](https://raw.githubusercontent.com/91qkxs/tc/file/uPic/image-20240206145444725.png)


# 一定要使用纯净家庭宽带ip否则跑不起来的 跑不起来检测自己网络问题，像阿里云这些机房服务器没积分的
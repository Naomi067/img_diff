import os
import requests
from jinja2 import Template
import time
import datetime

# 定义模板字符串
template_str = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>天谕手游测试组</title>
  </head>

  <body class="page-body">
    <div class="main-content" style="display: block; margin-top: 0px">
      <div class="row">
        <div class="col-md-2 col-sm-2"></div>
        <!-- 报告正文标题区域 -->
        <div class="col-md-8 col-lg-8 col-sm-8">
          <div style="margin-bottom: 10px; background-color: white">
            <div style="font-size: 28px; text-align: center">
              <a
                style="
                  font-family: 黑体;
                  color: #666666;
                  font-size: 24px;
                  margin-bottom: 2px;
                "
                >本周时装对比统计</a
              >
            </div>
          </div>
        <div>
            <p>本周次共测试时装数量{{ total_count }}个，需二次确认时装{{ num }}个：</p>
            <ul>
              {% for filename in cid_list %}
              <li>{{ filename }}</li>
              {% endfor %}
            </ul>
          </div>
          {% for cid in cid_list %}
          <img src="cid:{{ cid }}" style="max-width: 100%;">
          {% endfor %}
        </div>
      </div>
    </div>
  </body>
</html>
'''

# send msg
HELP_USER_NAME = "wangxin7"
MAIL_URL = "http://qa.leihuo.netease.com/webservice/mail/send"
POPO_URL = "http://qa.leihuo.netease.com:3316/popo_qatool"
RECV_USER = "zhangjing32@corp.netease.com,wb.huokunsong01@mesg.corp.netease.com,limengxue04@corp.netease.com,wb.mashiyao01@mesg.corp.netease.com,pangumqa.pm02@list.nie.netease.com"
MAIL_TITLE = "[天谕手游][时装对比][TEST] "
RESULT_MAIL = "resultMail.html"
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
HTML_PATH = "%s\\template"%BASE_PATH
IMG_PATH = 'G:/img_diff/tools/AllImages/L32_result'
TIME_FORMAT = "%Y%m%d%H%M%S"
WHICH_DAY = 4
DELTA_TIME = 7*24*3600

def makeNewEmailPage(image_paths, total_count):
    files = {}
    cid_list = []
    for filename in os.listdir(image_paths):
        with open(os.path.join(image_paths, filename), "rb") as f:
            cid = os.path.splitext(filename)[0]
            cid_list.append(cid)
            files[filename] = (filename, f.read(), "", {"Content-ID": cid})
    template = Template(template_str)
    mailContent = template.render(cid_list=cid_list,total_count=total_count,num=len(cid_list))

    resultMailPath = "%s/%s" % (HTML_PATH, RESULT_MAIL)
    with open(resultMailPath, "w", encoding='utf-8') as f:
        f.write(mailContent)
    return files

def sendMailToUser(userName, subject, content, files):
    """
        userName：发送目标。多人使用英文逗号,分隔。如没有@符号，会自动加上加@corp.netease.com后缀
        subject: 邮件主题
        content: 邮件内容。如果包含</html>标签，会以html方式来发送。否则，以plain方式来发送
    """
    payload = {
        "to": userName,
        "cc": HELP_USER_NAME,
        "subject": subject,
        "content":content,
    }
    try:
        r = requests.post(MAIL_URL, payload,files=files)
        if r.text != "OK":
            print(">Send Mail Failed: %s"%str(r.text))
            msg = "[UIOpenLogCount][Error] Send Mail Failed"
            sendPopoMsg(HELP_USER_NAME, msg)
    except Exception as e:
        print(">Send Mail Error: %s"%str(e))
        msg = "[UIOpenLogCount][Error] Send Mail Error:\r%s"%str(e)
        sendPopoMsg(HELP_USER_NAME, msg)

def sendPopoMsg(to, msg):
    """        to: 使用popo帐号的前缀.
    """
    if not to:
        return
    if "@" in to:
        to = to.split("@")[0]

    payload = {
        "receiver": to,
        "msg": msg
    }
    try:
        r = requests.post(POPO_URL, payload)
        if r.text != "OK":
            print(">POPO Msg Send Failed: %s"%str(r.text))
    except Exception as e:
        print(">POPO Msg Send Error: %s"%str(e))

def sendReport(files):
    with open("%s/%s" % (HTML_PATH, RESULT_MAIL), 'r', encoding='utf-8') as fp:
        EmailContent = fp.read()
    starTime = int(time.time())
    start, end = getWhichDayStr(WHICH_DAY)
    fp.close()
    if EmailContent!="":
        subject = MAIL_TITLE + start + " ~ " + end
        sendMailToUser(RECV_USER, subject, EmailContent, files)

def getWhichDayStr(whichDay):
    """
    :function: 获取当周 周X八点的时间戳和七天前的时间戳
    :param whichDay: 周几
    """
    dayTime = datetime.date.today()-datetime.timedelta(days=datetime.date.today().weekday()-(whichDay-1))
    targetTime = str(dayTime) + "-08-00-00"
    tgtTimeArray = time.strptime(targetTime, "%Y-%m-%d-%H-%M-%S")
    tgtTimeStamp = int(time.mktime(tgtTimeArray))
    start = time.strftime(TIME_FORMAT, time.localtime(tgtTimeStamp-DELTA_TIME))
    end = time.strftime(TIME_FORMAT, time.localtime(tgtTimeStamp))
    return start, end

if __name__ == "__main__":
    aa = IMG_PATH + '/' + '1698894505_1698896080_abnormal_zh'
    files = makeNewEmailPage(aa,150)
    # sendReport(files)

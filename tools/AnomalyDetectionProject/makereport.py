import os
import requests
from jinja2 import Template
import time
import datetime
import sys
import cv2
from PIL import Image
import glob
import utils
import numpy as np

# send msg
HELP_USER_NAME = "wangxin7"
MAIL_URL = "http://qa.leihuo.netease.com/webservice/mail/send"
POPO_URL = "http://qa.leihuo.netease.com:3316/popo_qatool"
RECV_USER = "wuao02@corp.netease.com,zhangjing32@corp.netease.com,wb.huokunsong01@mesg.corp.netease.com,limengxue04@corp.netease.com,wb.mashiyao01@mesg.corp.netease.com,pangumqa.pm02@list.nie.netease.com"
RECV_USER_TEST = "wangxin7@corp.netease.com"
MAIL_TITLE = "[天谕手游][时装对比][TEST] "
RESULT_MAIL = "resultMail.html"
RESULT_IMG = "resultImg.jpg"
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
HTML_PATH = "%s\\template"%BASE_PATH
IMG_PATH = utils.DIR_PATH_RESULT
TIME_FORMAT = "%Y%m%d%H%M%S"
WHICH_DAY = 4
DELTA_TIME = 7*24*3600

# send msg home
RECV_USER_HOME = "zhangjing32@corp.netease.com,wb.huokunsong01@mesg.corp.netease.com,limengxue04@corp.netease.com,wb.mashiyao01@mesg.corp.netease.com,pangumqa.pm02@list.nie.netease.com"
MAIL_TITLE_HOME = "[天谕手游][家园资源][TEST] "
RESULT_MAIL_HOME = "resultHomeMail.html"
RESULT_IMG_HOME = "resultHomeImg.jpg"
IMG_PATH_HOME = utils.HOME_DIR_PATH_RESULT

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
            <p>本周次共测试时装数量{{ total_count }}个，需二次确认时装{{ num }}个，包含新增时装{{ add_count }}个：</p>
            <ul>
              {% for filename in id_list %}
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

template_home_str = '''
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
                >本周家园资源对比统计</a
              >
            </div>
          </div>
        <div>
            <p>本周次共家园资源数量{{ total_count }}个，需二次确认资源{{ num }}个，包含新增资源{{ add_count }}个：</p>
            <ul>
              {% for filename in id_list %}
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

def cleaningUpResult():
    # 清除之前的压缩图片
    pattern = os.path.join(HTML_PATH, 'compressed_result_img_*.jpg')
    # 查找匹配的文件路径
    file_paths = glob.glob(pattern)
    # 删除每个匹配的文件
    for file_path in file_paths:
        os.remove(file_path)

def compressImage(result_img_path):
    # 压缩图片
    quality = 85
    img = Image.open(result_img_path)
    width, height = img.size
    new_width, new_height = width, height
    compress_cid = os.path.splitext(result_img_path)[0]
    # 进入循环，不断尝试不同的压缩参数，直到压缩后的文件大小不大于1MB或者达到最大循环次数
    max_iterations = 10
    iteration = 0
    while iteration < max_iterations:
        iteration += 1

        # 压缩图片
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        compressed_img_path = os.path.join(HTML_PATH, f'compressed_result_img_{quality}_{new_width}x{new_height}.jpg')
        compress_cid = f'compressed_result_img_{quality}_{new_width}x{new_height}'
        img.save(compressed_img_path, optimize=True, quality=quality)

        # 检查文件大小
        file_size = os.path.getsize(compressed_img_path)
        if file_size <= 1000000:
            return compressed_img_path, quality, compress_cid

        # 调整压缩参数
        if quality > 50:
            quality -= 5
        else:
            new_width = int(new_width * 0.9)
            new_height = int(new_height * 0.9)

    # 如果循环结束仍然没有找到合适的压缩参数，则返回最小的压缩图片
    return compressed_img_path, quality, compress_cid


def makeNewEmailPage(image_paths_list, total_count):
    files = {}
    id_list = []
    cid_list = []
    add_count = 0
    image_paths_list = list(image_paths_list)
    # 拼接图片
    images = []
    max_width = 0
    max_height = 0
    # 遍历图像路径列表
    for image_path in image_paths_list:
        image_folder_path = os.path.join(IMG_PATH, image_path)
        if image_path.split('_')[2] == 'add':
            add_count += len(os.listdir(image_folder_path))
        for filename in os.listdir(image_folder_path):
            id = os.path.splitext(filename)[0]
            id_list.append(id)
            img_path = os.path.join(image_folder_path, filename)
            img = cv2.imread(img_path)
            height, width, _ = img.shape
            max_width = max(max_width, width)
            max_height = max(max_height, height)
            images.append(img)
    # 合并图像
    merged_images = []
    black_image = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    for img in images:
        height, width, _ = img.shape
        if height < max_height or width < max_width:
            # 将较小的图像部分补充为纯黑图像
            padded_img = np.copy(black_image)
            padded_img[:height, :width] = img
            merged_images.append(padded_img)
        else:
            merged_images.append(img)

    # 合并图像
    result_img = cv2.vconcat(merged_images)

    # 保存图像
    result_img_path = os.path.join(HTML_PATH, RESULT_IMG)
    cv2.imwrite(result_img_path, result_img)

    # 压缩图片
    cleaningUpResult() # 清除之前的压缩图片
    compressed_img_path, quality, compress_cid = compressImage(result_img_path)
    print(f"压缩图片:{compressed_img_path}, 质量:{quality}, cid:{compress_cid}")

    # 创建邮件
    cid = compress_cid
    cid_list.append(cid)
    with open(compressed_img_path, "rb") as f:
        files[RESULT_IMG] = (RESULT_IMG, f.read(), "image/jpeg", {"Content-ID": cid})

    template = Template(template_str)
    mailContent = template.render(cid_list=cid_list, id_list=id_list,total_count=total_count, num=len(id_list),add_count=add_count)

    resultMailPath = os.path.join(HTML_PATH, RESULT_MAIL)
    with open(resultMailPath, "w", encoding='utf-8') as f:
        f.write(mailContent)

    return files


def makeNewEmailPageHome(image_paths_list, total_count):
    files = {}
    id_list = []
    cid_list = []
    add_count = 0
    image_paths_list = list(image_paths_list)
    # 拼接图片
    images = []
    max_width = 0
    max_height = 0
    # 遍历图像路径列表
    for image_path in image_paths_list:
        image_folder_path = os.path.join(IMG_PATH_HOME, image_path)
        if image_path.split('_')[2] == 'add':
            add_count += len(os.listdir(image_folder_path))
        for filename in os.listdir(image_folder_path):
            id = os.path.splitext(filename)[0]
            id_list.append(id)
            img_path = os.path.join(image_folder_path, filename)
            img = cv2.imread(img_path)
            height, width, _ = img.shape
            max_width = max(max_width, width)
            max_height = max(max_height, height)
            images.append(img)
    # 合并图像
    merged_images = []
    black_image = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    for img in images:
        height, width, _ = img.shape
        if height < max_height or width < max_width:
            # 将较小的图像部分补充为纯黑图像
            padded_img = np.copy(black_image)
            padded_img[:height, :width] = img
            merged_images.append(padded_img)
        else:
            merged_images.append(img)

    # 合并图像
    result_img = cv2.vconcat(merged_images)

    # 保存图像
    result_img_path = os.path.join(HTML_PATH, RESULT_IMG_HOME)
    cv2.imwrite(result_img_path, result_img)

    # 压缩图片
    cleaningUpResult() # 清除之前的压缩图片
    compressed_img_path, quality, compress_cid = compressImage(result_img_path)
    print(f"压缩图片:{compressed_img_path}, 质量:{quality}, cid:{compress_cid}")

    # 创建邮件
    cid = compress_cid
    cid_list.append(cid)
    with open(compressed_img_path, "rb") as f:
        files[RESULT_IMG_HOME] = (RESULT_IMG_HOME, f.read(), "image/jpeg", {"Content-ID": cid})

    template = Template(template_home_str)
    mailContent = template.render(cid_list=cid_list, id_list=id_list,total_count=total_count, num=len(id_list), add_count=add_count)

    resultMailPath = os.path.join(HTML_PATH, RESULT_MAIL_HOME)
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
            msg = "[时装对比][Error] Send Mail Failed"
            sendPopoMsg(HELP_USER_NAME, msg)
    except Exception as e:
        print(">Send Mail Error: %s"%str(e))
        msg = "[时装对比][Error] Send Mail Error:\r%s"%str(e)
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

def sendReport(files,testmode):
    with open("%s/%s" % (HTML_PATH, RESULT_MAIL), 'r', encoding='utf-8') as fp:
        EmailContent = fp.read()
    starTime = int(time.time())
    start, end = getWhichDayStr(WHICH_DAY)
    fp.close()
    if EmailContent!="":
        subject = MAIL_TITLE + start + " ~ " + end
        if testmode == 1:
          sendMailToUser(RECV_USER_TEST, subject, EmailContent, files)
        elif testmode == 0:
          sendMailToUser(RECV_USER, subject, EmailContent, files)

def sendReportHome(files,testmode):
    with open("%s/%s" % (HTML_PATH, RESULT_MAIL_HOME), 'r', encoding='utf-8') as fp:
        EmailContent = fp.read()
    starTime = int(time.time())
    start, end = getWhichDayStr(WHICH_DAY)
    fp.close()
    if EmailContent!="":
        subject = MAIL_TITLE_HOME + start + " ~ " + end
        if testmode == 1:
          sendMailToUser(RECV_USER_TEST, subject, EmailContent, files)
        elif testmode == 0:
          sendMailToUser(RECV_USER_HOME, subject, EmailContent, files)

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
  file_list = eval(sys.argv[1])
  count = int(sys.argv[2])
  testmode = int(sys.argv[3]) # 0: 正式模式,1: 测试模式
  reportmode = int(sys.argv[4]) # 0: 发时装邮件,1: 发家园邮件
  if reportmode == 0:
    files = makeNewEmailPage(file_list,count)
    sendReport(files,testmode)
  elif reportmode == 1:
    files = makeNewEmailPageHome(file_list,count)
    sendReportHome(files,testmode)

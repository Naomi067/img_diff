"""
filename: makereport.py
author: Xin Wang<wangxin7@corp.netease.com>
description: 用来调用接口发对比报告邮件
"""
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
import shutil

# 基本配置
HELP_USER_NAME = "wangxin7"
MAIL_URL = "http://qa.leihuo.netease.com/webservice/mail/send"
POPO_URL = "http://qa.leihuo.netease.com:3316/popo_qatool"
RECV_USER_TEST = "wangxin7@corp.netease.com"
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
TIME_FORMAT = "%Y%m%d%H%M%S"
WHICH_DAY = 4
DELTA_TIME = 7*24*3600
OLD_RESULT = "%s\\template\\oldresult"%BASE_PATH
# 时装对比邮件基本配置
RECV_USER = "wuao02@corp.netease.com,zhangjing32@corp.netease.com,wb.huokunsong01@mesg.corp.netease.com,limengxue04@corp.netease.com,wb.mashiyao01@mesg.corp.netease.com,pangumqa.pm02@list.nie.netease.com"
MAIL_TITLE = "[天谕手游][时装对比] "
RESULT_MAIL = "resultMail.html"
RESULT_IMG = "resultImg.jpg"
HTML_PATH = "%s\\template"%BASE_PATH
# 家园对比邮件的基本配置
RECV_USER_HOME = "zhangwei35@corp.netease.com,huangbingjun@corp.netease.com,fufan@corp.netease.com,pangumqa.pm02@list.nie.netease.com"
MAIL_TITLE_HOME = "[天谕手游][家园资源对比] "
RESULT_MAIL_HOME = "resultHomeMail.html"
RESULT_IMG_HOME = "resultHomeImg.jpg"
# D21对比邮件的基本配置
RECV_USER_D21 = "ty-qy@list.nie.netease.com,hzjiangwenchen@corp.netease.com,wb.lrr@mesg.corp.netease.com,gaojing04@corp.netease.com"
RECV_USER_D21_CC = "ty-qa@list.nie.netease.com,qianzepeng@corp.netease.com"
RECV_USER_TEST_D21 = "qianzepeng@corp.netease.com, wangxin7@corp.netease.com"
MAIL_TITLE_D21 = "[天谕端游][时装exe对比] "
RESULT_MAIL_D21 = "resultD21Mail.html"
RESULT_IMG_D21 = "resultD21Img.jpg"
ORI_IMG_D21 = "oriD21Img.jpg"
EXE_NUM = 5
# 时装对比邮件模板html
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
# 家园对比邮件模板html
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
# D21对比邮件模板html
template_D21_str = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>天谕端游</title>
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
                >本周D21EXE时装对比统计</a
              >
            </div>
          </div>
        <div>
            <p>本周次对比时装数量{{ total_count }}个：</p>
            <ul>
              {% for filename in id_list %}
              <li>{{ filename }}</li>
              {% endfor %}
            </ul>
          </div>
          <img src="cid:{{ cid_list[0] }}" style="max-width: 100%;">
          <p>原始图片如下：</p>
          <img src="cid:{{ cid_list[1] }}" style="max-width: 100%;">
        </div>
      </div>
    </div>
  </body>
</html>
'''

def cleaningUpResult():
    # 清除之前的压缩图片
    pattern = os.path.join(HTML_PATH, '*_compressed_result_img_*.jpg')
    # 查找匹配的文件路径
    file_paths = glob.glob(pattern)
    # 删除每个匹配的文件
    for file_path in file_paths:
        os.remove(file_path)

def compressImage(result_img_path, name):
    # 压缩图片
    name = name.split(".")[0]
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
        compressed_img_path = os.path.join(HTML_PATH, f'{name}_compressed_result_img_{quality}_{new_width}x{new_height}.jpg')
        compress_cid = f'{name}_compressed_result_img_{quality}_{new_width}x{new_height}'
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

def imageResultValid(image_path):
    if not os.path.exists(image_path):
        print("Error: The image file does not exist.")
        return False
    try:
        img = Image.open(image_path)  # 尝试打开图像文件
        img.verify()  # 验证图像文件
        return True
    except (IOError, SyntaxError) as e:
        print("Error: The image file appears to be corrupted.")
        return False

def renameAndSaveOldImage(image_path):
    # 每次生成新的结果图时，把旧的结果存到old_image_path
    if imageResultValid(image_path):
      image_date = datetime.datetime.fromtimestamp(os.path.getctime(image_path)).strftime("%Y-%m-%d")
      (path, filename) = os.path.split(image_path)
      image_name = os.path.splitext(filename)[0]
      old_image_name = f"{image_date}_{image_name}"+'.jpg'
      old_image_path = os.path.join(OLD_RESULT, old_image_name)
      # 重命名并移动旧图片
      shutil.move(image_path, old_image_path)

def stitchResultImages(mode,image_paths_list):
    # 拼接图片
    images = []
    id_list = []
    max_width = 0
    max_height = 0
    add_count = 0
    # 遍历图像路径列表
    for image_path in image_paths_list:
        path = utils.getResultPathByMode(mode)
        image_folder_path = os.path.join(path, image_path)
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
            padded_img[:height, max_width-width:max_width] = img
            merged_images.append(padded_img)
        else:
            merged_images.append(img)
    # 合并图像
    result_img = cv2.vconcat(merged_images)
    return result_img, id_list, add_count

def makeNewEmailPage(image_paths_list, total_count):
    # 时装对比创建邮件文件
    files = {}
    cid_list = []
    image_paths_list = list(image_paths_list)
    # 拼接图片
    result_img, id_list, add_count = stitchResultImages(utils.Mode.FASHION, image_paths_list)
    # 保存图像
    result_img_path = os.path.join(HTML_PATH, RESULT_IMG)
    renameAndSaveOldImage(result_img_path)
    cv2.imwrite(result_img_path, result_img)
    # 压缩图片
    cleaningUpResult() # 清除之前的压缩图片
    compressed_img_path, quality, compress_cid = compressImage(result_img_path, RESULT_IMG)
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
    # 家园对比创建邮件文件
    files = {}
    cid_list = []
    image_paths_list = list(image_paths_list)
    # 拼接图片
    result_img, id_list, add_count = stitchResultImages(utils.Mode.HOME,image_paths_list)
    # 保存图像
    result_img_path = os.path.join(HTML_PATH, RESULT_IMG_HOME)
    renameAndSaveOldImage(result_img_path)
    cv2.imwrite(result_img_path, result_img)
    # 压缩图片
    cleaningUpResult() # 清除之前的压缩图片
    compressed_img_path, quality, compress_cid = compressImage(result_img_path, RESULT_IMG_HOME)
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

def stitchResultImagesD21(mode,image_paths_list):
    # D21需要拼接同周6个版本的结果图
    # 存储不同类型的图片
    image_dict = {}
    exe_dict = {}
    ori_image_paths = image_paths_list[-1]
    image_paths_list = image_paths_list[:-1]
    for folder in image_paths_list:
      path = utils.getResultPathByMode(mode)
      image_folder_path = os.path.join(path, folder)
      for root, dirs, files in os.walk(image_folder_path):
          for file in files:
              if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                  id, tick = file.split('_')
                  if id not in image_dict:
                      image_dict[id] = []
                      exe_dict[id] = []
                  image_dict[id].append(cv2.imread(os.path.join(root, file)))
                  exe_dict[id].append(root.split('\\')[-1])
    # 处理初始图片因为他的路径不一样
    for id, images in image_dict.items():
        path = utils.getPathByMode(mode)
        ori_image = os.path.join(path, ori_image_paths)
        ori_image = os.path.join(ori_image,id)
        for root, dirs, files in os.walk(ori_image):
            for file in files:
              if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                  images.insert(0,cv2.imread(os.path.join(root, file)))
                  exe_dict[id].insert(0,root.split('\\')[-2])
    # 将所有ID的图片拼接成一张大图
    all_images = []
    for id, images in image_dict.items():
        watermarked_images = [addTextWatermark(images[i], utils.getD21ExeType(exe_dict[id][i])) for i in range(0,len(images))]
        all_images.extend(watermarked_images)

    rows = len(image_dict)  # 行数为ID的数量
    cols = EXE_NUM  # 列数
    max_images = rows * cols
    all_images = all_images[:max_images]  # 只取前(rows*cols)张图片
    while len(all_images) < max_images:  # 如果图片数量不足，用空白图片填充
        all_images.append(np.zeros_like(all_images[0]))

    result = np.vstack([np.hstack(all_images[i * cols:(i + 1) * cols]) for i in range(rows)])
    return result, image_dict.keys(), len(image_dict)

def stitchOriImagesD21(mode,image_paths_list):
    # D21需要拼接同周6个版本的结果图
    # 存储不同类型的图片
    image_dict = {}
    exe_dict = {}
    ori_image_paths = image_paths_list[-1]
    image_paths_list = image_paths_list[:-1]

    for folder in image_paths_list:
      path = utils.getResultPathByMode(mode)
      path_ori = utils.getPathByMode(mode)
      image_folder_path = os.path.join(path, folder)
      folder_ori = utils.d21ResultDirToOriDir(folder)
      image_folder_path_ori = os.path.join(path_ori, folder_ori)
      # print(image_folder_path_ori)
      for root, dirs, files in os.walk(image_folder_path):
          for file in files:
              if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                  id, tick = file.split('_')
                  if id not in image_dict:
                      image_dict[id] = []
                      exe_dict[id] = []
                  image_ori = os.path.join(image_folder_path_ori, id)
                  # print(image_ori)
                  for a, dirs, b in os.walk(image_ori):
                      for c in b:
                        if c.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                          image_dict[id].append(cv2.imread(os.path.join(a, c)))
                          exe_dict[id].append(a.split('\\')[-2])
    # 处理初始图片因为他的路径不一样
    for id, images in image_dict.items():
        path = utils.getPathByMode(mode)
        ori_image = os.path.join(path, ori_image_paths)
        ori_image = os.path.join(ori_image,id)
        for root, dirs, files in os.walk(ori_image):
            for file in files:
              if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                  images.insert(0,cv2.imread(os.path.join(root, file)))
                  exe_dict[id].insert(0,root.split('\\')[-2])
    # 将所有ID的图片拼接成一张大图
    # print(image_dict.keys())
    all_images = []
    for id, images in image_dict.items():
        watermarked_images = [addTextWatermark(images[i], utils.getD21ExeType(exe_dict[id][i])) for i in range(0,len(images))]
        all_images.extend(watermarked_images)

    rows = len(image_dict)  # 行数为ID的数量
    cols = EXE_NUM  # 列数
    max_images = rows * cols
    all_images = all_images[:max_images]  # 只取前(rows*cols)张图片
    while len(all_images) < max_images:  # 如果图片数量不足，用空白图片填充
        all_images.append(np.zeros_like(all_images[0]))

    result = np.vstack([np.hstack(all_images[i * cols:(i + 1) * cols]) for i in range(rows)])
    return result, image_dict.keys(), len(image_dict)

def makeNewEmailPageD21(image_paths_list):
    # 家园对比创建邮件文件
    files = {}
    cid_list = []
    image_paths_list = list(image_paths_list)
    # 拼接图片
    result_img, id_list, add_count = stitchResultImagesD21(utils.Mode.D21,image_paths_list)
    ori_img, _, _= stitchOriImagesD21(utils.Mode.D21,image_paths_list)
    # 保存图像
    result_img_path = os.path.join(HTML_PATH, RESULT_IMG_D21)
    ori_img_path = os.path.join(HTML_PATH, ORI_IMG_D21)
    renameAndSaveOldImage(result_img_path)
    renameAndSaveOldImage(ori_img_path)
    cv2.imwrite(result_img_path, result_img)
    cv2.imwrite(ori_img_path, ori_img)
    # 压缩图片
    cleaningUpResult() # 清除之前的压缩图片
    compressed_img_path, quality, compress_cid = compressImage(result_img_path, RESULT_IMG_D21)
    print(f"压缩图片:{compressed_img_path}, 质量:{quality}, cid:{compress_cid}")
    compressed_img_path_2, quality_2, compress_cid_2 = compressImage(ori_img_path, ORI_IMG_D21)
    print(f"压缩图片:{compressed_img_path_2}, 质量:{quality_2}, cid:{compress_cid_2}")
    # 创建邮件
    cid = compress_cid
    cid_list.append(cid)
    with open(compressed_img_path, "rb") as f:
        files[RESULT_IMG_D21] = (RESULT_IMG_D21, f.read(), "image/jpeg", {"Content-ID": cid})
    cid = compress_cid_2
    cid_list.append(cid)
    with open(compressed_img_path_2, "rb") as f:
        files[ORI_IMG_D21] = (ORI_IMG_D21, f.read(), "image/jpeg", {"Content-ID": cid})
    template = Template(template_D21_str)
    mailContent = template.render(cid_list=cid_list, id_list=id_list,total_count=add_count)
    resultMailPath = os.path.join(HTML_PATH, RESULT_MAIL_D21)
    with open(resultMailPath, "w", encoding='utf-8') as f:
        f.write(mailContent)
    return files

def sendMailToUser(userName, cc, subject, content, files):
    """
        userName：发送目标。多人使用英文逗号,分隔。如没有@符号，会自动加上加@corp.netease.com后缀
        subject: 邮件主题
        content: 邮件内容。如果包含</html>标签，会以html方式来发送。否则，以plain方式来发送
    """
    payload = {
        "to": userName,
        "cc": cc,
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
          sendMailToUser(RECV_USER_TEST,RECV_USER_TEST, subject, EmailContent, files)
        elif testmode == 0:
          sendMailToUser(RECV_USER,RECV_USER_TEST, subject, EmailContent, files)

def sendReportHome(files,testmode):
    with open("%s/%s" % (HTML_PATH, RESULT_MAIL_HOME), 'r', encoding='utf-8') as fp:
        EmailContent = fp.read()
    starTime = int(time.time())
    start, end = getWhichDayStr(WHICH_DAY)
    fp.close()
    if EmailContent!="":
        subject = MAIL_TITLE_HOME + start + " ~ " + end
        if testmode == 1:
          sendMailToUser(RECV_USER_TEST,RECV_USER_TEST, subject, EmailContent, files)
        elif testmode == 0:
          sendMailToUser(RECV_USER_HOME,RECV_USER_TEST, subject, EmailContent, files)

def sendReportD21(files,testmode):
    with open("%s/%s" % (HTML_PATH, RESULT_MAIL_D21), 'r', encoding='utf-8') as fp:
        EmailContent = fp.read()
    starTime = int(time.time())
    start, end = getWhichDayStr(WHICH_DAY)
    fp.close()
    if EmailContent!="":
        subject = MAIL_TITLE_D21 + start + " ~ " + end
        if testmode == 1:
          sendMailToUser(RECV_USER_TEST_D21,RECV_USER_TEST, subject, EmailContent, files)
        elif testmode == 0:
          sendMailToUser(RECV_USER_D21,RECV_USER_D21_CC, subject, EmailContent, files)

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

def addTextWatermark(inputImage, text):
    # 获取图片尺寸
    height, width, _ = inputImage.shape

    # 计算文字位置
    textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x = (width - textsize[0]) // 2  # 文字横坐标
    text_y = textsize[1]  # 文字纵坐标

    # 添加文字水印
    outputImage = inputImage.copy()
    cv2.putText(outputImage, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return outputImage
    
if __name__ == "__main__":
  file_list = eval(sys.argv[1])
  count = int(sys.argv[2])
  testmode = int(sys.argv[3]) # 0: 正式模式,1: 测试模式
  mode = utils.Mode(int(sys.argv[4]))
  if mode == utils.Mode.FASHION:
    files = makeNewEmailPage(file_list,count)
    sendReport(files,testmode)
  elif  mode == utils.Mode.HOME:
    files = makeNewEmailPageHome(file_list,count)
    sendReportHome(files,testmode)
  elif mode == utils.Mode.D21:
    files = makeNewEmailPageD21(file_list)
    # sendReportD21(files,testmode)

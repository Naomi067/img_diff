from img_load import img_process,ImageDir
from ssim import ssimProcess
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from config import Config
import logging
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='ssim_test.log')


def single_image_diff(oriversion,tarversion,tarappname):
    # 单个图片外观对比
    imgdir = ImageDir(oriversion,tarversion,tarappname)
    imgs,data,label = img_process().load_file_img(imgdir.oriappdir)
    imgs_2,data_2,label_2 = img_process().load_file_img(imgdir.tarappdir)
    result_ssim = 0
    # ssim_align = []
    for label,img in imgs_2.items():
        for orilabel,oriimg in imgs.items():
            ssimpre = ssimProcess(oriimg,img)
            # ssimpre = ssimProcess(imgs[label], img)
            score = ssimpre.get_ssim_score()
            if score > result_ssim:
                result_ssimpre = ssimpre
                result_ssim = score
    threshimg = result_ssimpre.get_result_img()
    normalimg = result_ssimpre.get_normal_img()
    if Config.HCONCAT_IMG:
        im_h = cv2.hconcat([normalimg,threshimg])
    else:
        im_h = threshimg
    result_thresh_img = result_ssimpre.get_thresh_img()
    result_diff_img = result_ssimpre.get_diff_img()
    cv2.imwrite(imgdir.save_path + "/" + orilabel , im_h)
    cv2.imwrite(imgdir.save_path_thresh + "/" + orilabel, result_thresh_img)
    cv2.imwrite(imgdir.save_path_diff + "/" + orilabel, result_diff_img)
    print(result_ssim)

if __name__ == '__main__':
    logging.info('--------------------------------start---------------------------------------')
    oriversion = '1666170945'
    tarversion = '1666173069'
    tarappname = 'school7Headdress60001'
    single_image_diff(oriversion,tarversion,tarappname)
    logging.info('--------------------------------end---------------------------------------')
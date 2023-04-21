from img_load import img_process,ImageDir
from ssim import ssimProcess
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from config import Config
import logging
import time
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='ssim_test.log')


def single_image_diff(oriversion,tarversion,tarappname):
    # 单个图片外观对比
    imgdir = ImageDir(oriversion,tarversion)
    imgdir.get_apperance_dir(tarappname)
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
            if result_ssim > Config.SSIM_SCORE_JUDGE:
                # 当分数满足时直接break节约时间
                break
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
    result_ssim_same = result_ssimpre.get_score_classify()
    result_thresh_same = result_ssimpre.get_thresh_classify()
    return result_ssim, result_ssim_same, result_thresh_same

def version_diff(oriversion,tarversion):
    # 根据版本号批量对比
    logging.info('--version_diff start -- oriversion:'+ str(oriversion) + ' -- tarversion:' + str(tarversion))
    imgdir = ImageDir(oriversion,tarversion)
    result= dict()
    for tarappname in imgdir.eff_app_files:
        imgdir.get_apperance_dir(tarappname)
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
                if result_ssim > Config.SSIM_SCORE_JUDGE:
                    # 当分数满足时直接break节约时间
                    break
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
        result_ssim_same = result_ssimpre.get_score_classify()
        result_thresh_same = result_ssimpre.get_thresh_classify()
        logging.info(tarappname +' ssim:'+ str(result_ssim)+' ssim_same:'+ str(result_ssim_same)+' thresh_same:'+ str(result_thresh_same) )
        result.update({tarappname:{'ssim':result_ssim,'ssim_same':result_ssim_same,'thresh_same':result_thresh_same}})
    logging.info('--version_diff end -- oriversion:'+ str(oriversion) + ' -- tarversion:' + str(tarversion))
    return result

def test():
    # 测试函数 拿几个外观来测试
    logging.info('----------------------------test----start---------------------------------------')
    oriversion = '1666170945'
    tarversion = '1666173069'
    tarappnamehead = 'school7Headdress'
    tarappnamelist = []
    for i in range(60001,60006):
        tarappname = tarappnamehead + str(i)
        tarappnamelist.append(tarappname)
    normalcount =0
    normallist =[]
    abnormalcount =0
    abnormallist =[]
    abscorecount = 0
    abscorelist =[]
    abthreshcount = 0
    abthreshlist = []
    count = 0
    for i in tarappnamelist:
        result_ssim, result_ssim_same, result_thresh_same = single_image_diff(oriversion,tarversion,i)
        count += 1
        if result_ssim_same and result_thresh_same:
            normalcount += 1
            normallist.append(i)
        elif not result_ssim_same and result_thresh_same:
            abscorecount += 1
            abscorelist.append(i)
        elif result_ssim_same and not result_thresh_same:
            abthreshcount += 1
            abthreshlist.append(i)
        else:
            abnormalcount += 1
            abnormallist.append(i)
    logging.info("normalcount = {}".format(normalcount))
    logging.info(str(normallist))
    logging.info("abnormalcount = {}".format(abnormalcount))
    logging.info(str(abnormallist))
    logging.info("abscorecount = {}".format(abscorecount))
    logging.info(str(abscorelist))
    logging.info("abthreshcount = {}".format(abthreshcount))
    logging.info(str(abthreshlist))
    #sum = normalcount+abnormalcount+abscorecount+abthreshcount
    logging.info("sum = {}".format(count))
    logging.info("accuracy = {}".format(normalcount/(count)))
    logging.info('-------------------------test-------end---------------------------------------')

def diff():
    # 根据版本来批量输出结果
    logging.info('----------------------------diff----start---------------------------------------')
    oriversion = '1666170945'
    tarversion = '1666173069'
    result = version_diff(oriversion,tarversion)
    normalcount =0
    normallist =[]
    abnormalcount =0
    abnormallist =[]
    abscorecount = 0
    abscorelist =[]
    abthreshcount = 0
    abthreshlist = []
    count = 0
    for appname,info in result.items():
        count += 1
        if info['ssim_same'] and info['thresh_same']:
            normalcount += 1
            normallist.append(appname)
        elif not info['ssim_same'] and info['thresh_same']:
            abscorecount += 1
            abscorelist.append(appname)
        elif info['ssim_same'] and not info['thresh_same']:
            abthreshcount += 1
            abthreshlist.append(appname)
        else:
            abnormalcount += 1
            abnormallist.append(appname)
    logging.info("normalcount = {}".format(normalcount))
    logging.info(str(normallist))
    logging.info("abnormalcount = {}".format(abnormalcount))
    logging.info(str(abnormallist))
    logging.info("abscorecount = {}".format(abscorecount))
    logging.info(str(abscorelist))
    logging.info("abthreshcount = {}".format(abthreshcount))
    logging.info(str(abthreshlist))
    #sum = normalcount+abnormalcount+abscorecount+abthreshcount
    logging.info("sum = {}".format(count))
    logging.info("accuracy = {}".format(normalcount/(count)))
    logging.info('----------------------------diff----end---------------------------------------')

if __name__ == '__main__':
    t = time.time()
    #test()
    diff()
    print(f'coast:{time.time() - t:.4f}s')
    logging.info(f'coast:{time.time() - t:.4f}s')
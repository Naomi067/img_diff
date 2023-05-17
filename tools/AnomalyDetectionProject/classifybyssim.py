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

class ClassifyBySSIM(object):
    def __init__(self,oriversion,tarversion):
        self.oriversion = oriversion
        self.tarversion = tarversion
        self.imgdir = ImageDir(self.oriversion,self.tarversion)
        self.diff()
        self.get_all_abnormal_imgs()

    def _single_image_diff(self,tarappname):
        # 单个图片外观对比
        self.imgdir.get_apperance_dir(tarappname)
        imgs,data,label = img_process().load_file_img(self.imgdir.oriappdir,False)
        imgs_2,data_2,label_2 = img_process().load_file_img(self.imgdir.tarappdir,True)
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
        cv2.imwrite(self.imgdir.save_path + "/" + orilabel , im_h)
        cv2.imwrite(self.imgdir.save_path_thresh + "/" + orilabel, result_thresh_img)
        cv2.imwrite(self.imgdir.save_path_diff + "/" + orilabel, result_diff_img)
        print(result_ssim)
        result_ssim_same = result_ssimpre.get_score_classify()
        result_thresh_same = result_ssimpre.get_thresh_classify()
        return result_ssim, result_ssim_same, result_thresh_same

    def _version_diff(self):
        # 根据版本号批量对比
        logging.info('--version_diff start -- oriversion:'+ str(self.oriversion) + ' -- tarversion:' + str(self.tarversion))
        result= dict()
        for tarappname in self.imgdir.eff_app_files:
            self.imgdir.get_apperance_dir(tarappname)
            imgs,data,label = img_process().load_file_img(self.imgdir.oriappdir,False)
            imgs_2,data_2,label_2 = img_process().load_file_img(self.imgdir.tarappdir,True)
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
            cv2.imwrite(self.imgdir.save_path + "/" + orilabel , im_h)
            cv2.imwrite(self.imgdir.save_path_thresh + "/" + orilabel, result_thresh_img)
            cv2.imwrite(self.imgdir.save_path_diff + "/" + orilabel, result_diff_img)
            result_ssim_same = result_ssimpre.get_score_classify()
            result_thresh_same = result_ssimpre.get_thresh_classify()
            logging.info(tarappname +' ssim:'+ str(result_ssim)+' ssim_same:'+ str(result_ssim_same)+' thresh_same:'+ str(result_thresh_same) )
            result.update({tarappname:{'ssim':result_ssim,'ssim_same':result_ssim_same,'thresh_same':result_thresh_same}})
        logging.info('--version_diff end -- oriversion:'+ str(self.oriversion) + ' -- tarversion:' + str(self.tarversion))
        return result

    def test(self):
        # 测试函数 拿几个外观来测试
        logging.info('----------------------------test----start---------------------------------------')
        tarappnamehead = 'school7Headdress'
        tarappnamelist = []
        for i in range(60001,60006):
            tarappname = tarappnamehead + str(i)
            tarappnamelist.append(tarappname)
        self.normalcount =0
        self.normallist =[]
        self.abnormalcount =0
        self.abnormallist =[]
        self.abscorecount = 0
        self.abscorelist =[]
        self.abthreshcount = 0
        self.abthreshlist = []
        self.count = 0
        for i in tarappnamelist:
            result_ssim, result_ssim_same, result_thresh_same = self._single_image_diff(i)
            self.count += 1
            if result_ssim_same and result_thresh_same:
                self.normalcount += 1
                self.normallist.append(i)
            elif not result_ssim_same and result_thresh_same:
                self.abscorecount += 1
                self.abscorelist.append(i)
            elif result_ssim_same and not result_thresh_same:
                self.abthreshcount += 1
                self.abthreshlist.append(i)
            else:
                self.abnormalcount += 1
                self.abnormallist.append(i)
        logging.info("normalcount = {}".format(self.normalcount))
        logging.info(str(self.normallist))
        logging.info("abnormalcount = {}".format(self.abnormalcount))
        logging.info(str(self.abnormallist))
        logging.info("abscorecount = {}".format(self.abscorecount))
        logging.info(str(self.abscorelist))
        logging.info("abthreshcount = {}".format(self.abthreshcount))
        logging.info(str(self.abthreshlist))
        #sum = normalcount+abnormalcount+abscorecount+abthreshcount
        logging.info("sum = {}".format(self.count))
        logging.info("accuracy (both abscorecount and abthreshcount) = {}".format(self.normalcount/(self.count)))
        logging.info("accuracy = {}".format((self.count-self.abnormalcount)/(self.count)))
        logging.info('-------------------------test-------end---------------------------------------')


    def diff(self):
        # 根据版本来批量输出结果 + 准确率统计
        logging.info('----------------------------diff----start---------------------------------------')
        self.versiondiffresult = self._version_diff()
        self.normalcount =0
        self.normallist =[]
        self.abnormalcount =0
        self.abnormallist =[]
        self.abscorecount = 0
        self.abscorelist =[]
        self.abthreshcount = 0
        self.abthreshlist = []
        self.count = 0
        for appname,info in self.versiondiffresult.items():
            self.count += 1
            if info['ssim_same'] and info['thresh_same']:
                self.normalcount += 1
                self.normallist.append(appname)
            elif not info['ssim_same'] and info['thresh_same']:
                self.abscorecount += 1
                self.abscorelist.append(appname)
            elif info['ssim_same'] and not info['thresh_same']:
                self.abthreshcount += 1
                self.abthreshlist.append(appname)
            else:
                self.abnormalcount += 1
                self.abnormallist.append(appname)
        logging.info("normalcount = {}".format(self.normalcount))
        logging.info(str(self.normallist))
        logging.info("abnormalcount = {}".format(self.abnormalcount))
        logging.info(str(self.abnormallist))
        logging.info("abscorecount = {}".format(self.abscorecount))
        logging.info(str(self.abscorelist))
        logging.info("abthreshcount = {}".format(self.abthreshcount))
        logging.info(str(self.abthreshlist))
        #sum = normalcount+abnormalcount+abscorecount+abthreshcount
        logging.info("sum = {}".format(self.count))
        logging.info("deviation = {}".format(self.abnormalcount/(self.count)))
        logging.info("accuracy = {}".format((self.normalcount+self.abscorecount+self.abthreshcount)/(self.count)))
        logging.info('----------------------------diff----end---------------------------------------')

    def get_all_abnormal_imgs(self):
        logging.info('----------------------------get_all_abnormal_imgs--start---------------------------------------')
        for i in self.abnormallist:
            self.imgdir.copy_apperance_abnormal_dir(i)
        logging.info('----------------------------get_all_abnormal_imgs--end---------------------------------------')

if __name__ == '__main__':
    t = time.time()
    #test()
    oriversion = '1682585756'
    # tarversion = '1682650225'
    tarversion = '1682670398'
    result = ClassifyBySSIM(oriversion,tarversion)
    print(f'coast:{time.time() - t:.4f}s')
    logging.info(f'coast:{time.time() - t:.4f}s')
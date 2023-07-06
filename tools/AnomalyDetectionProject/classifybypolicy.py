import policy
from img_load import img_process,ImageDir,ImgToWeb
import logging
import time
import cv2
from policy.CompareHist import histProcess
from policy.PHash import pHashProcess
from policy.MatchTemplate import matchTemplateProcess
from policy.OBR import obrProcess
from policy.Cut import cutProcess
from policy.ssimThresh import ssimThreshProcess
from config import Config
import utils
import sys
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='plicy_clasify_test.log')

class ClassifyByPolicy(object):
    def __init__(self,oriversion,tarversion,policy):
        logging.info('-------------ClassifyByPolicy start-----------')
        logging.info('oriversion: '+ str(oriversion) + ' tarversion:' + str(tarversion))
        self.imgdir = ImageDir(oriversion,tarversion)
        self.policy = policy
        logging.info('policy: '+ str(policy))
        self.diff()
        logging.info('-------------ClassifyByPolicy end-----------')

    def _get_policy_process(self,oriimg,img):
        if self.policy == 'histProcess':
            return histProcess(oriimg,img)
        elif self.policy == 'ssimThreshProcess':
            return ssimThreshProcess(oriimg,img)
        elif self.policy == 'pHashProcess':
            return pHashProcess(oriimg,img)

    def _version_diff(self):
        # 根据版本号批量对比
        result= dict()
        for tarappname in self.imgdir.eff_app_files:
            self.imgdir.get_apperance_dir(tarappname)
            imgs,data,label = img_process().load_file_img(self.imgdir.oriappdir,False)
            imgs_2,data_2,label_2 = img_process().load_file_img(self.imgdir.tarappdir,True)
            # ssim_align = []
            isame = False
            for label,img in imgs_2.items():
                for orilabel,oriimg in imgs.items():
                    process = self._get_policy_process(oriimg,img)
                    if process.result == True:
                        # 当50张图片中有满足条件的则break
                        isame = True
                        break
            logging.info("app:{},policy:{},policy_result:{}".format(tarappname,self.policy,isame))
            result.update({tarappname:{self.policy:isame}})
        return result


    def diff(self):
        # 根据版本来批量输出结果 + 准确率统计
        logging.info('----------------------------diff----start---------------------------------------')
        self.versiondiffresult = self._version_diff()
        self.normalcount =0
        self.normallist =[]
        self.abnormalcount =0
        self.abnormallist =[]
        self.count = 0
        for appname,info in self.versiondiffresult.items():
            self.count += 1
            if info[self.policy]:
                self.normalcount += 1
                self.normallist.append(appname)
            else:
                self.abnormalcount += 1
                self.abnormallist.append(appname)
        logging.info("normalcount = {}".format(self.normalcount))
        logging.info(str(self.normallist))
        logging.info("abnormalcount = {}".format(self.abnormalcount))
        logging.info(str(self.abnormallist))
        logging.info("sum = {}".format(self.count))
        logging.info("deviation = {}".format(self.abnormalcount/(self.count)))
        logging.info("accuracy = {}".format((self.normalcount/self.count)))
        logging.info('----------------------------diff----end---------------------------------------')

class ClassifyByTemplate(object):
    def __init__(self,oriversion,tarversion,policy):
        logging.info('-------------ClassifyByTemplate start-----------')
        logging.info('oriversion: '+ str(oriversion) + ' tarversion:' + str(tarversion))
        self.imgdir = ImageDir(oriversion,tarversion)
        self.policy = policy
        logging.info('policy: '+ str(policy))
        self.diff()
        logging.info('-------------ClassifyByTemplate end-----------')

    def _get_temp_policy_process(self,temp,img):
        if self.policy == 'matchTemplateProcess':
            return matchTemplateProcess(temp,img)

    def _version_temp(self):
        # 根据版本号批量对比
        result= dict()
        for tarappname in self.imgdir.eff_app_files:
            self.imgdir.get_apperance_dir(tarappname)
            # imgs,data,label = img_process().load_file_img(self.imgdir.oriappdir,False)
            self.imgdir.get_app_template_file(tarappname)
            if self.imgdir.template_file != -1:
                templte = cv2.imread(self.imgdir.template_file)
                imgs_2,data_2,label_2 = img_process().load_file_img(self.imgdir.tarappdir,True)
                # ssim_align = []
                isame = False
                for label,img in imgs_2.items():
                    process = self._get_temp_policy_process(templte,img)
                    if process.result == True:
                        # 当50张图片中有满足条件的则break
                        isame = True
                        break
                logging.info("app:{},policy:{},policy_result:{}".format(tarappname,self.policy,isame))
                result.update({tarappname:{self.policy:isame}})
            else:
                logging.info("app:{},policy:{},no template!".format(tarappname,self.policy))
                # result.update({tarappname:{self.policy:isame}})
        return result

    def diff(self):
        # 根据版本来批量输出结果 + 准确率统计
        logging.info('----------------------------diff----start---------------------------------------')
        self.versiontempresult = self._version_temp()
        self.normalcount =0
        self.normallist =[]
        self.abnormalcount =0
        self.abnormallist =[]
        self.count = 0
        for appname,info in self.versiontempresult.items():
            self.count += 1
            if info[self.policy]:
                self.normalcount += 1
                self.normallist.append(appname)
            else:
                self.abnormalcount += 1
                self.abnormallist.append(appname)
        logging.info("normalcount = {}".format(self.normalcount))
        logging.info(str(self.normallist))
        logging.info("abnormalcount = {}".format(self.abnormalcount))
        logging.info(str(self.abnormallist))
        logging.info("sum = {}".format(self.count))
        logging.info("deviation = {}".format(self.abnormalcount/(self.count)))
        logging.info("accuracy = {}".format((self.normalcount/self.count)))
        logging.info('----------------------------diff----end---------------------------------------')

class Preprocessing(object):
    def __init__(self,oriversion,tarversion,policy):
        logging.info('-------------Preprocessing start-----------')
        logging.info('oriversion: '+ str(oriversion) + ' tarversion:' + str(tarversion))
        self.imgdir = ImageDir(oriversion,tarversion)
        self.policy = policy
        logging.info('policy: '+ str(policy))
        self.diff()
        logging.info('-------------Preprocessing end-----------')

    def _get_pre_policy_process(self,img,tarappname):
        if self.policy == 'obrProcess':
            return obrProcess(img)
        elif self.policy == 'cutProcess':
            return cutProcess(img,tarappname)

    def _version_temp(self):
        # 根据版本号批量对比
        result= dict()
        from img_load import img_process
        img_process = img_process()
        for tarappname in self.imgdir.eff_app_files:
            self.imgdir.get_apperance_dir(tarappname)
            img_process = img_process()
            imgs_2,data_2,label_2 = img_process.load_file_img(self.imgdir.tarappdir,True)
            iseffect = False
            for label,img in imgs_2.items():
                    process = self._get_pre_policy_process(img,tarappname)
                    if process.result == True:
                        # 当50张图片中有满足条件的则break
                        if self.policy == 'obrProcess':
                            iseffect = True
                            effect_id = label
                            break
                        if self.policy == 'cutProcess':
                            iseffect = True
            if self.policy == 'obrProcess':
                logging.info("app:{},policy:{},policy_result:{},effect_id:{}".format(tarappname,self.policy,iseffect,effect_id))
                result.update({tarappname:{self.policy:iseffect,'effect_id':effect_id}})
            if self.policy == 'cutProcess':
                logging.info("app:{},policy:{},policy_result:{}".format(tarappname,self.policy,iseffect))
                result.update({tarappname:{self.policy:iseffect}})
            # 如果是cut图片预处理需要对原始图片也进行处理
            if self.policy == 'cutProcess':
                imgs,data,label = img_process.load_file_img(self.imgdir.oriappdir,False)
                for label,img in imgs.items():
                    process = self._get_pre_policy_process(img,tarappname)
                logging.info("app:{},policy:{},origin_app_preprocessing".format(tarappname,self.policy))
        return result

    def diff(self):
        # 根据版本来批量输出结果 + 准确率统计
        # logging.info('--------------------------------start---------------------------------------')
        self.versiontempresult = self._version_temp()
        self.normalcount =0
        self.normallist =[]
        self.abnormalcount =0
        self.abnormallist =[]
        self.count = 0
        for appname,info in self.versiontempresult.items():
            self.count += 1
            if info[self.policy]:
                self.normalcount += 1
                self.normallist.append(appname)
            else:
                self.abnormalcount += 1
                self.abnormallist.append(appname)
        logging.info("no preprocessing required= {}".format(self.normalcount))
        logging.info(str(self.normallist))
        logging.info("need preprocessing = {}".format(self.abnormalcount))
        logging.info(str(self.abnormallist))
        logging.info("sum = {}".format(self.count))
        logging.info("deviation = {}".format(self.abnormalcount/(self.count)))
        logging.info("accuracy = {}".format((self.normalcount/self.count)))
        # logging.info('----------------------------diff----end---------------------------------------')

class ClassifyByPolicyWithProcessing(object):
    def __init__(self,oriversion,tarversion,policy,prepolicy):
        logging.info('-------------ClassifyByPolicyWithProcessing start-----------')
        logging.info('oriversion: '+ str(oriversion) + ' tarversion:' + str(tarversion))
        self.imgdir = ImageDir(oriversion,tarversion)
        self.imgdir.copy_apperance_add_dir()
        self.policy = policy
        self.prepolicy = prepolicy
        logging.info('policy: '+ str(policy))
        logging.info('preprocessing policy: '+ str(prepolicy))
        self.diff()
        self.imgtoweb =ImgToWeb(self.imgdir.path_abnormal)
        self.imgtoweb =ImgToWeb(self.imgdir.path_add)
        logging.info('-------------ClassifyByPolicyWithProcessing end-----------')
        
    def _get_policy_process(self,oriimg,img):
        if self.policy == 'histProcess':
            return histProcess(oriimg,img)
        elif self.policy == 'ssimThreshProcess':
            return ssimThreshProcess(oriimg,img)
        elif self.policy == 'pHashProcess':
            return pHashProcess(oriimg,img)
        
    def _get_preprocessing_policy_process(self,img,tarappname):
        if self.prepolicy == 'obrProcess':
            return obrProcess(img)
        elif self.prepolicy == 'cutProcess':
            return cutProcess(tarappname)

    def _get_preprocessing_policy_process_by_tarappname(self,tarappname):
        if utils.isClipped(tarappname):
            self.prepolicy = 'cutProcess'
        else:
            self.prepolicy = 'obrProcess'

    def _version_diff(self):
        # 根据版本号批量对比
        result= dict()
        from img_load import img_process
        img_process = img_process()
        for tarappname in self.imgdir.eff_app_files:
            self.imgdir.get_apperance_dir(tarappname)
            imgs,data,label = img_process.load_file_img(self.imgdir.oriappdir,False)
            imgs_2,data_2,label_2 = img_process.load_file_img(self.imgdir.tarappdir,True)
            self._get_preprocessing_policy_process_by_tarappname(tarappname)
            if self.prepolicy == 'obrProcess':
                count = 0
                while(True):
                    img = imgs_2[list(imgs_2.keys())[0]]
                    preprocess = self._get_preprocessing_policy_process(img, tarappname)
                    count += 1
                    if preprocess.result == True:
                        break
                    elif count >= 50:
                        break
                    imgs_2,data_2,label_2 = img_process.reload_file_img(self.imgdir.tarappdir,True)
            isame = False
            for label,img in imgs_2.items():
                if self.prepolicy == 'cutProcess':
                    preprocess = self._get_preprocessing_policy_process(img, tarappname)
                    img = preprocess.get_cut_imgs(img)
                save_tar = img
                most_like_score = 1000000
                for orilabel,oriimg in imgs.items():
                    if self.prepolicy == 'cutProcess':
                        preprocess = self._get_preprocessing_policy_process(img, tarappname)
                        oriimg = preprocess.get_cut_imgs(oriimg)
                    process = self._get_policy_process(oriimg,img)
                    if process.score < most_like_score:
                        save_ori_label, save_ori = orilabel,oriimg
                        most_like_score = process.score
                    if process.result == True:
                        # 当50张图片中有满足条件的则break
                        isame = True
                        break
            if isame == False:
                if  save_ori.any() and save_tar.any():
                    self.imgdir.get_apperance_dir_save(tarappname)
                    self.obnormal_processing(save_ori,save_tar,save_ori_label)
                    self.imgdir.copy_apperance_abnormal_dir(tarappname)
            logging.info("app:{},policy:{},policy_result:{}".format(tarappname,self.policy,isame))
            result.update({tarappname:{self.policy:isame}})
        return result

    def obnormal_processing(self,ori,tar,orilabel):
        # 这里写下生成异常图片的阈值画框图片 + 对比图片的拼接图
        # 注意这里要是预处理之后的图片
        ssimpre = ssimThreshProcess(ori,tar) # 这里面还有很多可以用的参数和算法，包括tresh画框数量计算，sift修正等等
        score = ssimpre.get_ssim_score()
        logging.info("obnormal_processing ssim_core:{}".format(score))
        threshimg = ssimpre.get_result_img()
        normalimg = ssimpre.get_normal_img()
        if Config.HCONCAT_IMG:
            im_h = cv2.hconcat([normalimg,threshimg])
        else:
            im_h = threshimg
        result_thresh_img = ssimpre.get_thresh_img()
        result_diff_img = ssimpre.get_diff_img()
        cv2.imwrite(self.imgdir.save_path + "/" + orilabel , im_h)
        cv2.imwrite(self.imgdir.save_path_thresh + "/" + orilabel, result_thresh_img)
        cv2.imwrite(self.imgdir.save_path_diff + "/" + orilabel, result_diff_img)
        logging.info("obnormal_processing img save.")
        

    def diff(self):
        # 根据版本来批量输出结果 + 准确率统计
        logging.info('----------------------------diff----start---------------------------------------')
        self.versiondiffresult = self._version_diff()
        self.normalcount =0
        self.normallist =[]
        self.abnormalcount =0
        self.abnormallist =[]
        self.count = 0
        for appname,info in self.versiondiffresult.items():
            self.count += 1
            if info[self.policy]:
                self.normalcount += 1
                self.normallist.append(appname)
            else:
                self.abnormalcount += 1
                self.abnormallist.append(appname)
        logging.info("normalcount = {}".format(self.normalcount))
        logging.info(str(self.normallist))
        logging.info("abnormalcount = {}".format(self.abnormalcount))
        logging.info(str(self.abnormallist))
        logging.info("sum = {}".format(self.count))
        logging.info("deviation = {}".format(self.abnormalcount/(self.count)))
        logging.info("accuracy = {}".format((self.normalcount/self.count)))
        logging.info('----------------------------diff----end---------------------------------------')


if __name__ == '__main__':
    t = time.time()
    #test()
    oriversion = str(sys.argv[1])
    timeArray_ori = time.localtime(int(oriversion))
    otherStyleTime_ori = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_ori)
    # oriversion = '1682585756'
    # tarversion = '1682670398'
    # tarversion = '1682670399'
    tarversion = str(sys.argv[2])
    timeArray_tar = time.localtime(int(tarversion))
    otherStyleTime_tar = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_tar)
    print("compare file timestamps:\nori:{},times:{}\ntar:{},times:{}".format(oriversion,otherStyleTime_ori,tarversion,otherStyleTime_tar))
    if utils.isLegalVersion(oriversion) and utils.isLegalVersion(tarversion) and utils.isComparableVersions(oriversion,tarversion):
        # result = ClassifyByPolicy(oriversion,tarversion,'histProcess')
        # result = ClassifyByPolicy(oriversion,tarversion,'pHashProcess')
        # result = ClassifyByTemplate(oriversion,tarversion,'matchTemplateProcess')
        # result = Preprocessing(oriversion,tarversion,'obrProcess')
        # result = Preprocessing(oriversion,tarversion,'cutProcess')
        result = ClassifyByPolicyWithProcessing(oriversion,tarversion,'histProcess','cutProcess')
        print(f'coast:{time.time() - t:.4f}s')
        logging.info(f'coast:{time.time() - t:.4f}s')
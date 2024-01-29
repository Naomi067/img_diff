import sys
sys.path.append('..')
import os
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
import json
import utils
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='plicy_clasify_test.log')

# 主要类-批量预处理+分类
class ClassifyByMultiPolicyWithProcessing(object):
    def __init__(self,oriversion,tarversion,policy,prepolicy,mode):
        logging.info('-------------ClassifyByMultiPolicyWithProcessing start-----------')
        logging.info('oriversion: '+ str(oriversion) + ' tarversion:' + str(tarversion))
        self.mode = mode
        self.imgdir = ImageDir(oriversion,tarversion,utils.getPathByMode(mode)) # 图片路径处理等
        self.imgdir.copy_apperance_add_dir()
        self.policy = policy # 分类策略是个set,可以是多种
        self.prepolicy = prepolicy # 这里其实没多大用处了主要是由_get_preprocessing_policy_process_by_tarappname来决定如何预处理
        logging.info('policy: '+ str(policy))
        logging.info('preprocessing policy: '+ str(prepolicy))
        self.diff() # 主要函数
        self.imgtoweb =ImgToWeb(self.imgdir.path_abnormal) # 上传至web后台打包
        self.imgtoweb =ImgToWeb(self.imgdir.path_add)
        logging.info('-------------ClassifyByMultiPolicyWithProcessing end-----------')
        
    def _get_policy_process(self, oriimg, img):
        processRsult = []
        for policy in self.policy:
            if policy == 'histProcess':
                processRsult.append(histProcess(oriimg, img))
            elif policy == 'ssimThreshProcess':
                processRsult.append(ssimThreshProcess(oriimg, img, self.mode))
            elif policy == 'pHashProcess':
                processRsult.append(pHashProcess(oriimg, img))
        return processRsult
        
    def _get_preprocessing_policy_process(self,img,tarappname):
        if self.prepolicy == 'obrProcess':
            return obrProcess(img)
        elif self.prepolicy == 'cutProcess':
            return cutProcess(tarappname)

    def _get_preprocessing_policy_process_by_tarappname(self,tarappname):
        # 时装模式根据外观名称来决定预处理方法
        if self.mode == utils.Mode.FASHION:
            if utils.isClipped(tarappname):
                self.prepolicy = 'cutProcess'
            else:
                self.prepolicy = 'obrProcess'

    def _version_diff(self):
        # 根据版本号批量对比
        result= dict()
        scores = dict()
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
                    img = preprocess.get_cut_imgs(img,self.mode)
                save_tar = img
                most_like_score = utils.getMostLikelyScore(self.policy) # 这个是用来计算最相近的图片分数 初始值需要按照policy来给
                for orilabel,oriimg in imgs.items():
                    if self.prepolicy == 'cutProcess':
                        preprocess = self._get_preprocessing_policy_process(img, tarappname)
                        oriimg = preprocess.get_cut_imgs(oriimg,self.mode)
                    processList = self._get_policy_process(oriimg,img)
                    scoreList = [i.score for i in processList]
                    resultList = [i.result for i in processList]
                    if utils.compare(scoreList, most_like_score):
                        save_ori_label, save_ori = orilabel,oriimg
                        most_like_score = scoreList
                        scores.update({tarappname:{str(self.policy):str(most_like_score)}})
                    if  all(resultList):
                        # 当50张图片中有满足条件的则break
                        isame = True
                        break
            if isame == False or self.mode == utils.Mode.D21:
                if  save_ori.any() and save_tar.any():
                    self.imgdir.get_apperance_dir_save(tarappname)
                    isame = self.obnormal_processing(save_ori,save_tar,save_ori_label,tarappname)
                    # self.imgdir.copy_apperance_abnormal_dir(tarappname)
            logging.info("app:{},policy:{},policy_result:{}".format(tarappname,str(self.policy),isame))
            result.update({tarappname:{str(self.policy):isame}})
        json_str = json.dumps(scores)
        with open(self.imgdir.json_file_name, 'w') as f:
            f.write(json_str)
        return result

    def obnormal_processing(self,ori,tar,orilabel,tarappname):
        # 这里写下生成异常图片的阈值画框图片 + 对比图片的拼接图
        # 注意这里要是预处理之后的图片
        ssimpre = ssimThreshProcess(ori,tar,self.mode) # 这里面还有很多可以用的参数和算法，包括tresh画框数量计算，sift修正等等
        score = ssimpre.get_ssim_score()
        logging.info("obnormal_processing ssim_core:{}".format(score))
        threshimg = ssimpre.get_result_img()
        normalimg = ssimpre.get_normal_img()
        im_h = utils.hconcatImg(self.mode,normalimg,threshimg)
        result_thresh_img = ssimpre.get_thresh_img()
        result_diff_img = ssimpre.get_diff_img()
        if ssimpre.result == False or self.mode == utils.Mode.D21:
            # 这里再ssim修正一下
            # D21模式还是要存图的，因为量较少且需要正常版本也要输出结果
            cv2.imwrite(self.imgdir.save_path + "/" + orilabel , im_h)
            cv2.imwrite(self.imgdir.save_path_thresh + "/" + orilabel, result_thresh_img)
            cv2.imwrite(self.imgdir.save_path_diff + "/" + orilabel, result_diff_img)
            logging.info("obnormal_processing img save.")
            self.imgdir.copy_apperance_abnormal_dir(tarappname)
        return ssimpre.result

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
            if info[str(self.policy)]:
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
    oriversion = str(os.getenv('oriversion'))
    tarversion = str(os.getenv('tarversion'))
    mode = utils.Mode(os.getenv('tarversion'))
    timeArray_ori = time.localtime(utils.extractTimestamp(oriversion))
    otherStyleTime_ori = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_ori)
    timeArray_tar = time.localtime(utils.extractTimestamp(tarversion))
    otherStyleTime_tar = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_tar)
    print("MODE:{}:\ncompare file timestamps:\nori:{},times:{}\ntar:{},times:{}".format(mode,oriversion,otherStyleTime_ori,tarversion,otherStyleTime_tar))
    if utils.isLegalVersion(oriversion,mode) and utils.isLegalVersion(tarversion,mode) and utils.isComparableVersions(oriversion,tarversion,mode):
        mypolicy,myprepolicy = utils.getPolicy(mode)
        result = ClassifyByMultiPolicyWithProcessing(oriversion,tarversion,mypolicy,myprepolicy,mode)
        print(f'coast:{time.time() - t:.4f}s')
        logging.info(f'coast:{time.time() - t:.4f}s')
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
import sys
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='policy_test.log') # 全部接到jekins之后这部分可以不要了 全部换成print

# # 不带预处理的图片对比检测
# class ClassifyByPolicy(object):
#     def __init__(self,oriversion,tarversion,policy):
#         print('-------------ClassifyByPolicy start-----------')
#         print('oriversion: '+ str(oriversion) + ' tarversion:' + str(tarversion))
#         self.imgdir = ImageDir(oriversion,tarversion)
#         self.policy = policy
#         print('policy: '+ str(policy))
#         self.diff()
#         print('-------------ClassifyByPolicy end-----------')

#     def _get_policy_process(self,oriimg,img):
#         if self.policy == 'histProcess':
#             return histProcess(oriimg,img)
#         elif self.policy == 'ssimThreshProcess':
#             return ssimThreshProcess(oriimg,img)
#         elif self.policy == 'pHashProcess':
#             return pHashProcess(oriimg,img)

#     def _version_diff(self):
#         # 根据版本号批量对比
#         result= dict()
#         for tarappname in self.imgdir.eff_app_files:
#             self.imgdir.get_apperance_dir(tarappname)
#             imgs,data,label = img_process().load_file_img(self.imgdir.oriappdir,False)
#             imgs_2,data_2,label_2 = img_process().load_file_img(self.imgdir.tarappdir,True)
#             # ssim_align = []
#             isame = False
#             for label,img in imgs_2.items():
#                 for orilabel,oriimg in imgs.items():
#                     process = self._get_policy_process(oriimg,img)
#                     if process.result == True:
#                         # 当50张图片中有满足条件的则break
#                         isame = True
#                         break
#             print("app:{},policy:{},policy_result:{}".format(tarappname,self.policy,isame))
#             result.update({tarappname:{self.policy:isame}})
#         return result


#     def diff(self):
#         # 根据版本来批量输出结果 + 准确率统计
#         print('----------------------------diff----start---------------------------------------')
#         self.versiondiffresult = self._version_diff()
#         self.normalcount =0
#         self.normallist =[]
#         self.abnormalcount =0
#         self.abnormallist =[]
#         self.count = 0
#         for appname,info in self.versiondiffresult.items():
#             self.count += 1
#             if info[self.policy]:
#                 self.normalcount += 1
#                 self.normallist.append(appname)
#             else:
#                 self.abnormalcount += 1
#                 self.abnormallist.append(appname)
#         print("normalcount = {}".format(self.normalcount))
#         print(str(self.normallist))
#         print("abnormalcount = {}".format(self.abnormalcount))
#         print(str(self.abnormallist))
#         print("sum = {}".format(self.count))
#         print("deviation = {}".format(self.abnormalcount/(self.count)))
#         print("accuracy = {}".format((self.normalcount/self.count)))
#         print('----------------------------diff----end---------------------------------------')

# # 批量模板匹配测试代码
# class ClassifyByTemplate(object):
#     def __init__(self,oriversion,tarversion,policy):
#         print('-------------ClassifyByTemplate start-----------')
#         print('oriversion: '+ str(oriversion) + ' tarversion:' + str(tarversion))
#         self.imgdir = ImageDir(oriversion,tarversion)
#         self.policy = policy
#         print('policy: '+ str(policy))
#         self.diff()
#         print('-------------ClassifyByTemplate end-----------')

#     def _get_temp_policy_process(self,temp,img):
#         if self.policy == 'matchTemplateProcess':
#             return matchTemplateProcess(temp,img)

#     def _version_temp(self):
#         # 根据版本号批量对比
#         result= dict()
#         for tarappname in self.imgdir.eff_app_files:
#             self.imgdir.get_apperance_dir(tarappname)
#             # imgs,data,label = img_process().load_file_img(self.imgdir.oriappdir,False)
#             self.imgdir.get_app_template_file(tarappname)
#             if self.imgdir.template_file != -1:
#                 templte = cv2.imread(self.imgdir.template_file)
#                 imgs_2,data_2,label_2 = img_process().load_file_img(self.imgdir.tarappdir,True)
#                 # ssim_align = []
#                 isame = False
#                 for label,img in imgs_2.items():
#                     process = self._get_temp_policy_process(templte,img)
#                     if process.result == True:
#                         # 当50张图片中有满足条件的则break
#                         isame = True
#                         break
#                 print("app:{},policy:{},policy_result:{}".format(tarappname,self.policy,isame))
#                 result.update({tarappname:{self.policy:isame}})
#             else:
#                 print("app:{},policy:{},no template!".format(tarappname,self.policy))
#                 # result.update({tarappname:{self.policy:isame}})
#         return result

#     def diff(self):
#         # 根据版本来批量输出结果 + 准确率统计
#         print('----------------------------diff----start---------------------------------------')
#         self.versiontempresult = self._version_temp()
#         self.normalcount =0
#         self.normallist =[]
#         self.abnormalcount =0
#         self.abnormallist =[]
#         self.count = 0
#         for appname,info in self.versiontempresult.items():
#             self.count += 1
#             if info[self.policy]:
#                 self.normalcount += 1
#                 self.normallist.append(appname)
#             else:
#                 self.abnormalcount += 1
#                 self.abnormallist.append(appname)
#         print("normalcount = {}".format(self.normalcount))
#         print(str(self.normallist))
#         print("abnormalcount = {}".format(self.abnormalcount))
#         print(str(self.abnormallist))
#         print("sum = {}".format(self.count))
#         print("deviation = {}".format(self.abnormalcount/(self.count)))
#         print("accuracy = {}".format((self.normalcount/self.count)))
#         print('----------------------------diff----end---------------------------------------')

# # 批量预处理图片测试代码
# class Preprocessing(object):
#     def __init__(self,oriversion,tarversion,policy):
#         print('-------------Preprocessing start-----------')
#         print('oriversion: '+ str(oriversion) + ' tarversion:' + str(tarversion))
#         self.imgdir = ImageDir(oriversion,tarversion)
#         self.policy = policy
#         print('policy: '+ str(policy))
#         self.diff()
#         print('-------------Preprocessing end-----------')

#     def _get_pre_policy_process(self,img,tarappname):
#         if self.policy == 'obrProcess':
#             return obrProcess(img)
#         elif self.policy == 'cutProcess':
#             return cutProcess(img,tarappname)

#     def _version_temp(self):
#         # 根据版本号批量对比
#         result= dict()
#         from img_load import img_process
#         img_process = img_process()
#         for tarappname in self.imgdir.eff_app_files:
#             self.imgdir.get_apperance_dir(tarappname)
#             img_process = img_process()
#             imgs_2,data_2,label_2 = img_process.load_file_img(self.imgdir.tarappdir,True)
#             iseffect = False
#             for label,img in imgs_2.items():
#                     process = self._get_pre_policy_process(img,tarappname)
#                     if process.result == True:
#                         # 当50张图片中有满足条件的则break
#                         if self.policy == 'obrProcess':
#                             iseffect = True
#                             effect_id = label
#                             break
#                         if self.policy == 'cutProcess':
#                             iseffect = True
#             if self.policy == 'obrProcess':
#                 print("app:{},policy:{},policy_result:{},effect_id:{}".format(tarappname,self.policy,iseffect,effect_id))
#                 result.update({tarappname:{self.policy:iseffect,'effect_id':effect_id}})
#             if self.policy == 'cutProcess':
#                 print("app:{},policy:{},policy_result:{}".format(tarappname,self.policy,iseffect))
#                 result.update({tarappname:{self.policy:iseffect}})
#             # 如果是cut图片预处理需要对原始图片也进行处理
#             if self.policy == 'cutProcess':
#                 imgs,data,label = img_process.load_file_img(self.imgdir.oriappdir,False)
#                 for label,img in imgs.items():
#                     process = self._get_pre_policy_process(img,tarappname)
#                 print("app:{},policy:{},origin_app_preprocessing".format(tarappname,self.policy))
#         return result

#     def diff(self):
#         # 根据版本来批量输出结果 + 准确率统计
#         # print('--------------------------------start---------------------------------------')
#         self.versiontempresult = self._version_temp()
#         self.normalcount =0
#         self.normallist =[]
#         self.abnormalcount =0
#         self.abnormallist =[]
#         self.count = 0
#         for appname,info in self.versiontempresult.items():
#             self.count += 1
#             if info[self.policy]:
#                 self.normalcount += 1
#                 self.normallist.append(appname)
#             else:
#                 self.abnormalcount += 1
#                 self.abnormallist.append(appname)
#         print("no preprocessing required= {}".format(self.normalcount))
#         print(str(self.normallist))
#         print("need preprocessing = {}".format(self.abnormalcount))
#         print(str(self.abnormallist))
#         print("sum = {}".format(self.count))
#         print("deviation = {}".format(self.abnormalcount/(self.count)))
#         print("accuracy = {}".format((self.normalcount/self.count)))
#         # print('----------------------------diff----end---------------------------------------')

# # 主要类-批量预处理+分类
# class ClassifyByPolicyWithProcessing(object):
#     def __init__(self,oriversion,tarversion,policy,prepolicy):
#         print('-------------ClassifyByPolicyWithProcessing start-----------')
#         print('oriversion: '+ str(oriversion) + ' tarversion:' + str(tarversion))
#         self.imgdir = ImageDir(oriversion,tarversion)
#         self.imgdir.copy_apperance_add_dir()
#         self.policy = policy
#         self.prepolicy = prepolicy
#         print('policy: '+ str(policy))
#         print('preprocessing policy: '+ str(prepolicy))
#         self.diff()
#         self.imgtoweb =ImgToWeb(self.imgdir.path_abnormal)
#         self.imgtoweb =ImgToWeb(self.imgdir.path_add)
#         print('-------------ClassifyByPolicyWithProcessing end-----------')
        
#     def _get_policy_process(self,oriimg,img):
#         if self.policy == 'histProcess':
#             return histProcess(oriimg,img)
#         elif self.policy == 'ssimThreshProcess':
#             return ssimThreshProcess(oriimg,img)
#         elif self.policy == 'pHashProcess':
#             return pHashProcess(oriimg,img)
        
#     def _get_preprocessing_policy_process(self,img,tarappname):
#         if self.prepolicy == 'obrProcess':
#             return obrProcess(img)
#         elif self.prepolicy == 'cutProcess':
#             return cutProcess(tarappname)

#     def _get_preprocessing_policy_process_by_tarappname(self,tarappname):
#         # 根据外观名称来决定预处理方法
#         if utils.isClipped(tarappname):
#             self.prepolicy = 'cutProcess'
#         else:
#             self.prepolicy = 'obrProcess'

#     def _version_diff(self):
#         # 根据版本号批量对比
#         result= dict()
#         scores = dict()
#         from img_load import img_process
#         img_process = img_process()
#         for tarappname in self.imgdir.eff_app_files:
#             self.imgdir.get_apperance_dir(tarappname)
#             imgs,data,label = img_process.load_file_img(self.imgdir.oriappdir,False)
#             imgs_2,data_2,label_2 = img_process.load_file_img(self.imgdir.tarappdir,True)
#             self._get_preprocessing_policy_process_by_tarappname(tarappname)
#             if self.prepolicy == 'obrProcess':
#                 count = 0
#                 while(True):
#                     img = imgs_2[list(imgs_2.keys())[0]]
#                     preprocess = self._get_preprocessing_policy_process(img, tarappname)
#                     count += 1
#                     if preprocess.result == True:
#                         break
#                     elif count >= 50:
#                         break
#                     imgs_2,data_2,label_2 = img_process.reload_file_img(self.imgdir.tarappdir,True)
#             isame = False
#             for label,img in imgs_2.items():
#                 if self.prepolicy == 'cutProcess':
#                     preprocess = self._get_preprocessing_policy_process(img, tarappname)
#                     img = preprocess.get_cut_imgs(img)
#                 save_tar = img
#                 most_like_score = 1000000
#                 for orilabel,oriimg in imgs.items():
#                     if self.prepolicy == 'cutProcess':
#                         preprocess = self._get_preprocessing_policy_process(img, tarappname)
#                         oriimg = preprocess.get_cut_imgs(oriimg)
#                     process = self._get_policy_process(oriimg,img)
#                     if utils.compare(process.score, most_like_score):
#                         save_ori_label, save_ori = orilabel,oriimg
#                         most_like_score = process.score
#                         scores.update({tarappname:{self.policy:most_like_score}})
#                     if process.result == True:
#                         # 当50张图片中有满足条件的则break
#                         isame = True
#                         break
#             if isame == False:
#                 if  save_ori.any() and save_tar.any():
#                     self.imgdir.get_apperance_dir_save(tarappname)
#                     self.obnormal_processing(save_ori,save_tar,save_ori_label)
#                     self.imgdir.copy_apperance_abnormal_dir(tarappname)
#             print("app:{},policy:{},policy_result:{}".format(tarappname,self.policy,isame))
#             result.update({tarappname:{self.policy:isame}})
#         json_str = json.dumps(scores)
#         with open(self.imgdir.json_file_name, 'w') as f:
#             f.write(json_str)
#         return result

#     def obnormal_processing(self,ori,tar,orilabel):
#         # 这里写下生成异常图片的阈值画框图片 + 对比图片的拼接图
#         # 注意这里要是预处理之后的图片
#         ssimpre = ssimThreshProcess(ori,tar) # 这里面还有很多可以用的参数和算法，包括tresh画框数量计算，sift修正等等
#         score = ssimpre.get_ssim_score()
#         print("obnormal_processing ssim_core:{}".format(score))
#         threshimg = ssimpre.get_result_img()
#         normalimg = ssimpre.get_normal_img()
#         if Config.HCONCAT_IMG:
#             im_h = cv2.hconcat([normalimg,threshimg])
#         else:
#             im_h = threshimg
#         result_thresh_img = ssimpre.get_thresh_img()
#         result_diff_img = ssimpre.get_diff_img()
#         cv2.imwrite(self.imgdir.save_path + "/" + orilabel , im_h)
#         cv2.imwrite(self.imgdir.save_path_thresh + "/" + orilabel, result_thresh_img)
#         cv2.imwrite(self.imgdir.save_path_diff + "/" + orilabel, result_diff_img)
#         print("obnormal_processing img save.")
        

#     def diff(self):
#         # 根据版本来批量输出结果 + 准确率统计
#         print('----------------------------diff----start---------------------------------------')
#         self.versiondiffresult = self._version_diff()
#         self.normalcount =0
#         self.normallist =[]
#         self.abnormalcount =0
#         self.abnormallist =[]
#         self.count = 0
#         for appname,info in self.versiondiffresult.items():
#             self.count += 1
#             if info[self.policy]:
#                 self.normalcount += 1
#                 self.normallist.append(appname)
#             else:
#                 self.abnormalcount += 1
#                 self.abnormallist.append(appname)
#         print("normalcount = {}".format(self.normalcount))
#         print(str(self.normallist))
#         print("abnormalcount = {}".format(self.abnormalcount))
#         print(str(self.abnormallist))
#         print("sum = {}".format(self.count))
#         print("deviation = {}".format(self.abnormalcount/(self.count)))
#         print("accuracy = {}".format((self.normalcount/self.count)))
#         print('----------------------------diff----end---------------------------------------')


# 主要类-批量预处理+分类
class ClassifyByMultiPolicyWithProcessing(object):
    def __init__(self,oriversion,tarversion,policy,prepolicy,mode):
        print('-------------ClassifyByMultiPolicyWithProcessing start-----------')
        print('oriversion: '+ str(oriversion) + ' tarversion:' + str(tarversion))
        self.mode = mode
        self.imgdir = ImageDir(oriversion,tarversion,utils.getPathByMode(mode)) # 图片路径处理等
        self.imgdir.copy_apperance_add_dir()
        self.policy = policy # 分类策略是个set,可以是多种
        self.prepolicy = prepolicy # 这里其实没多大用处了主要是由_get_preprocessing_policy_process_by_tarappname来决定如何预处理
        print('policy: '+ str(policy))
        print('preprocessing policy: '+ str(prepolicy))
        self.diff() # 主要函数
        self.imgtoweb =ImgToWeb(self.imgdir.path_abnormal) # 上传至web后台打包
        self.imgtoweb =ImgToWeb(self.imgdir.path_add)
        print('-------------ClassifyByMultiPolicyWithProcessing end-----------')
        
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
            if isame == False or self.mode == utils.Mode.D21 or self.mode == utils.Mode.D21DJ:
                if  save_ori.any() and save_tar.any():
                    self.imgdir.get_apperance_dir_save(tarappname)
                    isame = self.obnormal_processing(save_ori,save_tar,save_ori_label,tarappname)
                    # self.imgdir.copy_apperance_abnormal_dir(tarappname)
            print("app:{},policy:{},policy_result:{}".format(tarappname,str(self.policy),isame))
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
        print("obnormal_processing ssim_core:{}".format(score))
        threshimg = ssimpre.get_result_img()
        normalimg = ssimpre.get_normal_img()
        im_h = utils.hconcatImg(self.mode,normalimg,threshimg)
        result_thresh_img = ssimpre.get_thresh_img()
        result_diff_img = ssimpre.get_diff_img()
        if ssimpre.result == False or self.mode == utils.Mode.D21 or self.mode == utils.Mode.D21DJ:
            # 这里再ssim修正一下
            # D21模式还是要存图的，因为量较少且需要正常版本也要输出结果
            cv2.imwrite(self.imgdir.save_path + "/" + orilabel , im_h)
            cv2.imwrite(self.imgdir.save_path_thresh + "/" + orilabel, result_thresh_img)
            cv2.imwrite(self.imgdir.save_path_diff + "/" + orilabel, result_diff_img)
            print("obnormal_processing img save.")
            self.imgdir.copy_apperance_abnormal_dir(tarappname)
        return ssimpre.result

    def diff(self):
        # 根据版本来批量输出结果 + 准确率统计
        print('----------------------------diff----start---------------------------------------')
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
        print("normalcount = {}".format(self.normalcount))
        print(str(self.normallist))
        print("abnormalcount = {}".format(self.abnormalcount))
        print(str(self.abnormallist))
        print("sum = {}".format(self.count))
        print("deviation = {}".format(self.abnormalcount/(self.count)))
        print("accuracy = {}".format((self.normalcount/self.count)))
        print('----------------------------diff----end---------------------------------------')

def jekins_call_class(oriversion,tarversion,mode):
    t = time.time()
    timeArray_ori = time.localtime(utils.extractTimestamp(oriversion))
    otherStyleTime_ori = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_ori)
    timeArray_tar = time.localtime(utils.extractTimestamp(tarversion))
    otherStyleTime_tar = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_tar)
    print("MODE:{}:\ncompare file timestamps:\nori:{},times:{}\ntar:{},times:{}".format(mode,oriversion,otherStyleTime_ori,tarversion,otherStyleTime_tar))
    if utils.isLegalVersion(oriversion,mode) and utils.isLegalVersion(tarversion,mode) and utils.isComparableVersions(oriversion,tarversion,mode):
        mypolicy,myprepolicy = utils.getPolicy(mode)
        result = ClassifyByMultiPolicyWithProcessing(oriversion,tarversion,mypolicy,myprepolicy,mode)
        print(f'coast:{time.time() - t:.4f}s')


if __name__ == '__main__':
    t = time.time()
    #test()
    oriversion = str(sys.argv[1])
    # oriversion = '1682585756'
    # tarversion = '1682670398'
    # tarversion = '1682670399'
    tarversion = str(sys.argv[2])
    mode = utils.Mode(int(sys.argv[3]))
    timeArray_ori = time.localtime(utils.extractTimestamp(oriversion))
    otherStyleTime_ori = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_ori)
    timeArray_tar = time.localtime(utils.extractTimestamp(tarversion))
    otherStyleTime_tar = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_tar)
    print("MODE:{}:\ncompare file timestamps:\nori:{},times:{}\ntar:{},times:{}".format(mode,oriversion,otherStyleTime_ori,tarversion,otherStyleTime_tar))
    if utils.isLegalVersion(oriversion,mode) and utils.isLegalVersion(tarversion,mode) and utils.isComparableVersions(oriversion,tarversion,mode):
        # result = ClassifyByPolicy(oriversion,tarversion,'histProcess')
        # result = ClassifyByPolicy(oriversion,tarversion,'pHashProcess')
        # result = ClassifyByTemplate(oriversion,tarversion,'matchTemplateProcess')
        # result = Preprocessing(oriversion,tarversion,'obrProcess')
        # result = Preprocessing(oriversion,tarversion,'cutProcess')
        # result = ClassifyByPolicyWithProcessing(oriversion,tarversion,'pHashProcess','cutProcess')
        mypolicy,myprepolicy = utils.getPolicy(mode)
        result = ClassifyByMultiPolicyWithProcessing(oriversion,tarversion,mypolicy,myprepolicy,mode)
        # result = ClassifyByMultiPolicyWithProcessing(oriversion,tarversion,['ssimThreshProcess'],'cutProcess') #当固定动作只截一张时
        print(f'coast:{time.time() - t:.4f}s')
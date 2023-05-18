import sys
sys.path.append("..")
from img_load import img_process,ImageDir
from ssim import ssimProcess
import logging
import time
import cv2
from CompareHist import histProcess
from PHash import pHashProcess
from MatchTemplate import matchTemplateProcess

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
        elif self.policy == 'ssimProcess':
            return ssimProcess(oriimg,img)
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

        
if __name__ == '__main__':
    t = time.time()
    #test()
    oriversion = '1682585756'
    # tarversion = '1682650225'
    tarversion = '1682670398'
    #result = ClassifyByPolicy(oriversion,tarversion,'histProcess')
    # result = ClassifyByPolicy(oriversion,tarversion,'pHashProcess')
    result = ClassifyByTemplate(oriversion,tarversion,'matchTemplateProcess')
    print(f'coast:{time.time() - t:.4f}s')
    logging.info(f'coast:{time.time() - t:.4f}s')
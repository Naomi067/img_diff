import cv2
import matplotlib.pyplot as plt
import numpy as np
import logging
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='policy_test.log')
import sys
sys.path.append("..")
from config import Config

class matchTemplateProcess(object):
    def __init__(self, template, compare_image):
        self.template = template
        self.template_h, self.template_w = self.template.shape[:2]
        self.image2 = compare_image
        self.effect_h, self.effect_w = self.image2.shape[:2]
        self.get_match_template()


    def _get_match_template_all_methods(self):
        # 测试用,所有模板匹配算法结果
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        # res = cv2.matchTemplate(self.image2, self.template, cv2.TM_SQDIFF)
        # # 函数返回值就是矩阵的最小值，最大值，最小值的索引，最大值的索引。
        # min_val, max_val, min_index, max_index = cv2.minMaxLoc(res)
        # print(min_val, max_val, min_index, max_index)
        all_imgs = dict()
        for meth in methods:
            img2 = self.image2.copy()
            method = eval(meth)
            res = cv2.matchTemplate(self.image2, self.template, method)
            # 函数返回值就是矩阵的最小值，最大值，最小值的索引，最大值的索引。
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            # print(min_val, max_val, min_loc, max_loc)
        
            # 如果是平方差匹配 TM_SQDIFF 或归一化平方差匹配 TM_SQDIFF_NORMED，取最小值
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            # print(top_left[0],top_left[1])
            ratio = Config.EDGE_RATIO
            # print(self.effect_w*ratio)
            # print(self.effect_w*(1-ratio))
            # print(self.effect_h*ratio)
            # print(self.effect_h*(1-ratio))
            if top_left[0] < self.effect_w*ratio or top_left[0] > self.effect_w*(1-ratio) \
    or top_left[1] < self.effect_h*ratio or top_left[1] > self.effect_h*(1-ratio):
                print(False)
            else:
                print(True)
            bottom_right = (top_left[0] + self.template_w, top_left[1] + self.template_h)
            cv2.rectangle(img2, top_left, bottom_right, 255, 2)
            all_imgs.update({meth:img2})
        self.all_imgs = all_imgs
        return all_imgs

    def get_match_template(self):
        method = eval(Config.MATCH_TEMPLATE_METHOD)
        res = cv2.matchTemplate(self.image2, self.template, method)
        # 函数返回值就是矩阵的最小值，最大值，最小值的索引，最大值的索引。
        min_val, max_val, min_index, max_index = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            self.top_left = min_index
        else:
            self.top_left = max_index
        logging.info("match template: {}, {}".format(self.top_left[0],self.top_left[1]))
        self.result = True
        # print(self.effect_h*0.2)
        # print(self.effect_h*0.9)
        # print(self.effect_w*0.2)
        # print(self.effect_w*0.8)
        # print(self.top_left[0],self.top_left[1])
        ratio = Config.EDGE_RATIO
        if self.top_left[0] < self.effect_w*ratio or self.top_left[0] > self.effect_w*(1-ratio) \
    or self.top_left[1] < self.effect_h*ratio or self.top_left[1] > self.effect_h*(1-ratio):
            self.result = False
        #print(self.result)

    def get_match_template_img(self):
        self.templated = self.image2.copy()
        bottom_right = (self.top_left[0] + self.template_w, self.top_left[1] + self.template_h)
        cv2.rectangle(self.templated, self.top_left, bottom_right, 255, 2)
        return self.templated

if __name__ == '__main__':
    #读取测试图片
    logging.info('----------------------------matchTemplateProcess--start---------------------------------------')
    Headdress_template = "G:/img_diff/tools/AllImages/L32/template/school7Headdress.jpg"
    second_same = 'G:/img_diff/tools/AllImages/L32/1682670398/school7Headdress60099/tick28.jpg'
    
    # first_dif = "G:/img_diff/tools/AllImages/L32/1682585756/school7Dress120013/tick1.jpg"
    second_dif = "G:/img_diff/tools/AllImages/L32/1682670398/school7Headdress60157/tick9.jpg"

    img1=cv2.imread(Headdress_template)
    img11=cv2.imread(second_same)
    imh21 = cv2.imread(second_dif)

    # img2=cv2.imread(first_dif)#读取测试图片
    # img21=cv2.imread(second_dif)
    mtp = matchTemplateProcess(img1,img11)
    mtp._get_match_template_all_methods()
    img_list = list()
    method_list =list()
    plt.figure(dpi=120,figsize=(16,8))
    i = 1
    for method, img in mtp.all_imgs.items():
        plt.subplot(2,3,i) 
        plt.title(method)
        plt.imshow(img,plt.cm.gray)
        plt.axis('off')
        i = i+1
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/matchTemplate_all.jpg')
    plt.show()
    plt.figure(dpi=120,figsize=(12,8))
    plt.subplot(1,2,1) 
    plt.title('template')
    plt.imshow(mtp.template)
    plt.axis('off')
    mtp.get_match_template_img()
    plt.subplot(1,2,2) 
    plt.title('matchTemlate')
    plt.imshow(mtp.templated)
    plt.axis('off')
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/matchTemplate.jpg')
    plt.show()

    mtp = matchTemplateProcess(img1,imh21)
    mtp._get_match_template_all_methods()
    img_list = list()
    method_list =list()
    plt.figure(dpi=120,figsize=(16,8))
    i = 1
    for method, img in mtp.all_imgs.items():
        plt.subplot(2,3,i) 
        plt.title(method)
        plt.imshow(img,plt.cm.gray)
        plt.axis('off')
        i = i+1
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/matchTemplate_all_diff.jpg')
    plt.show()
    plt.figure(dpi=120,figsize=(12,8))
    plt.subplot(1,2,1) 
    plt.title('template')
    plt.imshow(mtp.template)
    plt.axis('off')
    mtp.get_match_template_img()
    plt.subplot(1,2,2) 
    plt.title('matchTemlate')
    plt.imshow(mtp.templated)
    plt.axis('off')
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/matchTemplate_diff.jpg')
    plt.show()
    logging.info('----------------------------matchTemplateProcess--end---------------------------------------')
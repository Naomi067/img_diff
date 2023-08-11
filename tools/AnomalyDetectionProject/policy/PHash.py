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

class pHashProcess(object):
    def __init__(self, normal_image, compare_image):
        self.image1 = normal_image
        self.image2 = compare_image
        self.score = self.get_p_hash_result()
        logging.info('hash_value: '+str(self.score))
        self.result = True if self.score <= Config.PHASH_VALUE else False

    def get_img_p_hash(self,img):
        hash_len = 32
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        resize_gray_img = cv2.resize(gray_img, (hash_len, hash_len), cv2.INTER_AREA)
        h, w = resize_gray_img.shape[:2]
        vis0 = np.zeros((h, w), np.float32)
        vis0[:h, :w] = resize_gray_img
        # DCT: Discrete cosine transform(离散余弦变换)
        vis1 = cv2.dct(cv2.dct(vis0))
        vis1.resize(hash_len, hash_len)
        img_list = vis1.flatten()
        # Calculate the avg value
        avg = sum(img_list) * 1. / len(img_list)
        avg_list = []
        for i in img_list:
            if i < avg:
                tmp = '0'
            else:
                tmp = '1'
            avg_list.append(tmp)
        # Calculate the hash value
        p_hash_str = ''
        for x in range(0, hash_len * hash_len, 4):
            p_hash_str += '%x' % int(''.join(avg_list[x:x + 4]), 2)
        return p_hash_str,vis1

    def ham_dist(self, x, y):
        assert len(x) == len(y)
        return sum([ch1 != ch2 for ch1, ch2 in zip(x, y)])

    def get_p_hash_result(self):
        hash_img1,self.vis1 = self.get_img_p_hash(self.image1)
        hash_img2,self.vis2 = self.get_img_p_hash(self.image2)
        return self.ham_dist(hash_img1, hash_img2)


if __name__ == '__main__':
    #读取测试图片
    logging.info('----------------------------pHashProcess--start---------------------------------------')
    first_same = "G:/img_diff/tools/AllImages/L32/1682585756/school7Headdress60099/tick1.jpg"
    second_same = 'G:/img_diff/tools/AllImages/L32/1682670398/school7Headdress60099/tick28.jpg'
    first_dif = "G:/img_diff/tools/AllImages/L32/1682585756/school7Dress120013/tick1.jpg"
    second_dif = "G:/img_diff/tools/AllImages/L32/1682670398/school7Dress120013/tick9.jpg"

    img1=cv2.imread(first_same)
    img11=cv2.imread(second_same)

    img2=cv2.imread(first_dif)#读取测试图片
    img21=cv2.imread(second_dif)

    hp1 = pHashProcess(img1, img11)
    print(hp1.hash_value)
    hp2 = pHashProcess(img2, img21)
    print(hp2.hash_value)
    fig, axes =plt.subplots(nrows=2, ncols=2,dpi=120,figsize=(12,8))
    axes[0,0].matshow(hp1.vis1,cmap=plt.cm.gray)
    axes[0,0].set_xlabel("first_same")
    axes[0,1].matshow(hp1.vis2,cmap=plt.cm.gray)
    axes[0,1].set_xlabel("second_same")
    axes[1,0].matshow(hp2.vis1,cmap=plt.cm.gray)
    axes[1,0].set_xlabel("first_dif")
    axes[1,1].matshow(hp2.vis2,cmap=plt.cm.gray)
    axes[1,1].set_xlabel("second_dif")
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/pHash.jpg')
    plt.show()
    # cv2.destroyAllWindows()
    logging.info('----------------------------pHashProcess--end---------------------------------------')
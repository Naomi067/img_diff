import cv2
import matplotlib.pyplot as plt
import logging
import time
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='policy_test.log')

#计算方差
def getss(list):
    #计算平均值
    avg=sum(list)/len(list)
    #定义方差变量ss，初值为0
    ss=0
    #计算方差
    for l in list:
        ss+=(l-avg)*(l-avg)/len(list)
    #返回方差
    return ss
 
#获取每行像素平均值
def getdiff(img):
    #定义边长
    Sidelength=30
    #缩放图像
    img=cv2.resize(img,(Sidelength,Sidelength),interpolation=cv2.INTER_CUBIC)
    #灰度处理
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #avglist列表保存每行像素平均值
    avglist=[]
    #计算每行均值，保存到avglist列表
    for i in range(Sidelength):
        avg=sum(gray[i])/len(gray[i])
        avglist.append(avg)
    #返回avglist平均值
    return avglist
 

if __name__ == '__main__':
    #读取测试图片
    logging.info('----------------------------PixelVariance.py--start---------------------------------------')
    first_same = "G:/img_diff/tools/AllImages/L32/1682585756/school7Headdress60099/tick1.jpg"
    second_same = 'G:/img_diff/tools/AllImages/L32/1682670398/school7Headdress60099/tick28.jpg'
    first_dif = "G:/img_diff/tools/AllImages/L32/1682585756/school7Dress120013/tick1.jpg"
    second_dif = "G:/img_diff/tools/AllImages/L32/1682670398/school7Dress120013/tick9.jpg"

    img1=cv2.imread(first_same)
    diff1=getdiff(img1)
    logging.info(first_same+":"+str(getss(diff1)))
    
    #读取测试图片
    img11=cv2.imread(second_same)
    diff11=getdiff(img11)
    logging.info(first_same+":"+str(getss(diff11)))
    
    ss1=getss(diff1)
    ss2=getss(diff11)
    logging.info("The variance of the two images is: {}".format(abs(ss1-ss2)))
    
    x=range(30)
    
    plt.figure("PixelVariance_same")
    plt.plot(x,diff1,marker="*",label="$1682585756/school7Headdress60099/tick1.jpg$")
    plt.plot(x,diff11,marker="*",label="$1682670398/school7Headdress60099/tick28.jpg$")
    plt.title("PixelVariance_same")
    plt.legend()
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/PixelVariance_same.jpg')
    plt.show()
    

    img2=cv2.imread(first_dif)
    diff2=getdiff(img2)
    logging.info(first_dif+":"+str(getss(diff2)))
    
    #读取测试图片
    img21=cv2.imread(second_dif)
    diff21=getdiff(img21)
    logging.info(second_dif+":"+str(getss(diff21)))
    
    ss21=getss(diff2)
    ss22=getss(diff21)
    logging.info("The variance of the two images is: {}".format(abs(ss21-ss22)))
    
    x=range(30)
    
    plt.figure("PixelVariance_dif")
    plt.plot(x,diff2,marker="*",label="$1682585756/school7Dress120013/tick1.jpg$")
    plt.plot(x,diff21,marker="*",label="$1682670398/school7Dress120013/tick9.jpg$")
    plt.title("PixelVariance_dif")
    plt.legend()
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/PixelVariance_dif.jpg')
    plt.show()
    
    
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    logging.info('----------------------------PixelVariance.py--end---------------------------------------')
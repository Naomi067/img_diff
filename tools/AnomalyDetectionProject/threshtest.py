#这个是用来调整画threshold参数的测试文件
import numpy as np
import cv2
from matplotlib import pyplot as plt
from ssim import ssimProcess
import imutils
threshtest = False
threshlimittest = True
first = "G:/ai_image/ai-airtest/AllImages/D90/RepeatingCrossbow/RepeatingCrossbow_MidnightShriek_2.jpg"
second = 'G:/ai_image/ai-airtest/AllImages/D90/RepeatingCrossbow2/RepeatingCrossbow_MidnightShriek_2.jpg'
first_img =  cv2.imread(first)
second_img = cv2.imread(second)
gray = cv2.cvtColor(first_img, cv2.COLOR_BGR2GRAY)
count=0
for i in gray:
    if i[0]!=0:
        count =count+1
print(count)
print(gray)
ssimpre = ssimProcess(first_img,second_img)
diff,score,hlimit,wlimit = ssimpre.compare()
diff = (diff * 255).astype("uint8")
thresh = 0
imgdata = {}
while thresh < 255 and threshtest == True:
    thresh_img = cv2.threshold(diff, thresh, 255,cv2.THRESH_TOZERO_INV)[1]
    imgdata[thresh] = thresh_img
    thresh = thresh + 20
if threshtest == True:
    plt.figure()
    count =1
    for k,v in imgdata.items():
        plt.subplot(3,5,count)
        count= count+1
        plt.imshow(v)
        plt.xticks([])
        plt.yticks([])
        plt.title("thresh="+str(k))
    plt.show()

THRESH_ALGRITHON = 50
thresh = cv2.threshold(diff, THRESH_ALGRITHON, 255,
                                cv2.THRESH_TOZERO_INV)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
imgdata2 = {}
countlimit = 0
hlimit = 20
wlimit = 40
while threshlimittest == True and hlimit > 0 and wlimit > 0:
    countlimit = countlimit + 1
    print(countlimit)
    print(hlimit,wlimit)
    tempimag = np.copy(second_img)
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w < wlimit or h< hlimit:
            continue
        else:
            cv2.rectangle(tempimag, (x, y), (x + w, y + h), (0, 0, 255), 2)
    imgdata2["h:{}w:{}".format(hlimit,wlimit)] = tempimag
    hlimit = hlimit - 5
    wlimit = wlimit - 10

if threshlimittest == True:
    plt.figure()
    count =1
    for k,v in imgdata2.items():
        plt.subplot(2,2,count)
        count= count+1
        plt.imshow(v)
        cv2.imshow(k,v)
        plt.xticks([])
        plt.yticks([])
        plt.title("threshlimit="+str(k))
    plt.show()
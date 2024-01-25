"""
================================
Recognizing hand-written digits
================================

An example showing how the scikit-learn can be used to recognize images of
hand-written digits.

This example is commented in the
:ref:`tutorial section of the user manual <introduction>`.

"""
print(__doc__)

# Author: Gael Varoquaux <gael dot varoquaux at normalesup dot org>
# License: BSD 3 clause

import matplotlib.pyplot as plt
from sklearn import datasets, svm, metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


if __name__ == "__main__":
    # The digits dataset
    digits = datasets.load_digits()
    print(digits.DESCR)

    #打印数据集中的第一个图像
    print(digits.images[0])

    #显示数据集中的第一个图像
    # plt.imshow(digits.images[0], cmap=plt.cm.gray_r, interpolation='nearest')


    # The data that we are interested in is made of 8x8 images of digits, let's
    # have a look at the first 4 images, stored in the `images` attribute of the
    # dataset.  If we were working from image files, we could load them using
    # matplotlib.pyplot.imread.  Note that each image must have the same size. For these
    # images, we know which digit they represent: it is given in the 'target' of
    # the dataset.

    # 绘制数据集中的前4个图像, 了解zip方法的作用
    _, axes = plt.subplots(4, 4)  # 将输出的图分为4行4列
    images_and_labels = list(zip(digits.images, digits.target))
    # 第一行输出数据集中的前4个图像
    for ax, (image, label) in zip(axes[0, :], images_and_labels[:4]):
        ax.set_axis_off()
        ax.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
        ax.set_title('Training: %i' % label)

    # To apply a classifier on this data, we need to flatten the image, to
    # turn the data in a (samples, feature) matrix:
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))

    # 创建svm分类器
    svc_clf = svm.SVC(gamma=0.001)
    # 创建KNN分类器
    knn_clf = KNeighborsClassifier()
    # 创建朴素贝叶斯分类器
    nb_clf = MultinomialNB()


    # Split data into train and test subsets
    # 使用train_test_split将数据集分为训练集，测试集, y_train 表示训练集中样本的类别标签, y_test表示测试集中样本的类别标签
    # test_size = 0.5 表示使用一半数据进行测试, 另一半就用于训练
    X_train, X_test, y_train, y_test = train_test_split(
        data, digits.target, test_size=0.5, shuffle=False)

    # 调用fit方法进行训练，传入训练集样本和样本的类别标签，进行有监督学习
    svc_clf.fit(X_train, y_train)
    knn_clf.fit(X_train, y_train)
    nb_clf.fit(X_train, y_train)

    # 调用predict， 用训练得到的模型在测试集进行类别预测，得到预测的类别标签
    svc_predicted = svc_clf.predict(X_test)
    knn_predicted = knn_clf.predict(X_test)
    nb_predicted = nb_clf.predict(X_test)

    """
    zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
    例子：
    a = [1,2,3]
    b = [4,5,6]
    zipped = zip(a,b) 
    得到 [(1, 4), (2, 5), (3, 6)]

    注意 zip(digits.images[n_samples // 2:]
    // 表示整数除法,  /表示浮点数除法
    """
    svc_images_and_predictions = list(zip(digits.images[n_samples // 2:], svc_predicted))
    knn_images_and_predictions = list(zip(digits.images[n_samples // 2:], knn_predicted))
    nb_images_and_predictions = list(zip(digits.images[n_samples // 2:], nb_predicted))

    # 在图表的第二行输出svm在测试集的前四个手写体图像上的分类结果，大家可以在图上看看结果对不对
    for ax, (image, svc_prediction) in zip(axes[1, :], svc_images_and_predictions[:4]):
        ax.set_axis_off()
        ax.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
        ax.set_title('Prediction: %i' % svc_prediction)

    # 在图表的第三行输出KNN在测试集的前四个手写体图像上的分类结果，大家可以在图上看看结果对不对
    # 大家应该可以发现KNN把第二列的8这个手写数字识别为3，发生错误
    for ax, (image, knn_prediction) in zip(axes[2, :], knn_images_and_predictions[:4]):
        ax.set_axis_off()
        ax.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
        ax.set_title('Prediction: %i' % knn_prediction)

    # 在图表的第四行输出朴素贝叶斯在测试集的前四个手写体图像上的分类结果，大家可以在图上看看结果对不对
    for ax, (image, nb_prediction) in zip(axes[3, :], nb_images_and_predictions[:4]):
        ax.set_axis_off()
        ax.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
        ax.set_title('Prediction: %i' % nb_prediction)

    # 绘制出图
    plt.show()

    # 输出三个分类器的性能指标，大家需要了解二分类、多分类的性能评估指标主要有哪些

    # 输出svm的分类性能指标
    print("Classification report for classifier %s:\n%s\n"
        % (svc_clf, metrics.classification_report(y_test, svc_predicted)))

    # 输出KNN的分类性能指标
    print("Classification report for classifier %s:\n%s\n"
        % (knn_clf, metrics.classification_report(y_test, knn_predicted)))

    # 输出naive bayes的分类性能指标
    print("Classification report for classifier %s:\n%s\n"
        % (nb_clf, metrics.classification_report(y_test, nb_predicted)))
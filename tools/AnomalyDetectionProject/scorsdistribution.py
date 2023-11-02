
import matplotlib.pyplot as plt
import json
import seaborn as sns
import numpy as np
import utils
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import svm
from sklearn.ensemble import IsolationForest
import win32api

def scors_distribution(scorsdistribution):
    # 这个函数用来看下差异值的分布情况
    # 提取所有policy名称
    policies = list(set([policy for app in scorsdistribution.values() for policy in app.keys()]))
    
    # 针对每个policy，提取出所有most_like_score，并画出分布直方图
    for policy in policies:
        scores = [app[policy] for app in scorsdistribution.values() if policy in app.keys()]
        # plt.kdeplot(scores)
        sns.kdeplot(scores)
    # 添加图例和标题
    
    plt.show()


def calc_density(scorsdistribution):
    # 密度分布
    types = []
    scores_list = []

    # 遍历scores字典，将分类和最相似分数加入列表
    for tarappname, policy_scores in scorsdistribution.items():
        score_list = list(policy_scores.values())
        if score_list:
            types.append(utils.getApparanceType(tarappname))
            scores_list.extend(score_list)

    # 将列表转换为numpy数组
    types = np.array(types)
    scores_list = np.array(scores_list)

    # 根据类型分子图显示分布
    num_types = len(set(types))
    fig, axes = plt.subplots(1, num_types, figsize=(16, 6), sharey=True)
    plt.subplots_adjust(wspace=0.05)

    for i, t in enumerate(sorted(set(types))):
        t_scores = scores_list[types == t]
        sns.kdeplot(t_scores, ax=axes[i])
        axes[i].set_title(f'Type {t}')
        axes[i].set_xlabel('Policy Scores')

    # 显示图形
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/calc_density.jpg')
    plt.show()

def calc_density_2(scorsdistribution):
    # Swarm 分布
    types = []
    scores_list = []

    # 遍历scores字典，将分类和最相似分数加入列表
    for tarappname, policy_scores in scorsdistribution.items():
        score_list = list(policy_scores.values())
        if score_list:
            types.append(utils.getApparanceType(tarappname))
            scores_list.extend(score_list)

    df = pd.DataFrame({'Type': types, 'Policy Score': scores_list})

    sns.swarmplot(y='Policy Score', x='Type', data=df)
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/calc_density_2.jpg')
    plt.show()


def kmeans(scorsdistribution):
    # Swarm 分布
    types = []
    scores_list = []

    # 遍历scores字典，将分类和最相似分数加入列表
    for tarappname, policy_scores in scorsdistribution.items():
        score_list = list(policy_scores.values())
        if score_list:
            types.append(utils.getApparanceType(tarappname))
            scores_list.extend(score_list)

    df = pd.DataFrame({'Type': types, 'Policy Score': scores_list})

    # 对数据进行标准化
    data = (df - df.mean()) / df.std()

    # 使用KMeans算法进行聚类
    kmeans = KMeans(n_clusters=1)
    kmeans.fit(data)

    # 标记异常值
    y_pred = kmeans.predict(data)
    dist = np.min(kmeans.transform(data), axis=1)
    threshold = np.percentile(dist, 95)
    outliers = dist > threshold

    # 删除异常值
    new_df = df[~outliers]

    # 可视化异常值
    plt.figure(figsize=(8, 6))
    plt.scatter(df['Type'][outliers], df['Policy Score'][outliers], color='red', label='Outliers')
    plt.scatter(df['Type'][~outliers], df['Policy Score'][~outliers], color='blue', label='Inliers')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Outliers')
    plt.legend()
    plt.show()

def OC_SVM(scorsdistribution):
    types = []
    scores_list = []

    # 遍历scores字典，将分类和最相似分数加入列表
    for tarappname, policy_scores in scorsdistribution.items():
        score_list = list(policy_scores.values())
        if score_list:
            types.append(utils.getApparanceType(tarappname))
            scores_list.extend(score_list)

    df = pd.DataFrame({'Type': types, 'Policy Score': scores_list})

    # 使用 One-Class SVM 模型进行聚类
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    clf.fit(df)

    # 获取每个数据点的聚类标签
    labels = clf.predict(df)
    plt.scatter(df['Type'], df['Policy Score'], c=labels, cmap='viridis')
    plt.xlabel('Type')
    plt.ylabel('Policy Score')
    plt.title('OC-SVM Clustering')
    # 打印聚类结果
    print(labels)
    # 显示图形
    plt.show()

def test_IsolationForest(scorsdistribution):
    types = []
    scores_list = []

    # 遍历scores字典，将分类和最相似分数加入列表
    for tarappname, policy_scores in scorsdistribution.items():
        score_list = list(policy_scores.values())
        if score_list:
            types.append(utils.getApparanceType(tarappname))
            scores_list.extend(score_list)

    df = pd.DataFrame({'Type': types, 'Policy Score': scores_list})

    # 使用孤立森林模型进行分类
    clf = IsolationForest(contamination=0.1)
    clf.fit(df)

    # 获取每个数据点的分类标签
    labels = clf.predict(df)

    # 绘制散点图
    plt.scatter(df['Type'], df['Policy Score'], c=labels, cmap='viridis')

    # 添加轴标签和标题
    plt.xlabel('Type')
    plt.ylabel('Policy Score')
    plt.title('Isolation Forest Classification')

    # 显示图形
    plt.show()

def Z_score(scorsdistribution):

    width, height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
    fig, ax = plt.subplots(figsize=(width/100, height/100))

    types = []
    scores_list = []
    name_list = []

    # 遍历scores字典，将分类和最相似分数加入列表
    for tarappname, policy_scores in scorsdistribution.items():
        score_list = list(policy_scores.values())
        if score_list:
            types.append(utils.getApparanceType(tarappname))
            name_list.append(tarappname)
            scores_list.extend(score_list)

    df = pd.DataFrame({'Type': types, 'Policy Score': scores_list, 'App Name': name_list})

    # 计算Z-score标准化后的值
    df['Policy Score Z-score'] = (df['Policy Score'] - df['Policy Score'].mean()) / df['Policy Score'].std()

    # 使用3σ原则识别异常值
    threshold = 3
    df['Outlier'] = np.where(df['Policy Score Z-score'].abs() > threshold, 1, 0)

    # 绘制散点图
    ax.scatter(df['Type'], df['Policy Score'], c=df['Outlier'], cmap='viridis')

    for i, txt in enumerate(df.loc[df['Outlier'] == 1, 'App Name']):
        plt.annotate(txt, (df.loc[df['Outlier'] == 1, 'Type'].iloc[i], df.loc[df['Outlier'] == 1, 'Policy Score'].iloc[i]))
    # 添加轴标签和标题
    ax.set_xlabel('Type')
    ax.set_ylabel('Policy Score')
    ax.set_title('Z_score')

    # 显示图形
    plt.show()

def calc_density_3(scorsdistribution, para):
    # 获取屏幕分辨率
    width, height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

    # 读取数据
    types = []
    scores_list = []
    name_list = []

    for tarappname, policy_scores in scorsdistribution.items():
        score_list = list(policy_scores.values())
        if score_list:
            types.append(utils.getApparanceType(tarappname))
            name_list.append(tarappname)
            scores_list.extend(score_list)

    df = pd.DataFrame({'Type': types, 'Policy Score': scores_list, 'App Name': name_list})

    # 判断Policy Score是否大于1000
    df['Outlier'] = df['Policy Score'].apply(lambda x: 1 if x > para else 0)

    # count the total number of outlier points
    num_outliers = df[df['Outlier'] == 1].shape[0]
    print(f'Total number of outliers: {num_outliers}')

    # create a list of outlier names
    outlier_names = df.loc[df['Outlier'] == 1, 'App Name'].tolist()

    # display the list of outlier names
    print('List of outlier names:')
    for name in outlier_names:
        print(name)

    # 创建绘图窗口，并设置大小
    fig, ax = plt.subplots(figsize=(width/200, height/200))

    # 绘制散点图
    ax.scatter(df['Type'], df['Policy Score'], c=df['Outlier'], cmap='viridis')
    # sns.swarmplot(x='Type', y='Policy Score', data=df, hue='Outlier', palette='viridis', ax=ax)

    # 在异常数据点上添加标注
    for i, txt in enumerate(df.loc[df['Outlier'] == 1, 'App Name']):
        ax.annotate(txt, (df.loc[df['Outlier'] == 1, 'Type'].iloc[i], df.loc[df['Outlier'] == 1, 'Policy Score'].iloc[i]))
    
    # 添加轴标签和标题
    ax.set_xlabel('Type')
    ax.set_ylabel('Policy Score')
    ax.set_title('Scatter Plot with Labels')

    # 显示图形
    plt.show()

# 以下是二维数据的异常检测
def boxplot(scorsdistribution):
    # 提取数据
    x_values = []
    y_values = []
    for key in scorsdistribution:
        value = eval(scorsdistribution[key]["['pHashProcess', 'histProcess']"])
        if len(value) == 2:
            x_values.append(value[0]/10)
            y_values.append(value[1]/1000)

    # 绘制散点图
    fig, ax = plt.subplots()
    ax.scatter(x_values, y_values)

    plt.show()

def hist2d(scorsdistribution):

    # 将数据集转换为 pandas DataFrame
    df = pd.DataFrame([(eval(scorsdistribution[key]["['pHashProcess', 'histProcess']"])[0], eval(scorsdistribution[key]["['pHashProcess', 'histProcess']"])[1]) for key in scorsdistribution.keys()], columns=['pHashProcess', 'histProcess'])

    # 绘制二维直方图
    sns.histplot(data=df, x='pHashProcess', y='histProcess', bins=30, cmap='Reds') # 直方图
    # sns.jointplot(data=df, x='pHashProcess', y='histProcess') # 散点图
    # sns.jointplot(x='pHashProcess', y='histProcess', data=df, kind="kde") # 核密度估计

    # 添加标题和标签
    plt.title('2D Histogram')
    plt.xlabel('pHashProcess')
    plt.ylabel('histProcess')
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/2D_Histogram.jpg')
    # 展示图表
    plt.show()

def calc_set(scorsdistribution):
    pHashProcessSet = set()
    histProcessSet = set()

    for key, value in scorsdistribution.items():
        if eval(value["['pHashProcess', 'histProcess']"])[0] > 10:
            pHashProcessSet.add(key)
        if eval(value["['pHashProcess', 'histProcess']"])[1] > 1000:
            histProcessSet.add(key)
    print(len(pHashProcessSet))
    print(len(histProcessSet))
    print(pHashProcessSet-histProcessSet)
    print(histProcessSet-pHashProcessSet)

if __name__ == "__main__":
    # 打开scorsdistribution.json文件，以读取模式读取json字符串
    with open('1682585756_1682670398.json', 'r') as f:
        json_str = f.read()

    # 将json字符串转换为dict
    scorsdistribution = json.loads(json_str)
    # boxplot(scorsdistribution)
    # hist2d(scorsdistribution)
    calc_set(scorsdistribution)
    # with open('scorsdistribution.json', 'r') as b:
    #     json_str_2 = b.read()

    # # 将json字符串转换为dict
    # scorsdistribution_2 = json.loads(json_str_2)

    # 输出读取的dict
    # print(scorsdistribution)
    # calc_density_2(scorsdistribution)
    # calc_density(scorsdistribution)
    # kmeans(scorsdistribution)
    # calc_density_3(scorsdistribution,10)
    # calc_density_3(scorsdistribution_2,1000)
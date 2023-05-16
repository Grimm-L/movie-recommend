import json
import pandas as pd
import numpy as np
import math
import random


class CBRecommend:
    # 加载dataProcessing.py中预处理的数据
    def __init__(self, K):
        # 给用户推荐的item个数
        self.K = K
        self.item_profile = json.load(open("C:/Users/56469/Desktop/output_json/item_profile.json", "r"))
        self.user_profile = json.load(open("C:/Users/56469/Desktop/output_json/user_profile.json", "r"))

    # 获取用户未进行评分的item列表
    def get_none_score_item(self, user):
        items = pd.read_csv("C:/Users/56469/Desktop/top250.CSV",encoding = 'gbk')["id"].values
        data = pd.read_csv("C:/Users/56469/Desktop/user_ratedmovies.CSV", encoding = 'gbk')
        have_score_items = data[data["userID"] == user]["movieID"].values
        none_score_items = set(items) - set(have_score_items)
        return none_score_items

    # 获取用户对item的喜好程度
    def cosUI(self, user, item):
        # 通过余弦相似度
        # Uia 分子 Ua（用户对电影的偏好矩阵） Ia（电影类型的特征信息矩阵）电影是否属于类型a
        Uia = sum(np.array(self.user_profile[str(user)]) * np.array(self.item_profile[str(item)]))
        Ua = math.sqrt(sum([math.pow(one, 2) for one in self.user_profile[str(user)]]))  # 分母 Ua
        Ia = math.sqrt(sum([math.pow(one, 2) for one in self.item_profile[str(item)]]))  # 分母 Ia
        return Uia / (Ua * Ia)

     # 为用户进行电影推荐
    def recommend(self, user):
        user_result = {}
        item_list = self.get_none_score_item(user)
        for item in item_list:
            user_result[item] = self.cosUI(user, item)  # 获取用户对Item的喜好程度集合
        if self.K is None:
            result = sorted(user_result.items(), key=lambda k: k[1], reverse=True)
        else:
            result = sorted(user_result.items(), key=lambda k: k[1], reverse=True)[:self.K]
        # print(result)
        mid = []
        for i in result:
            mid.append(i[0])
        # print(mid)
        return mid


    # 推荐系统效果评估
    def evaluate(self):
        evas = []
        data = pd.read_csv("C:/Users/56469/Desktop/user_ratedmovies.CSV", encoding = 'gbk')
        for user in random.sample([one for one in range(1, 15)], 2):
            have_score_items = data[data["userID"] == user]["movieID"].values
            items = pd.read_csv("C:/Users/56469/Desktop/top250.CSV", encoding = 'gbk')["id"].values

            user_result = {}
            for item in items:
                user_result[item] = self.cosUI(user, item)
            results = sorted(
                user_result.items(), key=lambda k: k[1], reverse=True
            )[:len(have_score_items)]
            rec_items = []
            for one in results:
                rec_items.append(one[0])
            eva = len(set(rec_items) & set(have_score_items)) / len(have_score_items)
            evas.append(eva)
        return sum(evas) / len(evas)

# if __name__ == "__main__":
#     cb = CBRecommend(K=5)
#     movies_m = cb.recommend(10)
#     print(movies_m)
    # print(cb.evaluate())
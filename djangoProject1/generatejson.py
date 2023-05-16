import json
import pandas as pd

# 获取item的特征信息矩阵
def prepare_item_profile(self,file='C:/Users/56469/Desktop/top250.CSV'):
    items=pd.read_csv(file)
    item_ids=set(items["id"].values)  #MovieID{1,2,3,4,.....}
    self.item_dict={}
    #{1: ['Animation', "Children's", 'Comedy']，
    # 2:['Adventure', "Children's", 'Fantasy'],..}
    # #电影ID 和对应的电影类型
    genres_all=list()
    # 将每个电影的类型放在item_dict中
    for item in item_ids:
        genres=items[items["id"]==item]["type"].values[0].split("|")
        #['Animation', "Children's", 'Comedy']
        self.item_dict.setdefault(item,[]).extend(genres)
        #{1: ['Animation', "Children's", 'Comedy']}
        genres_all.extend(genres)
        #extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）。
    self.genres_all=set(genres_all)
    #去掉重复特征数据 得到18个特征{"Children's", 'Western', 'Drama', 'Musical', 'Mystery', 'Animation', 'Adventure', 'Sci-Fi', 'Romance', 'War', 'Action', 'Documentary', 'Film-Noir', 'Thriller', 'Crime', 'Comedy', 'Fantasy', 'Horror'}
    # 将每个电影的特征信息矩阵存放在 self.item_matrix中
    # 保存dict时，key只能为str，所以这里对item id做str()转换
    self.item_matrix={}
    #{'1': [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], '2': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    for item in self.item_dict.keys():
        self.item_matrix[str(item)]=[0] * len(set(self.genres_all))
        #创建一个 key为item电影ID，value 为长度为18初始值为0的数组 的数据字典{'1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        for genre in self.item_dict[item]:
            index=list(set(genres_all)).index(genre)
            #找到类型为例如'Animation'在genres_all所有类型集合中的位置(index)
            self.item_matrix[str(item)][index]=1
            #把对应 value 数值下标为5的值 0换成1
            #[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]离散型One——Hot编码
    json.dump(self.item_matrix,
              open('C:/Users/56469/Desktop/output_json/item_profile.json','w'))
    print("item 信息计算完成，保存路径为：{}".format('C:/Users/56469/Desktop/output_json/item_profile.json'))


# 计算用户的偏好矩阵
def prepare_user_profile(self, file='C:/Users/56469/Desktop/user_ratedmovies.CSV'):
    users = pd.read_csv(file)  # users:UserID,MovieID,Rating,Timestamp
    user_ids = set(users["userID"].values)  # 遍历用户UserId
    # 将users信息转化成dict
    users_rating_dict = {}  # {'UserId': {item1 :rate1,item2 :rate2}, '2': {}, '3': {},....}
    for user in user_ids:
        users_rating_dict.setdefault(str(user), {})  # {'1': {}}
    with open(file, "r") as fr:  # 无异常读文件
        for line in fr.readlines():  # 读每一行
            if not line.startswith("userID"):  # 去除第一行文字
                (user, item, rate) = line.split(",")[:3]
                users_rating_dict[user][item] = int(rate)  # 把 截取userId作为key  value (item :rate){1:{'1193': 5, '661': 3}}

    # 获取用户对每个类型下都有哪些电影进行了评分
    self.user_matrix = {}
    # 遍历每个用户
    for user in users_rating_dict.keys():
        print("user is {}".format(user))
        score_list = users_rating_dict[user].values()
        # 用户的平均打分
        avg = sum(score_list) / len(score_list)
        self.user_matrix[user] = []
        # 遍历每个类型（保证item_profile和user_profile信息矩阵中每列表示的类型一致）
        for genre in self.genres_all:  # 依次遍历每一个类型
            score_all = 0.0
            score_len = 0
            # 遍历每个item
            for item in users_rating_dict[user].keys():  # 遍历用户1的电影Id列表
                # 判断类型是否在用户评分过的电影里
                if genre in self.item_dict[int(item)]:  # 并判断这个电影类型是否在这个item的描述类型中
                    score_all += (users_rating_dict[user][item] - avg)  # 计算用户1对某一电影类型偏好程度公式
                    # 把所有用户看过这个类型的电影 依次评分与平均分相减和除以评分该类型电影总数
                    score_len += 1
            if score_len == 0:  # 用户无评分该类型电影
                self.user_matrix[user].append(0.0)
            else:
                self.user_matrix[user].append(score_all / score_len)  # 把所有用户看过这个类型的电影 依次评分与平均分相减  和除以评分该类型电影总数
    json.dump(self.user_matrix,
              open('C:/Users/56469/Desktop/output_json/user_profile.json', 'w'))
    print("user 信息计算完成，保存路径为：{}".format('C:/Users/56469/Desktop/output_json/user_profile.json'))




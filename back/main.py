import copy
import math

# from data_process.mk_index_sample import mk_index_sample
# from data_process.mk_dataset import mk_dataset
import pandas as pd

from collaboration_filtering.Collaboration_filtering_t import Collaboration_filtering
from Filter.Filter import Filter
from sentiment_analysis.proper_sentence_classifier import sentiment_analysis


def find_index(original_data, index):
    ret = original_data["공연명"].iloc[index]
    if not isinstance(ret, str):
        ret = "no_info"
    return ret


def recommend(condition):
    # 여기에 추가로 데이터 form 만드는 작업(전처리)
    # 나이, 성별, 날짜 range, 날씨를 선택하면 그 중에 긍정도가 높은 것들을 그 범위 안의 공연을 추천
    # 원하는 인자를 나이, 성별, 날짜 range 날씨를 선택하면

    # 날짜 filtering
    original_data: pd.DataFrame = pd.read_csv("processed_data.csv", encoding="utf-8")
    # print(original_data["공연명"])
    filtered_columns = ["성별", "연령", "장르명", "세부장르명", "공연지역명", "time", "date"]
    filtering_sample: pd.DataFrame = copy.deepcopy(original_data[filtered_columns])
    date_filterd_df: pd.DataFrame = Filter.date_filter(
        filtering_sample,
        input_start_date=202010,
        input_end_date=202012,
        input_start_time=1330,
        input_end_time=1600,
    )

    # 성별 filtering
    # date_sex_filtered_df:pd.DataFrame = Filter.sex_filter(date_filterd_df, input_sex = 0)

    # print(date_sex_filtered_df)
    # date_sex_filtered_df = date_sex_filtered_df.append({"index_name":{"공연지역명":4}}, ignore_index=True )
    dataset = date_filterd_df.to_dict(orient="index")
    # 필터링 다 된 user의 수
    USER_NUM: int = len(dataset)
    ##### 여기에 입력값을 넣으면 됩니다.#####
    ##### 여기에 입력값을 넣으면 됩니다.#####
    ##### 여기에 입력값을 넣으면 됩니다.#####
    ##### 여기에 입력값을 넣으면 됩니다.#####
    ##### 여기에 입력값을 넣으면 됩니다.#####
    # 입력 값이 dataset의 value로 들어가야 합니다
    dataset["index_name"] = condition
    similar_user_list: list = Collaboration_filtering.most_similar_users(
        dataset, "index_name", USER_NUM
    )
    similar_user_list.sort(key=lambda x: x[0], reverse=True)
    rank = []
    for i, user in enumerate(similar_user_list):
        if i >= 500:
            break
        rank.append(user)
    print(rank)
    musical_names: list = []

    # 여기서 인덱스만 받아서 dataset을 가져옴
    for similar, index in rank:
        musical_names.append(find_index(original_data, index))

    name_positive: list = []
    from Crwaler.Crwaler import Crwaler

    # 크롤러 시작
    musical_names = list(set(musical_names))
    print(musical_names)
    for index, musical_name in enumerate(musical_names):
        if musical_name == "no_info":
            continue
        if index > 5:
            break
        new_df = Crwaler.tis(musical_name)
        new_df3 = Crwaler.nav(musical_name)
        # new_df3 = Crwaler.youtube_comment_crwaler(musical_name)
        print(new_df3)
        new_df3.to_csv(f"save_{index}.csv", encoding="utf-8")
        print("aaa ", new_df3.columns)
        my_list = copy.deepcopy(new_df3["1"].to_list())
        positive_sum = 0

        for i, content in enumerate(my_list):
            positive_sum += sentiment_analysis(content)
            print(f"{i} {content}: {sentiment_analysis(content)}")
        name_positive.append((musical_name, positive_sum))

    name_positive.sort(key=lambda x: -x[1])
    print("추천 결과")
    print(name_positive)
    # print("추천 1위")
    # print(name_positive[0])
    # print("추천 2위")
    # print(name_positive[1])
    # 여기까지 순위 top 50인 애들 인덱스만 가져오고 가져온 index로  다시 mapping 해야한다.

    # pd1 = pd.read_csv('test_monte.csv',header=None)
    # print(pd1.columns)
    # print(pd1[1])

    return list(map(lambda x: x[0], name_positive[:5]))

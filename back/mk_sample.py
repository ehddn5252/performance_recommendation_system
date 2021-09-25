import pandas as pd
def mk_index_sample(sample_num:int=100000):
    data:pd.DataFrame= pd.read_csv("processed_data_0912.csv",encoding="utf-8")
    print(f" data read complete")
    print(data)
    print(f" =======")
    print(f" =======")

    print(data.head(5))
    data2 = data[:sample_num]

    data2.to_csv("mini100000_data.csv")

    print(f" data save complete")


mk_index_sample()
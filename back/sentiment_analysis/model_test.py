#pip install transformer pytorch
import pandas as pd
from proper_sentence_classifier import sentiment_analysis
pd1 = pd.read_csv('test_monte.csv',header=None)
print(pd1.columns)
print(pd1[1])
my_list = pd1[1].to_list()


with open('test_monte.txt','w') as f: 
    for i,content in enumerate(my_list):
        f.write(f'{i}. {pd1[1].iloc[i]} : {sentiment_analysis(content)}\n')
        print(f'{i} {content}: {sentiment_analysis(content)}')

'''
csv 판다스로 불러오고
column중에 글자가 있는 column만 가져와서 
맨 뒤에 .to_list를 치면 글자가 리스트에 담겨서 반환이 된다.
'''

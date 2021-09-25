import pandas as pd

class Filter:
	"""
	여기에 넣을 때는 dictionarya가 아닌 pandas dataframe 형으로 바꿔서 넣어줘야 함
	"""
	def __init__(self):
		pass

	@classmethod
	def date_filter(cls,dataset:pd.DataFrame,input_start_date:int=20160101,input_end_date:int=20210101,input_start_time:int=1330,input_end_time:int=2400):
		"""
		:desc:
		날짜와 시간에 따른 filter
		"""
		new_df = pd.DataFrame()
		for i in range(len(dataset.loc[:])):
			if input_start_date<=dataset["date"].iloc[i] and dataset["date"].iloc[i] <= input_end_date:
				if input_start_time <= dataset["time"].iloc[i] and dataset["time"].iloc[i]<= input_end_time:
					new_df = new_df.append(dataset[:].iloc[i])
		new_df.drop("date", axis = 1, inplace=True)
		new_df.drop("time", axis = 1, inplace=True)
		return new_df
	
	@classmethod
	def sex_filter(cls, dataset:pd.DataFrame, input_sex):
		"""
		:desc:
		성이 남자인지 여자인지에 따른 filter
		1 이면 남자 2면 여자
		"""
		new_df = pd.DataFrame()
		for i in range(len(dataset.loc[:])):
			current_sex = dataset["성별"].iloc[i]
			# 예외처리
			if current_sex == input_sex:
				new_df = new_df.append(dataset[:].iloc[i])
		
		new_df.drop("성별", axis=1, inplace=True)
		return new_df

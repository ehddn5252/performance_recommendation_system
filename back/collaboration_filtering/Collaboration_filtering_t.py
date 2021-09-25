
#!/usr/bin/env python
# Implementation of collaborative filtering recommendation engine
"""
여기에서 person이라는 것은 column 명이라고 생각하면 된다.

"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#from recommendation_data import dataset
#from collaborative_filtering.data_sample2 import dataset

import pandas as pd
from math import sqrt


class Collaboration_filtering:
	"""
	여기에 넣을 때는 딕셔너리 형으로 넣어야 함
	"""
	def __init__(self) -> None:
		pass

	@classmethod
	def similarity_score(cls, dataset:dict, person1:str,person2:str):
		# Returns ratio Euclidean distance score of person1 and person2 

		both_viewed = {}		# To get both rated items by person1 and person2
		for item in dataset[person1]:
			if item in dataset[person2]:
				both_viewed[item] = 1

			# Conditions to check they both have an common rating items	
			if len(both_viewed) == 0:
				return 0

			# Finding Euclidean distance 
			sum_of_eclidean_distance = []

			for item in dataset[person1]:
				if item in dataset[person2]:
					sum_of_eclidean_distance.append(pow(dataset[person1][item] - dataset[person2][item],2))
			sum_of_eclidean_distance = sum(sum_of_eclidean_distance)

			return 1/(1+sqrt(sum_of_eclidean_distance))

	@classmethod
	def pearson_correlation(cls, dataset:dict, person1: str, person2: str):
		"""
		:desc:
		피어슨 유사도 사람 1과 사람 2에 대한 피어슨 유사도를 return한다.

		:param person1: 사람1 string값
		:param person2: 사람2 string값
		:return: 사람 1과 사람 2에 대한 피어슨 유사도
		"""
		# To get both rated items
		both_rated = {}
		for item in dataset[person1]:
			if item in dataset[person2]:
				both_rated[item] = 1

		number_of_ratings = len(both_rated)		
		
		# Checking for number of ratings in common
		if number_of_ratings == 0:
			return 0

		# Add up all the preferences of each user
		person1_preferences_sum = sum([dataset[person1][item] for item in both_rated])
		person2_preferences_sum = sum([dataset[person2][item] for item in both_rated])

		# Sum up the squares of preferences of each user
		person1_square_preferences_sum = sum([pow(dataset[person1][item],2) for item in both_rated])
		person2_square_preferences_sum = sum([pow(dataset[person2][item],2) for item in both_rated])

		# Sum up the product value of both preferences for each item
		product_sum_of_both_users = sum([dataset[person1][item] * dataset[person2][item] for item in both_rated])

		# Calculate the pearson score
		numerator_value = product_sum_of_both_users - (person1_preferences_sum*person2_preferences_sum/number_of_ratings)
		denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum,2)/number_of_ratings) * (person2_square_preferences_sum -pow(person2_preferences_sum,2)/number_of_ratings))
		if denominator_value == 0:
			return 0
		else:
			r = numerator_value/denominator_value
			return r 

	@classmethod
	def most_similar_users(cls, dataset:dict, person, number_of_users:int):
		"""
		:desc:
		사람과 유저수
		"""

		# returns the number_of_users (similar persons) for a given specific person.
		scores = [(cls.pearson_correlation(dataset,person,other_person),other_person) for other_person in dataset if  other_person != person ]
		
		# Sort the similar persons so that highest scores person will appear at the first
		scores.sort()
		scores.reverse()
		return scores[0:number_of_users]

	@classmethod
	def user_reommendations(cls, dataset, person):
		"""
		"""

		# Gets recommendations for a person by using a weighted average of every other user's rankings
		totals = {}
		simSums = {}
		rankings_list =[]
		for other in dataset:
			# don't compare me to myself
			if other == person:
				continue
			sim = cls.pearson_correlation(dataset,person,other)

			# ignore scores of zero or lower
			if sim <=0: 
				continue
			for item in dataset[other]:

				# only score movies i haven't seen yet
				if item not in dataset[person] or dataset[person][item] == 0:

				# Similrity * score
					totals.setdefault(item,0)
					totals[item] += dataset[other][item]* sim
					# sum of similarities
					simSums.setdefault(item,0)
					simSums[item]+= sim

		# Create the normalized list
		rankings = [(total/simSums[item],item) for item,total in totals.items()]
		rankings.sort()
		rankings.reverse()
		# returns the recommended items
		recommendataions_list = [recommend_item for score,recommend_item in rankings]
		return recommendataions_list

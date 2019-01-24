# coding:utf-8 
'''
created on 2019/1/18

@author:sunyihuan
'''
# from recommendation_data import dataset
from math import sqrt

dataset = {
    'Lisa Rose': {'Lady in the Water': 2.5,
                  'Snakes on a Plane': 3.5,
                  'Just My Luck': 3.0,
                  'Superman Returns': 3.5,
                  'You, Me and Dupree': 2.5,
                  'The Night Listener': 3.0},
    'Gene Seymour': {'Lady in the Water': 3.0,
                     'Snakes on a Plane': 3.5,
                     'Just My Luck': 1.5,
                     'Superman Returns': 5.0,
                     'The Night Listener': 3.0,
                     'You, Me and Dupree': 3.5},

    'Michael Phillips': {'Lady in the Water': 2.5,
                         'Snakes on a Plane': 3.0,
                         'Superman Returns': 3.5,
                         'The Night Listener': 4.0},
    'Claudia Puig': {'Snakes on a Plane': 3.5,
                     'Just My Luck': 3.0,
                     'The Night Listener': 4.5,
                     'Superman Returns': 4.0,
                     'You, Me and Dupree': 2.5},
    'Mick LaSalle': {'Lady in the Water': 3.0,
                     'Snakes on a Plane': 4.0,
                     'Just My Luck': 2.0,
                     'Superman Returns': 3.0,
                     'The Night Listener': 3.0,
                     'You, Me and Dupree': 2.0},
    'Jack Matthews': {'Lady in the Water': 3.0,
                      'Snakes on a Plane': 4.0,
                      'The Night Listener': 3.0,
                      'Superman Returns': 5.0,
                      'You, Me and Dupree': 3.5},
    'Toby': {'Snakes on a Plane': 4.5,
             'You, Me and Dupree': 1.0,
             'Superman Returns': 4.0}}


def similarity_score(person1, person2):
    # Returns ratio Euclidean distance score of person1 and person2

    both_viewed = {}  # To get both rated items by person1 and person2

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
                sum_of_eclidean_distance.append(pow(dataset[person1][item] - dataset[person2][item], 2))
        sum_of_eclidean_distance = sum(sum_of_eclidean_distance)

        return 1 / (1 + sqrt(sum_of_eclidean_distance))


def pearson_correlation(person1, person2):
    # To get both rated items
    both_rated = {}  # 获取目标的keys
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
    person1_square_preferences_sum = sum([pow(dataset[person1][item], 2) for item in both_rated])
    person2_square_preferences_sum = sum([pow(dataset[person2][item], 2) for item in both_rated])

    # Sum up the product value of both preferences for each item
    product_sum_of_both_users = sum([dataset[person1][item] * dataset[person2][item] for item in both_rated])

    # Calculate the pearson score
    numerator_value = product_sum_of_both_users - (
            person1_preferences_sum * person2_preferences_sum / number_of_ratings)
    denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum, 2) / number_of_ratings) * (
            person2_square_preferences_sum - pow(person2_preferences_sum, 2) / number_of_ratings))
    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        return r


def most_similar_users(person, number_of_users):
    # returns the number_of_users (similar persons) for a given specific person.
    scores = [(pearson_correlation(person, other_person), other_person) for other_person in dataset if
              other_person != person]

    # Sort the similar persons so that highest scores person will appear at the first
    scores.sort()
    scores.reverse()
    return scores[0:number_of_users]


def user_reommendations(person):
    # Gets recommendations for a person by using a weighted average of every other user's rankings
    totals = {}
    simSums = {}

    for other in dataset:
        # don't compare me to myself
        if other == person:
            continue
        print(other)
        sim = pearson_correlation(person, other)
        print(">>>>>>>", sim)

        # ignore scores of zero or lower
        if sim <= 0:
            continue
        for item in dataset[other]:

            # only score movies i haven't seen yet
            if item not in dataset[person] or dataset[person][item] == 0:
                # Similrity * score
                totals.setdefault(item, 0)
                totals[item] += dataset[other][item] * sim
                # sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # Create the normalized list

    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    print("rankings", rankings)
    rankings.sort()
    rankings.reverse()
    # returns the recommended items
    recommendataions_list = [recommend_item for score, recommend_item in rankings]
    return recommendataions_list


print(user_reommendations('Toby'))

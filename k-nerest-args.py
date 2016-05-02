import csv
import random
import math
import operator
from collections import Counter
import time

#set the random number generator seed so that the same values go into the test set every time
random.seed("I'm a seed")

def euclidian_distance(item1, item2, dimensions):
    distance = 0
    for x in range(dimensions):
        distance += math.pow(item1[x] - item2[x], 2)
    return math.pow(distance, 0.5)


def getNeighbors(trainingSet, testpoint, k):
    distances = []
    for i in trainingSet:
        distances.append((euclidian_distance(testpoint, i, len(i) - 1), i))
    distances.sort(key=lambda tup: tup[0])
    return distances[0:k]


def getAllNeighbors(trainingSet, testpoint):
    distances = []
    for i in trainingSet:
        distances.append((euclidian_distance(testpoint, i, len(i) - 1), i))
    distances.sort(key=lambda tup: tup[0])
    return distances


def vote(neighbors):
    labels = []
    for i in neighbors:
        labels.append(i[1][-1])
    return Counter(labels).most_common(1)[0][0]
    

def loadDataset(fine_name, split, trainingSet, testSet, columns_to_exclude = []):
    with open(fine_name, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        headers.append(dataset.pop(0))
        n_attributes = len(dataset[0]) - 1
        for x in range(len(dataset)-1):
            for y in range(n_attributes):
                if not y in columns_to_exclude:
                    try:
                        dataset[x][y] = float(dataset[x][y])
                    except ValueError:
                        date_components = dataset[x][y].replace("-"," ").replace(":"," ").split(" ")
                        for i in range(len(date_components)):
                            dataset[x][y] = int(date_components[i]) * 10**(len(date_components) - i)
                else:
                    dataset[x][y] = 0.0
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])


def get_error_rate(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct/float(len(testSet)))*100.0


def get_accuracy(k = 11, args_to_exclude=[]):
    trainingSet = []
    testSet = []
    split = 0.90
    loadDataset('datatraining.txt', split, trainingSet, testSet, columns_to_exclude = args_to_exclude)
    
    predictions = []
    for i in testSet:
        predictions.append(vote(getNeighbors(trainingSet, i, k)))
#     print(predictions[len(predictions) - 1])
    return(get_error_rate(testSet, predictions))

headers = []



import itertools
import numpy as np

collumns = list(np.linspace(0, 5, 6))

for length in range(1, 7):
    for excluded in itertools.combinations(collumns, length):
        print("trying arguments " + str(i))
        k = 11
        running_total = 0
        n_iterations = 1
        for j in range(n_iterations):
            running_total += get_accuracy(k=k, args_to_exclude = excluded)


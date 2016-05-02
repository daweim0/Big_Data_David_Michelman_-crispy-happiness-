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
    

def loadDataset(fine_name, split, trainingSet, testSet):
    with open(fine_name, 'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        headers.append(dataset.pop(0))
        n_attributes = len(dataset[0]) - 1
        for x in range(len(dataset)-1):
            for y in range(n_attributes):
                try:
                    dataset[x][y] = float(dataset[x][y])
                except ValueError:
                    date_components = dataset[x][y].replace("-"," ").replace(":"," ").split(" ")
                    for i in range(len(date_components)):
                        dataset[x][y] = int(date_components[i]) * 10**(len(date_components) - i)
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


def get_accuracy(k = 11):
    trainingSet = []
    testSet = []
    split = 0.90
    loadDataset('datatraining.txt', split, trainingSet, testSet)
    
    predictions = []
    for i in testSet:
        predictions.append(vote(getNeighbors(trainingSet, i, k)))
#     print(predictions[len(predictions) - 1])
    return(get_error_rate(testSet, predictions))


headers = []

print("hi")
n_iterations = 8
for k_val_raw in range(2, 160, 2):
    k_val = math.floor(k_val_raw * math.log(k_val_raw))
    if k_val % 2 == 0 or k_val == 0:
        k_val += 1
#     print(k_val)
    total = 0.0
    start_time = time.time()
    for i in range(n_iterations):
        partial_sum = get_accuracy(k=k_val)
        total += partial_sum
    print('    average accuracy with k=' + str(k_val) + " is " + str(total/n_iterations) + "%")
    if k_val > 8001:
        break


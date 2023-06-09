# Project: lab-2
# File: main.py
# Created by 2 brigade on 08.06.2023
# Description: This code generates random numbers from a normal distribution, 
# calculates the mean, the standard deviation, and builds confidence intervals 
# for the mathematical expectation and the standard deviation. 
# It displays the result for each array and confidence percentage, 
# and compares the confidence intervals by size and confidence percentage.
# 

import numpy as np
import scipy.stats as stats

size = 147
mean = 0
variance = 1.4

np.random.seed(0)

basic = np.random.normal(loc=mean, scale=np.sqrt(variance), size=size)

arrays = [basic]
for i in range(1, 7):
    arrays.append(arrays[i - 1][:len(arrays[i - 1]) // 2])
percents = [0.995, 0.99, 0.975, 0.98, 0.95, 0.9, 0.5, 0.2]

def average(array):
    return np.mean(array)

def devSq(arr):
    return np.var(arr, ddof=1)

def intervalExpectation(arr, t, mean, s):
    n = len(arr)
    error = t * s / np.sqrt(n)
    return [mean - error, mean + error]

def intervalSquare(arr, chi1, chi2, s):
    n = len(arr)
    left = np.sqrt((n - 1) * (s ** 2) / chi1)
    right = np.sqrt((n - 1) * (s ** 2) / chi2)
    return [left, right]


# Commented code below is a pure python implementation of the same functions

# Функція для обчислення середнього значення масиву
# def average(array):
#     sum = 0
#     for i in range(len(array)):
#         sum += array[i]
#     return sum / len(array)

# # Функція для обчислення квадрату відхилення
# def devSq(arr):
#     sum = 0
#     for i in range(len(arr)):
#         sum += arr[i] ** 2
#     return 1 / (len(arr) - 1) * sum - average(arr) ** 2

# # Функція для обчислення довірчого інтервалу для математичного сподівання
# def intervalExpectation(arr, t, mean, s):
#     n = len(arr)
#     left = mean - (t * s / (n ** 0.5))
#     right = mean + (t * s / (n ** 0.5))
#     return [left, right]

# # Функція для обчислення довірчого інтервалу для середнього квадратичного відхилення
# def intervalSquare(arr, chi1, chi2, s):
#     n = len(arr)
#     left = math.sqrt((n - 1) * (s ** 2) / chi1)
#     right = math.sqrt((n - 1) * (s ** 2) / chi2)
#     return [left, right]

def T_value(percent, freedom):
    return np.abs(stats.t.ppf(percent, freedom))

def Xi_value(percent, freedom):
    return stats.chi2.ppf(percent, freedom)

# Функція для обчислення довірчих інтервалів для заданого масиву та відсотку довіри
def calculate(basicArray=None, percent=0.95):
    if basicArray is None:
        size = 147
        mean = 0
        variance = 1.4
        np.random.seed(0)
        basicArray = np.random.normal(loc=mean, scale=np.sqrt(variance), size=size)

    size = len(basicArray)
    t = T_value((1 - percent) / 2, size - 1)
    square = devSq(basicArray) ** 0.5
    avrg = average(basicArray)

    # Обчислення довірчих інтервалів для математичного сподівання
    left1, right1 = intervalExpectation(basicArray, t, avrg, square)

    # Обчислення довірчих інтервалів для середньоквадратичного відхилення
    xi2 = Xi_value((1 - percent) / 2, size - 1)
    xi1 = Xi_value(1 - (1 - percent) / 2, size - 1)

    left2, right2 = intervalSquare(basicArray, xi1, xi2, square)

    result = {
        'size': size, 
        'percent': percent, 
        'average': avrg, 
        'sq': square, 
        'expect': [left1, right1],
        'square': [left2, right2], 
        't': t, 
        'xi1': xi1, 
        'xi2': xi2}
    return result

def output(result, size):
    print("Number of elements: ", size)
    print("Percentage: ", result['percent'])
    print('t: ', result['t'])
    print('xi1: ', result['xi1'])
    print('xi2: ', result['xi2'])
    print("Average value: ", round(result['average'], 4))
    print("Standard deviation ^1: ", round(result['sq'] ** 0.5, 4), '^2 ', round(result['sq'], 4))
    print("Mathematical expectation:")
    print(result['expect'][0], " < u < ", result['expect'][1])
    print("\nStandard deviation:")
    print(result['square'][0], " < o < ", result['square'][1])


# Функція для порівняння довірчих інтервалів для різних масивів та відсотків довіри
def comparison(arrays, percents, sortBy='percent', reverse=True):
    result = []
    for array in arrays:
        for percent in percents:
            result.append(calculate(array, percent))

    result.sort(key=lambda x: x[sortBy], reverse=reverse)

    print("{:<10} {:<10} {:<50} {:<20}".format('Size', 'Percent', 'Expectation', 'SQ'))

    for data in result:
        size = data['size']
        percent = data['percent']
        expectation = f"{data['expect'][0]} < u < {data['expect'][1]}"
        sq = f"{data['square'][0]} < o < {data['square'][1]}"
        print("{:<10} {:<10} {:<50} {:<30}".format(size, percent, expectation, sq))


print(Xi_value((1 - 0.9) / 2, 100))
output(calculate(basic, percent=0.95), size)
comparison(arrays, percents, sortBy='size')

# Project: lab-2
# File: main.py
# Created by 2 brigade on 08.06.2023
# Description: This code generates random numbers from a normal distribution, 
# calculates the mean, the standard deviation, and builds confidence intervals 
# for the mathematical expectation and the standard deviation. 
# It displays the result for each array and confidence percentage, 
# and compares the confidence intervals by size and confidence percentage.
# 

import math
import numpy as np
import scipy

# Задання розміру, середнього значення та дисперсії
size = 147
mean = 0
variance = 1.4
np.random.seed(0)

# Генерація випадкових чисел з нормального розподілу
basic = np.random.normal(loc=mean, scale=np.sqrt(variance), size=size)

# Розбиття масиву на підмасиви з половини розміру попереднього масиву
arr2 = basic[:len(basic) // 2]
arr4 = basic[:len(arr2) // 2]
arr8 = basic[:len(arr4) // 2]
arr16 = basic[:len(arr8) // 2]
arr32 = basic[:len(arr16) // 2]
arr64 = basic[:len(arr32) // 2]

# Створення масиву підмасивів для порівняння довірчих інтервалів
arrays = [basic, arr2, arr4, arr8, arr16, arr32, arr64]
percents = [0.995, 0.99, 0.975, 0.98, 0.95, 0.9, 0.5, 0.2]

# Функція для обчислення середнього значення масиву
def average(array):
    sum = 0
    for i in range(len(array)):
        sum += array[i]
    return sum / len(array)

# Функція для обчислення квадрату відхилення
def devSq(arr):
    sum = 0
    for i in range(len(arr)):
        sum += arr[i] ** 2
    return 1 / (len(arr) - 1) * sum - average(arr) ** 2

# Функція для обчислення довірчого інтервалу для математичного сподівання
def intervalExpectation(arr, t, mean, s):
    n = len(arr)
    left = mean - (t * s / (n ** 0.5))
    right = mean + (t * s / (n ** 0.5))
    return [left, right]

# Функція для обчислення довірчого інтервалу для середнього квадратичного відхилення
def intervalSquare(arr, chi1, chi2, s):
    n = len(arr)
    left = math.sqrt((n - 1) * (s ** 2) / chi1)
    right = math.sqrt((n - 1) * (s ** 2) / chi2)
    return [left, right]

# Функція для обчислення значення t-статистики
def T_value(percent, freedom):
    return abs(scipy.stats.t.ppf(percent, freedom))

# Функція для обчислення значення t-статистики
def Xi_value(percent, freedom):
    return scipy.stats.chi2.ppf(percent, freedom)

# Функція для обчислення довірчих інтервалів для заданого масиву та відсотку довіри
def calculate(basicArray=[], percent=0.95):
    if len(basicArray) == 0:
        size = 147
        mean = 0
        variance = 1.4
        np.random.seed(0)
        basicArray = np.random.normal(loc=mean, scale=np.sqrt(variance), size=size)
    size = len(basicArray)
    t = T_value((1 - percent) / 2, size-1)
    s = devSq(basicArray) ** 0.5
    avrg = average(basicArray)

    # Обчислення довірчих інтервалів для математичного сподівання
    left1, right1 = intervalExpectation(basicArray, t, avrg, s)

    # Обчислення довірчих інтервалів для середньоквадратичного відхилення
    xi2 = Xi_value((1-percent)/2, size - 1)
    xi1 = Xi_value(1-(1 - percent)/2, size - 1)
    left2, right2 = intervalSquare(basicArray, xi1, xi2, s)

    result = {'size': size, 'percent': percent, 'average': avrg, 'sq': s, 'expect': [left1, right1],
           'square': [left2, right2], 't':t, 'xi1':xi1, 'xi2':xi2}
    return result

# Функція для виведення результатів
def output(result):
    print("Count of elements: " + str(size))
    print("Percentage: " + str(result.get('percent')))
    print('t: ' + str(result.get('t')))
    print('xi1: ' + str(result.get('xi1')))
    print('xi2: ' + str(result.get('xi2')))
    print("Average value: " + str(round(result.get('average'), 4)))
    print("Standard deviation ^1: " + str(round(result.get('sq') ** 0.5, 4)) + ' ^2 ' + str(round(result.get('sq'), 4)))
    print("Mathematical expectatiom:")
    print(str(result.get('expect')[0]) + " < u < " + str(result.get('expect')[1]))
    print("\nStandard deviation:")
    print(str(result.get('square')[0]) + " < o < " + str(result.get('square')[1]))

# Функція для порівняння довірчих інтервалів для різних масивів та відсотків довіри
def comparison(arrays, percents, sortBy='percent', reverse=True):
    result = []
    for array in arrays:
        for percent in percents:
            result.append(calculate(array, percent))

    result.sort(key=lambda x: x.get(sortBy), reverse=reverse)

    print("{:<10} {:<10} {:<50} {:<20}".format('Size', 'Percent', 'Expectation', 'SQ'))

    for data in result:
        size = data.get('size')
        percent = data.get('percent')
        expectation = str(data.get('expect')[0]) + " < u < " + str(data.get('expect')[1])
        sq = str(data.get('square')[0]) + " < o < " + str(data.get('square')[1])
        print("{:<10} {:<10} {:<50} {:<30}".format(size, percent, expectation, sq))


print(Xi_value((1-0.9)/2, 100))
output(calculate(basic, percent=0.95))
comparison(arrays, percents, sortBy='size')
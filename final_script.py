# Andrew Lallos
# WorldQuant University
# WQU605 - Programming in Python 1
# Final Project, Due 7/18/2017

# The data used from this project was obtained from: 
# http://www.nasdaq.com/symbol/aapl/historical
# The time period used is monthly from 8/2016 - 3/2017 -- 8 time periods
# Pricing/dates are from the first trading day of each respective month/period.

# Import any necessary libraries

import pandas as pd
import matplotlib.pyplot as plt
import math

# This class will allow us to more easily use our datasets in later projects

class Data(object):

    def __init__(self,name):
        self.name = name

    def dataset(self, data):
        self.data = data

# Building our expontential smoothing formula to use with the users' desired data

# smoothing formula = f_t+1 = aY_t + (1 - a)F_t

def expontential_smoothing(series, alpha):
    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result

#The following check prompts the user to ensure their data is formatted properly

print("Before we begin, please ensure you're dataset has the proper formatting:\n")
print("Column header for price sholud be named: 'value'")

test_stock = Data('Security')

#Ask our user for the their desired dataset file path

question = input('Please enter the file path for your desired data:\n')
test_stock.data = pd.read_csv(question)
print('\n Here are the first 5 rows of your data:\n \n', test_stock.data[:5])
alpha = float(input('\nWhat alpha value would you like to use? '))
print("\nYou've chosen %.2f as your alpha value" % alpha)

exp_smooth1 = expontential_smoothing(test_stock.data['value'], alpha)

plt.plot(test_stock.data)
plt.plot(exp_smooth1)
plt.ylabel('Stock Price')
plt.show()

correct_plot = input("Does this plot look correct\n")

if correct_plot == "yes":
    print("Great! Mission Accomplished!")
    print("Now let's have a look at some Linear Regression.\n")
else:
    fix_plot = float(input("What alpha would you like to use then?\n"))
    new_alpha = expontential_smoothing(test_stock.data['value'], fix_plot)
    plt.plot(test_stock.data)
    plt.plot(new_alpha)
    plt.ylabel('Stock Price')
    plt.show()

    follow_up = input("How about now?\n")

    if follow_up == "yes":
        print("Awesome! I knew we'd get it.\n")
        print("Now let's have a look at some Linear Regression.\n")
    else:
        print("Let's take one last shot at updating your alpha...\n")
        third_shot = float(input("Third time's a charm...choose your alpha wisely:\n"))
        third_alpha = expontential_smoothing(test_stock.data['value'], third_shot)
        plt.plot(test_stock.data)
        plt.plot(third_alpha)
        plt.ylabel('Stock Price')
        plt.show()

        last_check = input("Finger's crossed -- does it look correct?\n")

        if last_check == "yes":
            print("\nFinally!")
            print("Now let's have a look at some Linear Regression.\n")
        else:
            print("Hmmm...you win some you lose some. Back to the drawing board.\n")


            
# Linear regression formula:
# y = b0 + b1 * x
# b1 = sum((x(i) - mean(x)) * (y(i) - mean(y))) / sum( (x(i) - mean(x))^2)
# b0 = mean(y) - b1 * mean(x)

# First, let's transform our data into something a little more easily useable

dataset = [1,106.05], [2,106.73],[3,112.52],[4,111.49],[5,109.49],[6,116.15],[7,128.75],[8,139.79]
list1 = list([1,2,3,4,5,6,7,8])
list2 = ([106.05,106.73,112.52,111.49,109.49,116.15,128.75,139.79])

# create mean function
def mean(values):
    return sum(values) / float(len(values))

# create variance function

def variance(values, mean):
    return sum([(x-mean)**2 for x in values])

#create covariance function

def covariance(x, mean_x, y, mean_y):
    covar = 0.0
    for i in range(len(x)):
        covar += (x[i] - mean_x) * (y[i] - mean_y)
        return covar

# create standard deviation function

def Sample_Standard_Deviation(L1):
    Mean_of_L1 = mean(L1)
    tsum = 0
    for x in range(0, len(L1)):
        tsum = tsum + (L1[x] - Mean_of_L1) ** 2
    return math.sqrt(tsum / (len(L1) - 1))

# Calculate coefficients

def coefficients(dataset):
    x = [row[0] for row in dataset]
    y = [row[1] for row in dataset]
    x_mean, y_mean = mean(x), mean(y)
    b1 = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
    b0 = y_mean - b1 * x_mean
    return [b0, b1]

b0, b1 = coefficients(dataset)

print("Our value for b0=%.3f and b1=%.3f\n" % (b0, b1))

print("Therefore, our regression equation is: y = %.3f + %.3f * x\n" % (b0, b1))

time9_predict = (b0 + (b1 * 9))

print("With our equation determined, we now can predict that at Time 9, our price will be: %.3f.\n" % time9_predict)

def Correlation_Coefficient(L1,L2):
    meanx = mean(L1)
    meany = mean(L2)
    stdx = Sample_Standard_Deviation(L1)
    stdy = Sample_Standard_Deviation(L2)
    tsum = 0
    for idx in range(0,len(L1)):
        tsum = tsum + ((L1[idx] - meanx)/stdx) * ((L2[idx] - meany) / stdy)
    return tsum / (len(L1) - 1)

corr_coef = Correlation_Coefficient(list1, list2)

print("Lastly, we see that our correlation coefficient, or R^2 value, is: %.3f.\n" % corr_coef)

if corr_coef <= 0.75:
    print ("Given this, we can see that our Linear Regression model is not a great fit.\n")
else:
    print("Given this, we can sumise that our Linear Regression model is a good fit.\n")

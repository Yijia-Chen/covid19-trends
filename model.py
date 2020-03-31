import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import sys
import os
import shutil
import csv

no_read = ["countries.csv"]

"""Return a dictionary of countries whose values are two-dimensional arrays."""
def get_countries(path):
    # can potentially simplify using pandas
    (_, _, filenames) = next(os.walk(path))
    countries = dict()
    for fname in filenames:
        data = [[], []]
        if fname not in no_read:
            with open(path + '/' + fname, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    data[0].append(str(row[0]))
                    data[1].append(int(row[1]))
            countries[fname[:-4]] = data
    return countries

"""Plot total cases of each country."""
def plot(countries, option='regular'):
    if os.path.isdir("plots"):
        shutil.rmtree("plots")
    os.mkdir("plots")
    print("plotting number of cases observed so far...")

    for (country, data) in countries.items():
        if option == 'regular':
            plt.plot(data[0], data[1])
            plt.title("Total coronavirus cases in %s" % country)
            plt.xlabel("Date")
            plt.ylabel("Number of cases")
            plt.savefig("plots/%s.png" % country)
            plt.close()
        elif option == 'log':
            plt.plot(data[0], data[1])
            plt.yscale('log')
            plt.title("Total coronavirus cases in %s" % country)
            plt.xlabel("Date")
            plt.ylabel("Number of cases")
            plt.savefig("plots/%s_log.png" % country)
            plt.close()
        else:
            print("Plot form not supported.")

"""Fits a logistic model to each country and predict number of cases in coming days."""
def fit(countries, future_days):
    if os.path.isdir("preds"):
        shutil.rmtree("preds")
    os.mkdir("preds")
    print("predicting number of cases in the next %d days..." % future_days)

    params = dict()
    for i, (country, data) in enumerate(countries.items()):
        # fit logistic model
        def logistic(t, a, b, c):
            return c / (1 + a * np.exp(-b*t))
        bounds = (0, [100000., 3., 10000000.])
        p0 = np.random.randint(low=0.1, high=2.9, size=3)
        Y = data[1]
        X = range(len(Y))
        X_ext = range(len(Y) + future_days)
        (a, b, c), _ = curve_fit(logistic, X, Y, bounds=bounds, p0=p0)
        params[country] = (a, b, c)

        # plot the fit
        plt.plot(X_ext, [logistic(xi, a, b, c) for xi in X_ext])
        plt.scatter(X, Y)
        plt.title("Logistic Model vs. Real Observations of Coronavirus in %s" % country)
        plt.legend(['logistic model', 'real data'])
        plt.xlabel("Date since beginning")
        plt.ylabel("Number of cases")
        plt.savefig("preds/%s_predictions.png" % country)
        plt.close()
    
    return params

if __name__ == '__main__':
    argc = len(sys.argv)
    assert argc == 1 or argc == 2
    future_days = int(sys.argv[1]) if argc == 2 else 90 # default choice is 90 days
    countries = get_countries('data')
    plot(countries)
    fit(countries, future_days)

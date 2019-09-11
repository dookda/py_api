from sqlalchemy import create_engine
import numpy as np
from scipy import stats
from flask_restful import Resource, Api, reqparse


from math import sqrt
from numpy.random import seed
from numpy.random import randn
from numpy import mean
from scipy.stats import sem
from scipy.stats import t
from scipy import stats


class DbUtils:
    db_string = "postgresql+psycopg2://postgres:1234@localhost/pro40"

    def createTable(self):
        db = create_engine(self.db_string)
        db.execute(
            "CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")

    def addNewFilm(self, title, director, year):
        db_string = "postgresql+psycopg2://postgres:1234@localhost/pro40"
        db = create_engine(db_string)
        db.execute(
            "INSERT INTO films(title, director, year) VALUES (%s,%s, %s)", title, director, year)

    def getFilms(self):
        db_string = "postgresql+psycopg2://postgres:1234@localhost/pro40"
        db = create_engine(db_string)
        films = db.execute("SELECT * FROM accident")
        return films


class stat:
    def ttest(self):
        N = 10
        # Gaussian distributed data with mean = 2 and var = 1
        a = np.random.randn(N) + 2
        # Gaussian distributed data with with mean = 0 and var = 1
        b = np.random.randn(N)

        # For unbiased max likelihood estimate we have to divide the var by N-1, and therefore the parameter ddof = 1
        var_a = a.var(ddof=1)
        var_b = b.var(ddof=1)

        # std deviation
        s = np.sqrt((var_a + var_b)/2)
        s

        # Calculate the t-statistics
        t = (a.mean() - b.mean())/(s*np.sqrt(2/N))

        # Compare with the critical t-value
        # Degrees of freedom
        df = 2*N - 2

        # p-value after comparison with the t
        p = 1 - stats.t.cdf(t, df=df)

        print("t = " + str(t))
        print("p = " + str(2*p))
        # You can see that after comparing the t statistic with the critical t value (computed internally) we get a good p value of 0.0005 and thus we reject the null hypothesis and thus it proves that the mean of the two distributions are different and statistically significant.

        # Cross Checking with the internal scipy function
        t2, p2 = stats.ttest_ind(a, b)
        print("t = " + str(t2))
        print("p = " + str(p2))
        return p2

    def linregress(self, x, y):
        # calculate the p-value
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        # return everything
        return slope, intercept, r_value, p_value, std_err

    def independent_ttest(self, data1, data2, alpha):
        # calculate means
        mean1, mean2 = mean(data1), mean(data2)
        # calculate standard errors
        se1, se2 = sem(data1), sem(data2)
        # standard error on the difference between the samples
        sed = sqrt(se1**2.0 + se2**2.0)
        # calculate the t statistic
        t_stat = (mean1 - mean2) / sed
        # degrees of freedom
        df = len(data1) + len(data2) - 2
        # calculate the critical value
        cv = t.ppf(1.0 - alpha, df)
        # calculate the p-value
        p = (1.0 - t.cdf(abs(t_stat), df)) * 2.0
        # return everything
        return t_stat, df, cv, p

    def dependent_ttest(self, data1, data2, alpha):
        # calculate means
        mean1, mean2 = mean(data1), mean(data2)
        # number of paired samples
        n = len(data1)
        # sum squared difference between observations
        d1 = sum([(data1[i]-data2[i])**2 for i in range(n)])
        # sum difference between observations
        d2 = sum([data1[i]-data2[i] for i in range(n)])
        # standard deviation of the difference between means
        sd = sqrt((d1 - (d2**2 / n)) / (n - 1))
        # standard error of the difference between the means
        sed = sd / sqrt(n)
        # calculate the t statistic
        t_stat = (mean1 - mean2) / sed
        # degrees of freedom
        df = n - 1
        # calculate the critical value
        cv = t.ppf(1.0 - alpha, df)
        # calculate the p-value
        p = (1.0 - t.cdf(abs(t_stat), df)) * 2.0
        # return everything
        return t_stat, df, cv, p

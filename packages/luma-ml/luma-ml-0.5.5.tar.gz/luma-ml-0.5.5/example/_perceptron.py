import __local__
from luma.neural.perceptron import PerceptronClassifier, PerceptronRegressor
from luma.visual.result import DecisionRegion

from sklearn.datasets import make_blobs
import numpy as np
import matplotlib.pyplot as plt


X, y = make_blobs(n_samples=500, centers=5, random_state=10)

per = PerceptronClassifier()
per.fit(X, y)

DecisionRegion(per, X, y,).plot(show=True)

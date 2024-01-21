import __local__
from luma.ensemble.vote import VotingRegressor
from luma.regressor.neighbors import KNNRegressor
from luma.regressor.poly import PolynomialRegressor
from luma.regressor.svm import KernelSVR
from luma.regressor.tree import DecisionTreeRegressor

import matplotlib.pyplot as plt
import numpy as np


n_samples = 100

X = np.linspace(-3, 3, n_samples)
y = np.sin(X) + 0.05 * np.random.normal(size=n_samples)

X = X.reshape(-1, 1)
noise_indices = np.random.choice(n_samples, size=n_samples // 2)
y[noise_indices] += 0.2 * np.random.normal(size=n_samples // 2)

vote = VotingRegressor(estimators=[KNNRegressor(n_neighbors=5),
                                   PolynomialRegressor(degree=3),
                                   KernelSVR(C=0.1,
                                             gamma=1.0,
                                             learning_rate=0.001,
                                             max_iter=1000,
                                             kernel='rbf'),
                                   DecisionTreeRegressor(max_depth=5,
                                                         min_samples_split=2)])

vote.fit(X, y)

models = [*vote, vote]
preds = [model.predict(X) for model in models]

fig = plt.figure(figsize=(7, 5))
for i, (pred, model) in enumerate(zip(preds, models)):
    if i < 4: 
        plt.plot(X, pred, 
                 label=type(model).__name__ + f' - {model.score(X, y):.3f}', 
                 linestyle='--', 
                 alpha=0.5)
        plt.fill_between(X.flatten(), pred, preds[-1], alpha=0.1)
    else: 
        plt.plot(X, pred, label=type(model).__name__, linewidth=2)

plt.scatter(X, y, c='black', s=5, label='Original Data')
plt.xlabel('x')
plt.ylabel('y')
plt.title(f'Voting Regressor [MSE: {vote.score(X, y):.4f}]')
plt.legend()
plt.tight_layout()
plt.show()

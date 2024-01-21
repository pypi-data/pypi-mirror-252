import __local__
from luma.ensemble.boost import AdaBoostRegressor
from luma.regressor.tree import DecisionTreeRegressor

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

X = np.linspace(-3, 3, 100)
y = np.sin(X) + 0.02 * np.random.normal(size=100)

X = X.reshape(-1, 1)
y[np.random.choice(100, size=50)] += 0.25 * np.random.normal(size=50)

ada = AdaBoostRegressor(n_estimators=100,
                        learning_rate=0.1,
                        loss='linear')

ada.fit(X, y)
ada_pred = ada.predict(X)

tree = DecisionTreeRegressor(max_depth=3)

tree.fit(X, y)
tree_pred = tree.predict(X)

plt.scatter(X, y, c='black', s=10)

plt.plot(X, tree_pred, linewidth=2, color='hotpink', label=f'{type(tree).__name__}: {tree.score(X, y):.4f}')
plt.fill_between(X.flatten(), tree_pred, np.sin(X).flatten(), color='hotpink', alpha=0.2)

plt.plot(X, ada_pred, linewidth=2, color='dodgerblue', label=f'{type(ada).__name__}: {ada.score(X, y):.4f}')
plt.fill_between(X.flatten(), ada_pred, np.sin(X).flatten(), color='dodgerblue', alpha=0.2)

plt.title(f'AdaBoost Regression')
plt.legend()
plt.tight_layout()
plt.show()

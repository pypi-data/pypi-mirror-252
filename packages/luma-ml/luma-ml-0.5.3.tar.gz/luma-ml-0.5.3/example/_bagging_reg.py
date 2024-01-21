import __local__
from luma.ensemble.bagging import BaggingRegressor
from luma.regressor.tree import DecisionTreeRegressor
from luma.visual.result import DecisionRegion

import matplotlib.pyplot as plt
import numpy as np


n_samples = 100

X = np.linspace(-3, 3, n_samples)
y = np.sin(X) + 0.05 * np.random.normal(size=n_samples)

X = X.reshape(-1, 1)
noise_indices = np.random.choice(n_samples, size=n_samples // 2)
y[noise_indices] += 0.2 * np.random.normal(size=n_samples // 2)

bag = BaggingRegressor(base_estimator=DecisionTreeRegressor(max_depth=5),
                       n_estimators=100,
                       max_samples=1.0,
                       max_features=1.0,
                       bootstrap=True,
                       bootstrap_feature=False)

bag.fit(X, y)

fig = plt.figure(figsize=(10, 5))
ax_1 = fig.add_subplot(1, 2, 1)
ax_2 = fig.add_subplot(1, 2, 2)

scores = [est.score(X, y) for est, _ in bag]
scores.append(bag.score(X, y))

X_range = range(bag.n_estimators + 1)
ax_1.plot(X_range, scores, color='dodgerblue')
ax_1.plot(X_range, [np.mean(scores)] * len(X_range), linestyle='--', label='Mean MSE of Estimators')
ax_1.plot(X_range, [bag.score(X, y)] * len(X_range), linestyle='-.', label='MSE of Bagging Regressor')
ax_1.fill_between(X_range, scores, 0, color='dodgerblue', alpha=0.2)
ax_1.set_xlabel('Estimators')
ax_1.set_ylabel('Mean Squared Error')
ax_1.set_title('MSEs Over Estimators')
ax_1.legend()

ax_2.scatter(X, y, s=10, label='Original Data', c='black')
ax_2.plot(X, bag.predict(X), linewidth=2, color='crimson', label='Predicted Plot')
ax_2.fill_between(X.flatten(), bag.predict(X), np.sin(X).flatten(), color='crimson', alpha=0.3, label='Residual Area')
ax_2.plot(X, np.sin(X), linewidth=2, linestyle='--', color='dimgray', label='True Plot')
ax_2.set_xlabel('x')
ax_2.set_ylabel('y')
ax_2.set_title(f'Bagging Regression Result [MSE: {bag.score(X, y):.4f}]')
ax_2.legend()

plt.tight_layout()
plt.show()
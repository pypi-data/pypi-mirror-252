import __local__
from luma.ensemble.bagging import BaggingClassifier
from luma.classifier.svm import KernelSVC
from luma.reduction.select import RFE
from luma.metric.classification import Accuracy
from luma.visual.result import DecisionRegion

from sklearn.datasets import load_wine
import matplotlib.pyplot as plt


X, y = load_wine(return_X_y=True)
X = X[:, [6, 9]]

bag = BaggingClassifier(base_estimator=KernelSVC(),
                        n_estimators=50,
                        max_samples=1.0,
                        max_features=1.0,
                        bootstrap=True,
                        bootstrap_feature=False,
                        random_state=42,
                        verbose=True)

bag.fit(X, y)

fig = plt.figure(figsize=(10, 5))
ax_1 = fig.add_subplot(1, 2, 1)
ax_2 = fig.add_subplot(1, 2, 2)

scores = [est.score(X, y) for est, _ in bag]
scores.append(bag.score(X, y))

x_range = range(51)
ax_1.plot(x_range, scores, color='royalblue')
ax_1.fill_between(x_range, scores, 0, color='royalblue', alpha=0.3)
ax_1.scatter(50, scores[-1], c='royalblue')
ax_1.set_xticks(x_range, [''] * 50 + ['bag'])
ax_1.set_xlabel('Estimators')
ax_1.set_ylabel('Accuracy')
ax_1.set_ylim(0.0, 1.05)
ax_1.set_title('Accuracies Over Estimators')

dec = DecisionRegion(estimator=bag,
                     X=X,
                     y=y,
                     title=f'Bagging Classifier with Kernel SVCs')

dec.plot(ax=ax_2, show=True)

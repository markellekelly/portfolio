from linear_models.base_model import BaseModel
import numpy as np
import matplotlib.pyplot as plt

from plotting_utils import plot_contours, plot_2d_decision_boundary, make_meshgrid


class LDAClassifier(BaseModel):
    def __init__(self):
        super(LDAClassifier, self).__init__()
        self.method = 'MLE'
        self.classes = None
        self.prior_probs_ = None
        self.means_ = None

    def __str__(self):
        return f'Linear Regression Model\n' \
               f'Coefficients: \n{self.coef_}\n' \
               f'Intercept: {self.intercept_}\n' \


    def _fit(self, data, y, **kwargs):
        assert len(data) == len(y)
        assert len(np.unique(y) == 2)

        self.classes = np.unique(y)
        y = y.reshape(1, len(y)).flatten()

        # separate the data
        X_0 = data[y == self.classes[0]]
        X_1 = data[y == self.classes[1]]

        self.prior_probs_ = [len(X_0)/len(data), len(X_1)/len(data)]

        mu_0 = X_0.mean(axis=0)
        mu_1 = X_1.mean(axis=0)

        # find B
        diff = mu_0 - mu_1
        B = np.outer(diff, diff)

        # find S
        S_0 = np.apply_along_axis(lambda x: np.outer(x, x), 1, X_0 - mu_0).sum(axis=0)
        S_1 = np.apply_along_axis(lambda x: np.outer(x, x), 1, X_1 - mu_1).sum(axis=0)
        S = S_0 + S_1

        # solve
        values, vectors = np.linalg.eig(np.matmul(np.linalg.inv(S), B))
        w = vectors[:, np.argmax(values)]

        self.coef_ = w[:, None]
        self.intercept_ = -(mu_0.dot(w) + mu_1.dot(w))/2
        self.means_ = np.asarray((w.dot(mu_0), w.dot(mu_1)))[:, None]
        return self

    def predict(self, x):
        scores = self.decision_function(x)

        distance_to_0 = np.abs(scores - self.means_[0] - self.intercept_)
        distance_to_1 = np.abs(scores - self.means_[1] - self.intercept_)

        return self.classes[(distance_to_1 < distance_to_0).astype(int)]

    def score(self, x, y, metric=None):
        predictions = self.predict(x)
        y0 = y.reshape(predictions.shape)

        return np.mean(predictions == y0)

    def decision_boundary(self, x):
        w0 = self.coef_[0][0]
        w1 = self.coef_[1][0]

        return (w0*x + self.intercept_) / -w1

    def decision_function(self, x):
        return (x.dot(self.coef_)).T.flatten() + self.intercept_

    def generate_2d_plot(self, x, y):
        plt.subplot(211)
        ax = plt.gca()
        ax.scatter(x[:, 0], x[:, 1], c=y, cmap='winter', edgecolors='k')
        plot_2d_decision_boundary(self, ax, x[:, 0])
        plt.subplot(212)
        ax = plt.gca()
        xx, yy = make_meshgrid(x[:, 0], x[:, 1])
        plot_contours(self, ax, xx, yy)
        plt.scatter(x[:, 0], x[:, 1], c=y, cmap='winter', edgecolors='k')








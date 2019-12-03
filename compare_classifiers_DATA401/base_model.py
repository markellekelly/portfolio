import abc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from abc import abstractmethod


def _convert_dataframe(x):
    """
    Converts x from a Pandas DataFrame to a Numpy ndarray if x is a DataFrame. If x is already a
    ndarray, then x is returned
    :param x: Input DataFrame
    :return: ndarray
    """
    try:
        if isinstance(x, np.ndarray):
            return x
        elif isinstance(x, list) or isinstance(x, pd.Series):
            return np.asarray(x).reshape((len(x), 1))
        else:
            return x.to_numpy().reshape(len(x), len(x.columns))
    except NameError:
        print(f'Invalid input. Input must be either Pandas DataFrame or Numpy ndarray.')


class BaseModel(abc.ABC):
    def __init__(self, **kwargs):
        # Model Definition
        self.coef_ = None
        self.intercept_ = None

        # Model Parameters
        self.method = None
        self.learning_rate = None
        self.epsilon = None
        self.penalty = None
        self.max_iters = None
        self.max_iters_no_change = None
        self.fit_intercept = None
        self.num_workers = None
        self.loss = None

        # Extra metrics
        self.errors = []
        self.iterations = []

    def fit(self, x, y, **kwargs):
        """
           This method actually builds the model.

           :parameter x - Pandas DataFrame or numpy ndarray containing explanatory variables
           :parameter y - Pandas DataFrame or numpy ndarray containing response variables
           :parameter method - String that determines the method used to build the model.
        """
        x0 = _convert_dataframe(x)
        y0 = _convert_dataframe(y)

        return self._fit(x0, y0, **kwargs)

    @abstractmethod
    def _fit(self, x, y, **kwargs):
        pass

    def generate_2d_plot(self, x, y):
        """
        Method used for sanity checking fit functions. It will generate a 2d plot of x and y
        with the best fit generated by our fit function.

        :parameter x - X values
        :parameter y - y values
        """

        if self.coef_ is None:
            print(f'Model must be fit before a plot can be generated. Please use fit() first.')

        domain = pd.DataFrame(np.arange(np.min(x).iloc[0], np.max(x).iloc[0] + 1))
        predictions = self.predict(domain)
        plt.plot(domain, predictions)
        plt.text(np.mean(x).iloc[0], np.max(predictions),
                 f'y = {np.round(self.intercept_, 3)} + {np.round(self.coef_[0], 3)}x',
                 horizontalalignment='center',
                 verticalalignment='center',
                 bbox=dict(facecolor='blue', alpha=0.25))
        plt.title('Line of Best Fit')
        plt.xlabel('X')
        plt.ylabel('Y')

        plt.scatter(x, y)

    def plot_error(self):
        """
        Plots the error vs iterations of the fit algorithm. Therefore, fit() must be called before this.
        :return - None
        """
        plt.title('Errors vs. Iterations')
        plt.xlabel('Iterations')
        plt.ylabel('Error')

        plt.plot(self.iterations, self.errors)

    def plot_loss(self):
        plt.title('Training Loss')
        plt.xlabel('Training Iterations')
        plt.ylabel('SSE Loss')

        plt.plot(self.iterations, self.losses)

    def predict(self, x):
        """
            Makes predictions based on fit data. This means that fit() must be called before predict()

            :parameter x - Pandas DataFrame of data you want to make predictions about.
        """
        if self.intercept_ is None or self.coef_ is None:
            print(f'Unable to make predictions until the model is fit. Please use fit() first.')
            return
        elif len(x[0]) != len(self.coef_):
            print(f'Column mismatch. Expected(,{len(self.coef_)}) but was {np.shape(x)}')
            return
        else:
            slopes = self.coef_

            return [(self.intercept_ + row.dot(slopes)) for row in x]

    def score(self, x, y, metric='adj'):
        """
        Method for calculating the score of a prediction.

        :param x - Pandas DataFrame containing data you want to make predictions about.
        :param y - Pandas DataFrame dependent variables.
        :param metric - Scoring metric to use. Default is adjusted R^2. Can be one of: 'adj', 'r2', 'aic', 'bic'
        """
        x0 = _convert_dataframe(x)
        y0 = _convert_dataframe(y).T
        predicted = [pred[0] for pred in self.predict(x0)]

        if metric == 'adj':
            # 1 - (1 - R^2)(n-1/n-k-1)
            ssr = ((y0 - predicted) ** 2).sum()
            sst = ((y0 - y0.mean()) ** 2).sum()
            r2 = 1 - (ssr / sst)
            n = len(x0)  # Number of observations
            p = len(x0[0])  # Number of predictor variables
            return 1 - (1 - r2 * (n - 1) / (n - p - 1))
        elif metric == 'r2':
            ssr = ((y0 - predicted) ** 2).sum()
            sst = ((y0 - y0.mean()) ** 2).sum()
            return 1 - ssr / sst
        elif metric == 'aic':
            # Not implemented yet since these rely on MLE
            pass
        elif metric == 'bic':
            pass
        else:
            print(f'Unsupported score metric: {metric}')
            pass

    @abstractmethod
    def _loss(self, x, y):
        pass
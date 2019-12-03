import numpy as np

from linear_models.base_model import BaseModel
from abc import abstractmethod
from timeit import default_timer as timer
from errors.convergence import ConvergenceError
from linear_models.base_model import _convert_dataframe
import matplotlib.pyplot as plt

from plotting_utils import plot_2d_decision_boundary, plot_contours, make_meshgrid


class _BaseSGD(BaseModel):
    batch_size: int = 1

    @abstractmethod
    def initialize_weights(self, x):
        pass

    @abstractmethod
    def get_weights(self):
        pass

    @abstractmethod
    def _update_rule(self, x, y, b):
        pass

    @abstractmethod
    def update_model_params(self, params):
        pass

    def _fit(self, x, y, **kwargs):
        # We initialize weights in the model here because the incoming weights for the first hidden layer cannot
        # be known without knowing the size of the input vector
        return self._fit_by_sgd(x, y, **kwargs)

    def _fit_by_sgd(self, x, y, verbose=0, initial_weights=None):
        """
        Calculates the gradient of the loss function for linear regression.

        :param x: Column vector of explanatory variables
        :param y: Column vector of dependent variables
        :param verbose: Int that determines how verbose the output of the fit algorithm is
        :param initial_weights: Column vector of initial weights if initial weights are non-zero.
            This also is used for Neural Nets since the weights vector is not a 1D vector. In the case of
            neural nets, each index in the initial weights should be a matrix containing the weights for the
            corresponding hidden layer
        :return: Vector of parameters for Linear Regression
        """
        assert len(x) == len(y)

        # Reset model error calculations
        self.errors = []
        self.iterations = []
        self.losses = []

        # Setup Debugging/ Graphing
        start_time = timer()
        train_time = 0

        # Copy input DataFrame so we don't modify original (may need to change if copy is too expensive)
        if self.fit_intercept:
            intercept_terms = np.ones((x.shape[0], 1))
            x0 = np.hstack((intercept_terms, x.copy()))
        else:
            x0 = x.copy()

        y0 = y.reshape(len(y), 1)  # Convert y to a column vector

        self.initialize_weights(x.shape)

        betas = self.get_weights()

        n_iter = 0
        n_iters_no_change = 0
        while n_iters_no_change < self.max_iters_no_change and n_iter < self.max_iters:
            permutation = np.random.permutation(x0.shape[0])
            x_batches = np.array_split(x0[permutation], np.ceil(len(x0)/self.batch_size))
            y_batches = np.array_split(y0[permutation], np.ceil(len(y0)/self.batch_size))

            pre_epoch_betas = betas
            # Iterate through all (X, Y) pairs where X is a vector of predictor variables [x1, x2, x3, ...]
            # and Y is a vector containing the response variable
            with np.errstate(invalid='raise'):
                for x_batch, y_batch in zip(x_batches, y_batches):
                    v = x_batch
                    w = y_batch.reshape(1, len(y_batch))
                    prior_betas = betas
                    try:
                        update = self._update_rule(v, w, prior_betas)
                        loss_change = [np.multiply(self.learning_rate, weight_set) for weight_set in update]
                        # print(f'Priors: {prior_betas}')
                        # print(f'Update: {loss_change}\n')
                        betas = [np.subtract(prior_weight, weight_change)
                                 for prior_weight, weight_change
                                 in zip(prior_betas, loss_change)]
                    except FloatingPointError:
                        raise ConvergenceError()

            total_error = np.sum([np.sum(np.subtract(beta, pre_beta) ** 2)
                                  for beta, pre_beta
                                  in zip(betas, pre_epoch_betas)])
            n_iters_no_change = n_iters_no_change + 1 if total_error < self.epsilon else 0
            n_iter += 1
            train_time = timer() - start_time
            if verbose > 0:
                print(
                    f'-- Epoch {n_iter}\n'
                    f'Total training time: {round(train_time, 3)}')
                if verbose > 1:
                    print(f'Equation:\n'
                          f'y = {np.round(betas[1:][0][0], 3)}(x1) + {np.round(betas[1:][1][0], 3)}(x2) + {np.round(betas[0][0], 3)}')
                if verbose > 2:
                    print(
                        f'Pre Epoch Betas:\n{pre_epoch_betas}\n'
                        f'Post Epoch Betas:\n{betas}\n')
            self.update_model_params(betas)

            self.iterations.append(n_iter)
            # self.losses.append(self._loss(x, y))
            self.errors.append(total_error)


        # self.coef_ = betas[1 if self.fit_intercept else 0:]
        # self.intercept_ = betas[0][0] if self.fit_intercept else 0  # betas[0] gives a series with a single value
        if verbose > 0:
            print(f'SGD converged after {n_iter} epochs.\n'
                  f'Total Training Time: {round(train_time, 3)} sec.')

        # if n_iter == self.max_iters and self.errors[-1] > self.epsilon:
        #     print(f'SGD did not converge after {self.max_iters} epochs. Increase max_iters for a better model.')

        return self


class SGDRegressor(_BaseSGD):
    def __init__(
            self,
            learning_rate=1e-4,
            epsilon=1e-3,
            penalty='l2',
            max_iters=1000,
            max_iters_no_change=5,
            fit_intercept=True,
            alpha=1e-4):
        super(SGDRegressor, self).__init__()
        self.method = 'SGD'
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.penalty = penalty
        self.max_iters = max_iters
        self.max_iters_no_change = max_iters_no_change
        self.fit_intercept = fit_intercept
        self.alpha = alpha

    def _update_rule(self, x, y, b):
        """
        Returns the value of the gradient of the loss function with a regularization term
        dL/dβ = -2η(X.T(y - Xb)
        Where X is a column vector of [x_1, x_2, ... , x_i] and
        y is a column vector of [y_1, y_2, ... , y_i] and
        b is the column vector of [β_1, β_2, ... , β_n]

        However, since this is stochastic, we randomly sample a single x_i, y_i
        :param x: Vector of predictor variables for a single observation
        :param y: Vector containing the response variable for a single observation
        :param b: vector of prior betas
        :return: vector of changes to apply to vector of betas
        """
        if self.penalty == 'l2':
            xb = x.dot(b)
            change_in_loss = np.multiply(-2 * self.learning_rate, x.T.dot(y - xb))
            p = np.multiply(2 * self.alpha, b)
            p[0] = 0  # Penalizing the intercept is no bueno and b = [b_0, b_1, ...]
            return change_in_loss + p
        if self.penalty is None:
            xb = x.dot(b)
            change_in_loss = np.multiply(-2 * self.learning_rate, x.T.dot(y - xb))
            return change_in_loss
        else:
            print(f'Other penalty types are not supported yet.')
            return NotImplementedError


class SGDClassifier(_BaseSGD):
    def __init__(
            self,
            learning_rate=1e-4,
            epsilon=1e-3,
            penalty='l2',
            max_iters=1000,
            max_iters_no_change=5,
            fit_intercept=True,
            alpha=1e-4,
            loss='hinge',
            C=1):
        super(SGDClassifier, self).__init__()
        self.method = 'SGD'
        self.learning_rate = learning_rate
        self.loss = loss
        self.epsilon = epsilon
        self.penalty = penalty
        self.max_iters = max_iters
        self.max_iters_no_change = max_iters_no_change
        self.fit_intercept = fit_intercept
        self.alpha = alpha
        self.C = C

    def _update_rule(self, x, y, w):
        """
        Returns the value of the gradient of the loss function with a L2 regularization term
        The gradient that is calculated by this method is determined by self.loss
        Possible values:
        'log' - Compute the gradient for logistic regression
        'hinge' - Compute the gradient for SVM

        :param x0: Vector of predictor variables for a single observation
        :param y0: Vector containing the response variable for a single observation
        :param w: vector of prior betas
        :return: COLUMN vector of changes to apply to COLUMN vector of betas
        """
        if self.loss == 'log':
            xw = -(x.dot(w))
            exp = np.exp(xw)
            p = 1 / (1 + exp)
            reg_term = np.multiply(self.alpha / len(w), w)
            reg_term[0] = 0

            change_in_loss = -np.dot(np.subtract(y, p), x).T
            return change_in_loss + reg_term

        elif self.loss == 'hinge':
            print(f'X: {x}')
            print(f'w: {w}')
            xw = x.dot(w)[0]
            return w - self.C * y.dot(x).T if y.dot(xw) < 1 else w

    def predict(self, x):
        x0 = _convert_dataframe(x)
        return self.classes[(self.decision_function(x0) > 0).astype(int)].T.flatten()

    def score(self, x, y, metric=None):
        x0 = _convert_dataframe(x)
        y0 = _convert_dataframe(y)

        predictions = self.predict(x0)
        y0 = y0.reshape(predictions.shape)

        return np.mean(predictions == y0)

    def decision_function(self, x):
        x = _convert_dataframe(x)
        return self.intercept_ + np.dot(x, self.coef_)

    def decision_boundary(self, x, c=0):
        b1 = self.coef_[0]
        b2 = self.coef_[1]
        return (b1*x + self.intercept_ - c)/-b2

    def _fit(self, x, y, **kwargs):
        assert len(np.unique(y) == 2)
        y0 = np.asarray(y).flatten()
        self.classes = np.unique(y0)
        if self.loss == 'hinge':
            y0 = np.asarray([-1 if val == self.classes[0] else 1 for val in y0])
        elif self.loss == 'log':
            y0 = np.asarray([0 if val == self.classes[0] else 1 for val in y0])
        else:
            return NotImplementedError

        return super()._fit(x, y0, **kwargs)

    def _loss(self, x, y):
        return NotImplementedError

    def update_model_params(self, params):
        print(f'Params: {params}')
        self.coef_ = np.asarray(params).flatten()[1:]
        self.intercept_ = np.asarray(params).flatten()[0]

    def get_weights(self):
        model_params = np.insert(self.coef_, 0, self.intercept_)
        return model_params.reshape((len(model_params), 1))

    def initialize_weights(self, x):
        self.intercept_ = 1
        self.coef_ = np.asarray(np.random.uniform(-1, 1, len(x)))

    def generate_2d_plot(self, x, y):
        ax = plt.gca()
        xx, yy = make_meshgrid(x, y)
        plot_contours(self, ax, xx, yy)
        plt.scatter(x[:, 0], x[:, 1], c=y, cmap='winter', edgecolors='k')

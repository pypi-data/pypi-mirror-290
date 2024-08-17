from typing import Optional

import numpy as np
import optuna
import scipy


class AdaptiveLearningRate:
    """Customized learning rate decay"""

    def __init__(self,
                 learning_rate: float = 0.3,
                 decay_rate: float = 0.9,
                 patience: int = 10) -> None:
        self.learning_rate = learning_rate
        self.decay_rate = decay_rate
        self.patience = patience
        self.best_score = float('inf')
        self.wait_count = 0

    def callback(self, env):
        score = env.evaluation_result_list[0][2]  # AUC as the metric

        # Find a larger AUC
        if score > self.best_score:
            self.best_score = score
            self.wait_count = 0  # Reset wait_count
        else:
            self.wait_count += 1  # Increment wait_count

        # If there has been no improvement for 'patience' attempts
        # Decay the learning rate
        if self.wait_count >= self.patience:
            pre = self.learning_rate
            self.learning_rate *= self.decay_rate
            if env.params.get('verbose', 0) >= 0:
                print(
                    f"Learning rate ==> {self.learning_rate:.3f} "
                    f"(-{pre - self.learning_rate:.4f})"
                )
            self.wait_count = 0  # Reset wait_count

        # Update the learning rate
        env.model.params['learning_rate'] = self.learning_rate


def gen_threshold(y_true, y_pred, metric, n_trials: int) -> float:
    """
    Finds the optimal threshold based on the desired metric
    """

    # Set the logging level to ERROR
    verbose = optuna.logging.get_verbosity()
    optuna.logging.set_verbosity(optuna.logging.ERROR)

    def objective(trial):
        t = trial.suggest_float('threshold', 0.0, 1.0)
        y_label = [1 if e > t else 0 for e in y_pred]
        return metric(y_true=y_true, y_pred=y_label)

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    best_params = study.best_params

    # Restore the original logging level
    optuna.logging.set_verbosity(verbose)

    return best_params['threshold']


def gen_threshold_cdf(y_pred, rate: float, interval: int = 100) -> Optional[float]:
    """
    Finds the optimal threshold based on the desired proportion of negative samples (label 0)

    :param y_pred: An array of predicted probabilities.
    :param rate: The proportion of negative samples.
    :param interval: The number of intervals.
    :return: The optimal threshold.
    """
    xx = np.linspace(min(y_pred), max(y_pred), interval)
    kde = scipy.stats.gaussian_kde(y_pred)
    pdf = kde.evaluate(xx)
    cdf = np.cumsum(pdf) * (xx[1] - xx[0])

    px = 0
    for x, y in zip(xx, cdf):
        if y > rate:
            return (px + x) / 2
        px = x

    return None

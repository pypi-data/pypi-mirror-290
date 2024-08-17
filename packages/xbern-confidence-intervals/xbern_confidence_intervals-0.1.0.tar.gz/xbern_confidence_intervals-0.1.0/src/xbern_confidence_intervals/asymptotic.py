# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Asymptotic confidence intervals for exchangeable Bernoulli (XBern) means.

The confidence intervals are asymptotic (i.e., they hold in the limit that 
the number of samples is infinite). They are based on the Wilson confidence
interval and its higher-order variants introduced by
[Pillutla et al. (2023)](https://arxiv.org/pdf/2305.18447.pdf).
"""

import math
from typing import Tuple

import numpy as np
import pandas as pd
import scipy.stats


def get_wilson_confidence_intervals(
    samples: np.ndarray,
    beta: float = 0.05,
) -> Tuple[pd.Series, pd.Series]:
  """Asymptotic higher-order Wilson confidence intervals for XBern.

  Args:
    samples: binary matrix of shape (n, k). Represents n i.i.d. trials of a
        k-dimensional XBern distribution.
    beta: failure probability, such that we return a one-sided 1-beta confidence
        intervals.

  Returns:
    ci_left, ci_right: pd.Series containing that maps the name of an asymptotic
        confidence interval to its value. The keys are:
          * 1st-Order Wilson (Algorithm 5)
          * 2nd-Order Wilson (Algorithm 6)
          * 4th-Order Wilson (Algorithm 7)
        Each confidence interval provides the guarantee that
          * with probability at least 1 - beta, the mean of the XBern
              is greater than ci_left, or,
          * with probability at least 1 - beta, the mean of the XBern
              is smaller than ci_right.
        Note that both guarantees do not hold simulatenously for the given
        failure probability beta. However, both guarantees hold simulatenously
        with probability at least:
          * 1 - 2 * beta for 1st-Order Bernstein,
          * 1 - 3/2 * beta for 2nd-Order Bernstein, and
          * 1 - 5/4 * beta for 4th-Order Bernstein.
  """
  n, k = samples.shape
  ci_left, ci_right = {}, {}

  # Compute the moments
  m1 = np.mean(samples, axis=1)  # (n,)
  mu1_hat = m1.mean()  # (n,) -> scalar
  if k > 1:
    m2 = m1 * (k * m1 - 1) / (k - 1)  # (n,)
    mu2_hat = m2.mean()  # (n,) -> scalar
  else:
    mu2_hat = None
    m2 = 0.
  if k > 2:
    m3 = m2 * (k * m1 - 2)  / (k - 2)  # (n,)
    mu3_hat = m3.mean()  # (n,) -> scalar
  else:
    mu3_hat = None
    m3 = 0.
  if k > 3:
    m4 = m3 * (k * m1 - 3)  / (k - 3)  # (n,)
    mu4_hat = m4.mean()  # (n,) -> scalar
  else:
    mu4_hat = None

  key = '1st-Order Wilson'
  left = solve_first_order_wilson_left_tail(mu1_hat, n, beta)
  right = solve_first_order_wilson_right_tail(mu1_hat, n, beta)
  ci_left[key] = left
  ci_right[key] = right

  key = '2nd-Order Wilson'
  if k > 1:
    mu2_upper = solve_first_order_wilson_right_tail(
        mu2_hat, n, beta / 2
    )
    left = solve_second_order_wilson_left_tail(
        mu1_hat, mu2_upper, n, k, beta / 2
    )
    right = solve_second_order_wilson_right_tail(
        mu1_hat, mu2_upper, n, k, beta / 2
    )
    ci_left[key] = left
    ci_right[key] = right

  key = '4th-Order Wilson'
  if k > 3:
    mu3_upper = solve_first_order_wilson_right_tail(mu3_hat, n, beta / 4)
    mu4_upper = solve_first_order_wilson_right_tail(mu4_hat, n, beta / 4)
    mu2_upper = solve_fourth_order_wilson_right_tail_for_mu2(
        mu2_hat, mu3_upper, mu4_upper, n, k, beta / 4)
    left = solve_second_order_wilson_left_tail(
        mu1_hat, mu2_upper, n, k, beta / 4
    )
    right = solve_second_order_wilson_right_tail(
        mu1_hat, mu2_upper, n, k, beta / 4
    )
    ci_left[key] = left
    ci_right[key] = right

  return pd.Series(ci_left), pd.Series(ci_right)


def solve_first_order_wilson_right_tail(mu_hat, n, beta):
  """First order Wilson bound (right tail)."""
  z_beta = scipy.stats.norm.ppf(1-beta)  # (1-beta) quantile of the Gaussian
  a = n + z_beta**2
  b = 2 * n * mu_hat + z_beta**2
  c = n * mu_hat**2
  sol = (b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)
  sol = max(0, min(1, sol))  # clip to [0, 1]
  # Worst-case solution using var <= 1/4
  sol2 = max(0, min(1, mu_hat + z_beta * math.sqrt(0.25 / n)))
  return min(sol, sol2)


def solve_first_order_wilson_left_tail(mu_hat, n, beta):
  """First order Wilson bound (left tail)."""
  z_beta = scipy.stats.norm.ppf(1-beta)  # (1-beta) quantile of the Gaussian
  a = n + z_beta**2
  b = 2 * n * mu_hat + z_beta**2
  c = n * mu_hat**2
  sol = (b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
  sol = max(0, min(1, sol))  # clip to [0, 1]
  # Worst-case solution using var <= 1/4
  sol2 = max(0, min(1, mu_hat - z_beta * math.sqrt(0.25 / n)))
  return max(sol, sol2)


def solve_second_order_wilson_right_tail(mu_hat, mu2, n, k, beta):
  """Second order Wilson bound (right tail)."""
  z_beta = scipy.stats.norm.ppf(
      1 - beta
  )  # (1-beta) quantile of the Gaussian
  a = n + z_beta**2
  b = 2 * n * mu_hat + z_beta**2 / k
  c = n * mu_hat**2 - z_beta**2 * (k - 1) / k * mu2
  sol = (b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)
  sol = max(0, min(1, sol))  # clip to [0, 1]
  # Worst-case solution using var <= 1/4
  sol2 = max(0, min(1, mu_hat + z_beta * math.sqrt(0.25 / n)))
  return min(sol, sol2)


def solve_second_order_wilson_left_tail(mu_hat, mu2, n, k, beta):
  """Second order Wilson bound (left tail)."""
  z_beta = scipy.stats.norm.ppf(
      1 - beta
  )  # (1-beta) quantile of the Gaussian
  a = n + z_beta**2
  b = 2 * n * mu_hat + z_beta**2 / k
  c = n * mu_hat**2 - z_beta**2 * (k - 1) / k * mu2
  sol = (b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
  sol = max(0, min(1, sol))  # clip to [0, 1]
  # Worst-case solution using var <= 1/4
  sol2 = max(0, min(1, mu_hat - z_beta * math.sqrt(0.25 / n)))
  return max(sol, sol2)


def solve_fourth_order_wilson_right_tail_for_mu2(
    mu2_hat, mu3, mu4, n, k, beta
):
  """Fourth order Wilson bound (right tail)."""
  z_beta = scipy.stats.norm.ppf(
      1 - beta
  )  # (1-beta) quantile of the Gaussian
  a = n + 2 * z_beta**2 * (1 + 2 * (k - 2)) / (k**2 - k)
  b = 2 * n * mu2_hat + 2 * z_beta**2 / (k**2 - k)
  c1 = ((k - 2) * (k - 3) / (k**2 - k) * (mu4 - mu3**2) +
        4 * (k - 2) / (k**2 - k) * mu3)
  c = n * mu2_hat**2 - z_beta**2 * c1
  sol = (b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)
  sol = max(0, min(1, sol))  # clip to [0, 1]
  # Worst-case solution using var <= 1/4
  sol2 = max(0, min(1, mu2_hat + z_beta * math.sqrt(0.25 / n)))
  return min(sol, sol2)


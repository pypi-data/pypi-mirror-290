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
"""Non-asymptotic confidence intervals for exchangeable Bernoulli (XBern) means.

The confidence intervals are exact (i.e., non-asymptotic) and are based on
the Bernstein inequality and its higher-order variants introduced by
[Pillutla et al. (2023)](https://arxiv.org/pdf/2305.18447.pdf).
"""

import math
from typing import Tuple

import numpy as np
import pandas as pd
import scipy.optimize
import scipy.stats


TOLERANCE = 1e-10  # Required for the numerical root-finder.
# Anything below this will be treated as 0.


def get_bernstein_confidence_intervals(
    samples: np.ndarray,
    beta: float = 0.05,
) -> Tuple[pd.Series, pd.Series]:
  """Non-asymptotic higher-order Wilson confidence intervals for XBern.

  Args:
    samples: binary matrix of shape (n, k). Represents n i.i.d. trials of a
        k-dimensional XBern distribution.
    beta: failure probability, such that we return a one-sided 1-beta confidence
        intervals.

  Returns:
    ci_left, ci_right: pd.Series containing that maps the name of an asymptotic
        confidence interval to its value. The keys are:
          * 1st-Order Bernstein (Algorithm 2)
          * 2nd-Order Bernstein (Algorithm 3)
          * 4th-Order Bernstein (Algorithm 4)
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
  m1 = samples.mean(axis=1)  # (n,)
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

  key = '1st-Order Bernstein'
  left = solve_first_order_bernstein_left_tail(mu1_hat, n, beta)
  right = solve_first_order_bernstein_right_tail(mu1_hat, n, beta)
  ci_left[key] = left
  ci_right[key] = right

  key = '2nd-Order Bernstein'
  if k > 1:
    mu2_upper = solve_first_order_bernstein_right_tail(
        mu2_hat, n, beta / 2
    )
    left = solve_second_order_bernstein_left_tail(
        mu1_hat, mu2_upper, n, k, beta / 2
    )
    right = solve_second_order_bernstein_right_tail(
        mu1_hat, mu2_upper, n, k, beta / 2
    )
    ci_left[key] = left
    ci_right[key] = right

  key = '4th-Order Bernstein'
  if k > 3:
    mu3_upper = solve_first_order_bernstein_right_tail(mu3_hat, n, beta/4)
    mu4_upper = solve_first_order_bernstein_right_tail(mu4_hat, n, beta/4)
    mu2_upper = solve_fourth_order_bernstein_right_tail_for_mu2(
        mu2_hat, mu3_upper, mu4_upper, n, k, beta/4)
    left = solve_second_order_bernstein_left_tail(
        mu1_hat, mu2_upper, n, k, beta/4
    )
    right = solve_second_order_bernstein_right_tail(
        mu1_hat, mu2_upper, n, k, beta/4
    )
    ci_left[key] = left
    ci_right[key] = right

  return pd.Series(ci_left), pd.Series(ci_right)


# Helper Functions
def solve_first_order_bernstein_right_tail(mu_hat, n, beta):
  """First order Bernstein bound (right tail)."""
  # LHS - RHS of the Bernstein self-bound
  def lhs_minus_rhs(x):
    return (x - mu_hat - 2 / (3 * n) * math.log(1 / beta)
            - math.sqrt(2 * x * (1 - x) / n * math.log(1 / beta)))
  # left end point = mu_hat; sign = -ve
  # right end point = 1; check the sign
  if lhs_minus_rhs(1) <= 0:
    # no solution for x in [mu_hat, 1]
    right_end_point = 1
  else:  # opposite signs => solution exists
    # We need the lower bound to be strictly less than 0 (so that x = 0 is not
    # a solution). We just give a small number here.
    lower_bound = max(mu_hat, TOLERANCE)
    right_end_point = scipy.optimize.brentq(
        lhs_minus_rhs, lower_bound, 1, maxiter=10000)
  return right_end_point


def solve_first_order_bernstein_left_tail(mu_hat, n, beta):
  """First order Bernstein bound (left tail)."""
  # LHS - RHS of the Bernstein self-bound
  def lhs_minus_rhs(x):
    return (mu_hat - x - 2 / (3 * n) * math.log(1 / beta)
            - math.sqrt(2 * x * (1 - x) / n * math.log(1 / beta)))
  # right end point = mu_hat; sign = -ve
  # left end point = 0; check the sign
  if lhs_minus_rhs(0) <= 0:
    # no solution for x in [0, mu_hat]
    left_end_point = 0
  else:  # opposite signs => solution exists
    upper_bound = min(mu_hat, 1-TOLERANCE)
    left_end_point = scipy.optimize.brentq(
        lhs_minus_rhs, 0, upper_bound, maxiter=10000)
  return left_end_point


def solve_second_order_bernstein_right_tail(mu_hat, mu2, n, k, beta):
  """Second order Bernstein bound (right tail)."""
  # LHS - RHS of the Bernstein self-bound
  def lhs_minus_rhs(x):
    variance_estimate = max(0, min(0.25, x / k - x * x + mu2 * (k - 1) / k))
    return (x - mu_hat - 2 / (3 * n) * math.log(1 / beta)
            - math.sqrt(2 / n * variance_estimate * math.log(1 / beta)))
  # left end point = mu_hat; sign = -ve
  # right end point = 1; check the sign
  if lhs_minus_rhs(1) <= 0:
    # no solution for x in [mu_hat, 1]
    print('No solution in [mu_hat, 1]')
    right_end_point = 1
  else:  # opposite signs => solution exists
    lower_bound = max(mu_hat, TOLERANCE)
    right_end_point = scipy.optimize.brentq(
        lhs_minus_rhs, lower_bound, 1, maxiter=10000)
  return right_end_point


def solve_second_order_bernstein_left_tail(mu_hat, mu2, n, k, beta):
  """Second order Bernstein bound (left tail)."""
  # LHS - RHS of the Bernstein self-bound
  def lhs_minus_rhs(x):
    variance_estimate = max(0, min(0.25, x / k - x * x + mu2 * (k - 1) / k))
    return (mu_hat - x - 2 / (3 * n) * math.log(1 / beta)
            - math.sqrt(2 / n * variance_estimate * math.log(1 / beta)))
  # right end point = mu_hat; sign = -ve
  # left end point = 0; check the sign
  if lhs_minus_rhs(0) <= 0:
    # no solution for x in [0, mu_hat]
    left_end_point = 0
  else:  # opposite signs => solution exists
    upper_bound = min(mu_hat, 1-TOLERANCE)
    left_end_point = scipy.optimize.brentq(
        lhs_minus_rhs, 0, upper_bound, maxiter=10000)
  return left_end_point


def solve_fourth_order_bernstein_right_tail_for_mu2(
    mu2_hat, mu3, mu4, n, k, beta
    ):
  """Fourth order Bernstein bound (right tail)."""
  # LHS - RHS of the Bernstein self-bound
  def lhs_minus_rhs(x):
    numerator = (2 * x  * (1 - x) +
                 4 * (k-2) * (mu3 - x**2) +
                 (k-2) * (k-3) * (mu4 - mu3**2))
    variance_estimate = max(0, min(0.25, numerator / (k * (k-1))))
    # print(variance_estimate)
    return (x - mu2_hat - 2 / (3 * n) * math.log(1 / beta)
            - math.sqrt(2 / n * variance_estimate * math.log(1 / beta)))
  # left end point = mu2_hat; sign = -ve
  # right end point = 1; check the sign
  if lhs_minus_rhs(1) <= 0:
    # no solution for x in [mu2_hat, 1]
    print('No solution in [mu2_hat, 1]'
          f'end_points = {lhs_minus_rhs(mu2_hat)}, {lhs_minus_rhs(1)}')
    right_end_point = 1
  else:  # opposite signs => solution exists
    lower_bound = max(mu2_hat, TOLERANCE)
    right_end_point = scipy.optimize.brentq(
        lhs_minus_rhs, lower_bound, 1, maxiter=10000)
  return right_end_point


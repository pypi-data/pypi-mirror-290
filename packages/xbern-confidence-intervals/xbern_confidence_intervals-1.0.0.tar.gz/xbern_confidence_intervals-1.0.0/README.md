# Adaptive Confidence Intervals for Exchangeable Bernoulli (XBern) Means

**NOTE**: This library has been extracted from the open-source code at [this link](https://github.com/google-research/federated/tree/master/lidp_auditing). Please refer to the license there (Apache 2.0 license) for details, which is also applicable to this package.

An XBern or exchangeable Bernoulli distribution is a probability distribution
over binary vectors which is exchangeable, i.e., the probability mass does not
change when the coordinates of the vector are permuted.
This package gives confidence intervals for the mean (first moment) of the 
XBern distribution from 
[Pillutla et al. (NeurIPS 2023)](https://arxiv.org/pdf/2305.18447.pdf).

For n binary vectors in k-dimensions, the confidence interval could vary
from 1 / sqrt(n) (if the k dimensions are copies of each other)
to 1 / sqrt(nk) (if the k dimensions are independent). We give adaptive
confidence intervals that automatically adapt the actual level of correlation between the
k dimensions. The obtained confidence intervals recover the 1 / sqrt(n) rate in the high correlation regime while getting an improved 1 / sqrt(nk) + 1 / n^{3/4} rate in the low correlation regime.


# Table of Contents
- [Installation](#installation)
- [Requirements](#requirements)
- [Functionality](#functionality)
- [Citation](#citation)


# Installation

For a direct install, run 
```bash
pip install xbern-confidence-intervals
```
or navigate to the parent directory and run
```bash
pip install -e .
```


# Requirements
The installation command above installs the main requirements, which are:
- numpy >= 1.22.4
- pandas >= 1.4.4
- scipy >= 1.7.3


#  Functionality

We give a quick overview of the API here. Please see [xbern_demo.ipynb](https://github.com/krishnap25/xbern_confidence_intervals/xbern_demo.ipynb) for a full tour of the features.

The API works as follows:

```python
import numpy as np
import xbern_confidence_intervals as xbern_ci

n, k = 1000, 10  # n samples of k components each.

# The input is a boolean array of shape (n, k).
# The components are correlated in general but we take them
#  to be independent for a quick demonstration of this package.
samples = (np.random.rand(n, k) > 0.99)
beta = 0.05  # failure probability

# For asymptotic Wilson intervals:
left, right = xbern_ci.get_bernstein_confidence_intervals(samples, beta)
# One-sided confidence intervals that satisfy Pr(mean < left) < 1-beta or
# Pr(mean > right) < 1-beta under the limit n -> infinity.
# Here, left/right are pd.Series with different confidence estimates as index.

# For non-asymptotic Bernstein intervals:
left, right = xbern_ci.get_bernstein_confidence_intervals(samples, beta)
# One-sided confidence intervals that satisfy Pr(mean < left) < 1-beta or
# Pr(mean > right) < 1-beta which holds at each n.
```

We also provide a vectorized implementation for the Wilson intervals,
that repeats the above calculations for each element in the batch:

```python
# The first dimension represents the batch:
samples = (np.random.rand(batch_size, n, k) > 0.99)

left, right = xbern_ci.xbern_ci.get_wilson_confidence_intervals_vectorized(
    samples, beta
)
# Here, left/right are pd.DataFrame with confidence estimates as index and
# the batch entires on the columns.
```

# Citation

If you find this package useful, please cite
```
@inproceedings{pillutla2023unleashing,
  author       = {Krishna Pillutla and
                  Galen Andrew and
                  Peter Kairouz and
                  H. Brendan McMahan and
                  Alina Oprea and
                  Sewoong Oh},
  title        = {{Unleashing the Power of Randomization in Auditing Differentially Private
                  ML}},
  booktitle      = {NeurIPS},
  year         = {2023},
}
```


"""
This file contains a tutorial on how to implement various basic asset pricing techniques using the Toolkit. These
include univariate sorts, bivariate sorts, Fama-MacBeth regressions, and accounting for transaction costs.
"""

import pandas as pd
import numpy as np
import AssayingAnomalies.Functions as aa

from AssayingAnomalies import initial_setup
initial_setup()


# First load in your parameters
params = AssayingAnomalies.Config.load_params()

"Univariate Sorts"
ret = pd.read_csv()

import scipy.stats as stats
from scipy.stats import rv_continuous

class neg_log_uniform(rv_continuous):
	"negative log uniform distribution"

	def _cdf(self, x):
		"""
		cdf of the negative log uniform distribution
		"""
		return 1. - 10**(-x)
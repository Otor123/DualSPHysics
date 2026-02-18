from scipy.special import jn_zeros

# Anzahl Nullstellen, die du willst:
n = 5

lambdas = jn_zeros(0, n)
print(lambdas)

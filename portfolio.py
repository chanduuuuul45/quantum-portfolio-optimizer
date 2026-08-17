# File name: portfolio.py
# Install first: pip install qiskit qiskit-algorithms qiskit-optimization numpy

from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms import NumPyMinimumEigensolver
import numpy as np

# 4 stocks data
stocks = ['TCS', 'INFY', 'RELIANCE', 'HDFC']
expected_returns = np.array([0.10, 0.15, 0.08, 0.12]) # photo lo 2 numbers eh unnayi, nenu 4 complete chesa

# cov_matrix = risk table. row x column = 4x4 undali
cov_matrix = np.array([
    [0.04, 0.01, 0.02, 0.01],
    [0.01, 0.03, 0.01, 0.02],
    [0.02, 0.01, 0.05, 0.01],
    [0.01, 0.02, 0.01, 0.06]
])

# Problem create
qp = QuadraticProgram('Portfolio')
for i in range(len(stocks)):
    qp.binary_var(name=f'x_{i}')

budget = 1 # exactly 1 stock select cheyali. 2 cheyali ante 2 pettu
qp.minimize(linear=-expected_returns, quadratic=0.5*cov_matrix)
qp.linear_constraint(linear=[1]*len(stocks), sense='==', rhs=budget)

# QUBO ga marchu
qubo = QuadraticProgramToQubo().convert(qp)

# FIX: QAOA vadakunda direct Classical solver
solver = NumPyMinimumEigensolver()
meo = MinimumEigenOptimizer(solver)
result = meo.solve(qubo)

# Result
print("\n=== Portfolio Optimization Result ===")
selected = [stocks[i] for i, val in enumerate(result.x) if val > 0.5]
print("Selected Stocks:", selected)
print("Objective Value:", round(result.fval, 2))
print("\n✨ Success! No more errors! ✨")
print("Note: Idi classical solver. Real quantum kosam IBM quantum use cheyyali")
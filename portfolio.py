# File name: portfolio.py
# Install first: pip install qiskit qiskit-algorithms qiskit-optimization numpy

from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms import NumPyMinimumEigensolver
import numpy as np

stocks = ['TCS', 'INFY', 'RELIANCE', 'HDFC']
expected_returns = np.array([0.10, 0.15, 0.08, 0.12]) 

cov_matrix = np.array([
    [0.04, 0.01, 0.02, 0.01],
    [0.01, 0.03, 0.01, 0.02],
    [0.02, 0.01, 0.05, 0.01],
    [0.01, 0.02, 0.01, 0.06]
])


qp = QuadraticProgram('Portfolio')
for i in range(len(stocks)):
    qp.binary_var(name=f'x_{i}')

budget = 1 
qp.minimize(linear=-expected_returns, quadratic=0.5*cov_matrix)
qp.linear_constraint(linear=[1]*len(stocks), sense='==', rhs=budget)

qubo = QuadraticProgramToQubo().convert(qp)


solver = NumPyMinimumEigensolver()
meo = MinimumEigenOptimizer(solver)
result = meo.solve(qubo)


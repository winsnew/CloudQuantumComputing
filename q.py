import numpy as np
from BE.list import service
from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

def create_oracle(n_qubits, target):
    oracle = QuantumCircuit(n_qubits)
    target_bits = format(target, f'0{n_qubits}b')[::-1]
    for qubit in range(n_qubits):
        if target_bits[qubit] == '0':
            oracle.x(qubit)

    oracle.h(n_qubits - 1)
    oracle.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    oracle.h(n_qubits - 1)
    for qubit in range(n_qubits):
        if target_bits[qubit] == '0':
            oracle.x(qubit)
    return oracle


def create_diffusion(n_qubits):
    diffusion = QuantumCircuit(n_qubits)
    diffusion.x(range(n_qubits))
    diffusion.h(n_qubits - 1)
    diffusion.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    diffusion.h(n_qubits - 1)
    diffusion.x(range(n_qubits))
    return diffusion

def grover_algo(n_qubits, target, num_iterations):
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(range(n_qubits))
    
    oracle = create_oracle(n_qubits, target)
    diffusion = create_diffusion(n_qubits)


    for _ in range(num_iterations):
        qc.append(oracle, range(n_qubits))
        qc.append(diffusion, range(n_qubits))

    qc.measure(range(n_qubits), range(n_qubits))
    return qc

n_qubits = 3
target_private_key = 5
num_iteration = 2

grover_circuit = grover_algo(n_qubits, target_private_key, num_iteration)
transpiled = transpile(grover_circuit, service, optimization_level=3)

print(transpiled)
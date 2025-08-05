from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.circuit.library import QFT
from math import gcd
import random
import numpy as np

# Fungsi klasik untuk mencari faktor
def find_private_key_in_range(N):
    # Pilih bilangan acak a yang relatif prima terhadap N
    a = random.randint(2, N)
    while gcd(a, N) != 1:
        a = random.randint(2, N)

    print(f"Trying to factorize N={N} with a={a}")

    # Step 1: Coba temukan periode (r)
    period = quantum_period_finding(N, a)
    if period is None or period % 2 != 0:
        print(f"Period not found or invalid for a={a}.")
        return None

    # Step 2: Hitung faktor dari N menggunakan periode (r)
    x = pow(a, period // 2, N)  # a^(r/2) mod N
    factor1 = gcd(x - 1, N)
    factor2 = gcd(x + 1, N)

    if factor1 == 1 or factor2 == 1 or factor1 == N or factor2 == N:
        print("Failed to find factors.")
        return None

    return factor1, factor2

# Fungsi kuantum untuk mencari periode (r)
def quantum_period_finding(N, a):
    n_qubits = int(np.ceil(np.log2(float(N)))) + 1  # Jumlah qubit input
    circuit = QuantumCircuit(2 * n_qubits, n_qubits)

    # 1. Inisialisasi superposisi
    circuit.h(range(n_qubits))

    # 2. Operator modular exponentiation
    def modular_exponentiation(base, mod, n_qubits):
        qc = QuantumCircuit(n_qubits)
        for i in range(n_qubits):
            qc.p(base ** (2**i) % mod, i)  # Modular eksponensiasi
        return qc

    modular_qc = modular_exponentiation(a, N, n_qubits)
    circuit.compose(modular_qc, qubits=range(n_qubits), inplace=True)

    # 3. Terapkan QFT (Quantum Fourier Transform)
    qft_dagger = QFT(n_qubits).inverse()
    circuit.compose(qft_dagger, qubits=range(n_qubits), inplace=True)

    # 4. Ukur qubit
    circuit.measure(range(n_qubits), range(n_qubits))

    # Decompose sirkuit agar dapat dibaca oleh simulator
    decomposed_circuit = circuit.decompose()

    # Simulasi kuantum dengan AerSimulator
    simulator = Aer.get_backend("aer_simulator")
    result = simulator.run(decomposed_circuit, shots=1).result()
    counts = result.get_counts()
    if not counts:
        return None

    measured_value = max(counts, key=counts.get)
    period = int(measured_value, 2)

    return period

# Range angka yang ingin difaktorkan
lower_bound = 295147905179352825856
upper_bound = 590295810358705651711

# Pilih bilangan dalam rentang tersebut untuk difaktorkan
N = random.randint(lower_bound, upper_bound)
print(f"Selected number for factorization: N={N}")

# Cari faktor dari N
factors = find_private_key_in_range(N)
if factors:
    print(f"Factors of {N} are: {factors}")
else:
    print("Failed to find factors.")
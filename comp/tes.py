from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator
from qiskit_aer import Aer
from qiskit_algorithms import Grover, AmplificationProblem
from block.b1 import get_public_key_hash160

def oracle(qc: QuantumCircuit, target_hash160: int, num_qubits: int):
    binary_target = f"{target_hash160:0{num_qubits}b}"
    for i, bit in enumerate(reversed(binary_target)):
        if bit == "0":
            qc.x(i)

    qc.mcx(list(range(num_qubits)), num_qubits)
    for i, bit in enumerate(reversed(binary_target)):
        if bit == "0":
            qc.x(i)

def grover_search(start_private_key: int, end_private_key: int, target_hash160: int):
    database_size = end_private_key - start_private_key + 1
    num_qubits = database_size.bit_length()

    print(f"=== Grover's Algorithm ===")
    print(f"Rentang Private Key: {start_private_key} - {end_private_key}")
    print(f"Target Hash160: {target_hash160}")
    print(f"Jumlah Qubit: {num_qubits}")

    backend = Aer.get_backend('qasm_simulator')

    qc = QuantumCircuit(num_qubits + 1)
    qc.h(range(num_qubits))
    qc.x(num_qubits)
    qc.h(num_qubits)

    oracle(qc, target_hash160, num_qubits)

    grover_op = GroverOperator(oracle=qc)
    amplification_problem = AmplificationProblem(oracle=qc)
    grover = Grover(backend)

    result = grover.amplify(amplification_problem)
    solution = result.top_measurement

    found_index = int(solution, 2)
    found_private_key = start_private_key + found_index

    computed_hash160 = get_public_key_hash160(found_private_key)

    print(f"\nHasil Grover:")
    print(f"Private Key Ditemukan: {found_private_key}")
    print(f"Hash160 yang Dihitung: {computed_hash160}")

    if computed_hash160 == target_hash160:
        print("Cocok dengan target!")
        return found_private_key
    else:
        print("Tidak cocok dengan target.")
        return None

    


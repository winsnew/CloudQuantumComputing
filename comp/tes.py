from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import GroverOperator, MCXGate
from qiskit_aer import Aer
from qiskit_algorithms import Grover, AmplificationProblem
from .block.b1 import get_public_key_hash160

def oracle(qc: QuantumCircuit, target_hash160: int, num_qubits: int):
    binary_target = f"{target_hash160:0{num_qubits}b}"
    for i, bit in enumerate(reversed(binary_target)):
        if bit == "0":
            qc.x(i)
    
    mcx_gate = MCXGate(num_ctrl_qubits=num_qubits - 1, mode='noancilla')
    qc.append(mcx_gate, list(range(num_qubits - 1)) + [num_qubits - 1])
    
    # Uncompute X gates
    for i, bit in enumerate(reversed(binary_target)):
        if bit == "0":
            qc.x(i)

def execute_grover_search(backend, start_private_key: int, end_private_key: int, target_hash160: int):
    database_size = end_private_key - start_private_key + 1
    num_qubits = database_size.bit_length()

    print(f"\n=== Grover's Algorithm ===")
    print(f"Searching Private Key Range: {start_private_key} - {end_private_key}")
    print(f"Target Hash160: {target_hash160}")
    print(f"Number of Qubits: {num_qubits}")

    if num_qubits > 62:  # Pastikan jumlah qubit tidak melebihi batas
        raise ValueError("Jumlah qubit melebihi kapasitas backend (maksimum 62 qubit).")


    # Create a quantum circuit
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))  

    # Add oracle
    oracle(qc, target_hash160, num_qubits)

    # Wrap oracle in Grover operator
    grover_op = GroverOperator(oracle=qc)

    # Create amplification problem
    amplification_problem = AmplificationProblem(oracle=qc)

    # Run Grover's algorithm
    grover = Grover(backend)
    result = grover.amplify(amplification_problem)

    solution = result.top_measurement
    found_index = int(solution, 2)
    found_private_key = start_private_key + found_index

    # Verify the result
    computed_hash160 = get_public_key_hash160(found_private_key)

    print(f"\nGrover's Result:")
    print(f"Found Private Key: {found_private_key}")
    print(f"Computed Hash160: {computed_hash160}")

    if computed_hash160 == target_hash160:
        print("Success! The private key matches the target Hash160.")
        return found_private_key
    else:
        print("Failure! The private key does not match the target Hash160.")
        return None




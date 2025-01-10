from qiskit import QuantumCircuit
from qiskit_ibm_runtime import Sampler

def execute_circuit(backend):
    qc = QuantumCircuit(2,2)
    qc.h(0)
    qc.cx(0,1)
    qc.measure_all()

    print("\n Result: ")
    print(qc)

    print("\nRunning Backend Circuit...")
    sampler = Sampler(backend=backend)
    job = sampler.run(qc)

    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print("\nHasil eksekusi sirkuit:")
    for state, probability in counts.items():
        print(f"State: {state}, Probability: {probability:.4f}")
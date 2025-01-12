from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import Sampler

def execute_circuit(backend):
    qc = QuantumCircuit(2,2)
    qc.h(0)
    qc.cx(0,1)
    qc.measure_all()

    print("\n Result: ")
    print(qc)

    print("\nTranspilasi sirkuit untuk backend...")
    transpiled_qc = transpile(qc, backend=backend)

    print("\nSirkuit setelah ditranspilasi:")
    print(transpiled_qc)

    print("\nRunning Backend Circuit...")
    sampler = Sampler(mode=backend)
    job = sampler.run([transpiled_qc])

    result = job.result()
    

    print(result)
    
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()

print("Daftar backend yang tersedia:")
for backend in service.backends():
    print(f"- {backend}")


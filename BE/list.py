from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()

print("List Backend Avaluable :")
for backend in service.backends():
    print(f"- {backend}")


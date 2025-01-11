from BE.list import service
from comp.sample import execute_circuit

def main():
    print("\n===== Quantum Cloud Test =====")

    backends = list(service.backends())
    print("\nList Backend Available:")
    for backend in backends:
        print(f"- {backend.name}") 
    
    try:
        choose = input("\nChoose Quantum Backend (name): ").strip()
        backend = next((b for b in backends if b.name == choose), None)
        if backend is None:
            raise ValueError(f"Backend '{choose}' not found. Please choose a valid backend.")
        print(f"\nChoose backend: {backend}")
    except ValueError as e:
        print(f"\nError: {e}")
        return
    
    execute_circuit(backend)

if __name__ == "__main__":
    main()
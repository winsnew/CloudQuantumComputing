from BE.list import service
# from comp.sample import execute_circuit
from comp.tes import execute_grover_search

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
    
    start_private_key = int(input("Enter start of private key range: ").strip())
    end_private_key = int(input("Enter end of private key range: ").strip())
    target_hash160 = int(input("Enter target Hash160: ").strip(), 16)  # Input as hexadecimal

    # Execute Grover's search
    found_key = execute_grover_search(backend, start_private_key, end_private_key, target_hash160)
    if found_key:
        print(f"Private Key Found: {found_key}")
    else:
        print("Private Key not found in the given range.")

if __name__ == "__main__":
    main()
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
    
    start_random = int(input("Enter start of rand range: ").strip())
    end_random = int(input("Enter end of rand range: ").strip())
    target_num = int(input("Enter target Num: ").strip(), 16)  

    # Execute Grover's search
    found_num = execute_grover_search(backend, start_random, end_random, target_num)
    if found_num:
        print(f"State Found: {found_num}")
    else:
        print("State Number not found in the given range.")

if __name__ == "__main__":
    main()
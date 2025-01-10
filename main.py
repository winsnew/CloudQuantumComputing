from BE.list import service

def main():
    print("\n===== Quantum Cloud Test =====")

    backends = service.backends()
    for idx, backends in enumerate(backends):
        print(f"{idx + 1}. {backends}")
    
    try:
        choose = int(input("\nChoose Quantum Backend: "))
        if choose < 1 or choose > len(backends):
            raise ValueError("Choose Not Found")
        backend = backends[choose - 1]
        print(f"\nChoose backend: {backend}")
    except ValueError as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
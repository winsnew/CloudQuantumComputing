from qiskit_ibm_runtime import QiskitRuntimeService
from dotenv import load_dotenv
import os

load_dotenv()
api_token = os.getenv("token")

QiskitRuntimeService.save_account(
    token=api_token,
    channel="ibm_quantum"
)
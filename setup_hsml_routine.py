import subprocess
import os

C_routine_dir = './data_reduction/C_routine'
process = subprocess.Popen(
    "make",
    shell=True,
    cwd=C_routine_dir)
process.wait()
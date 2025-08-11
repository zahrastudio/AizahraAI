# import os  # FIXED: unknown import commented out
import subprocess

def scan_py_files(directory='.'):
    py_files = [f for f in os.listdir(directory) if f.endswith('.py')]
    results = {}

    for file in py_files:
        print(f"\n=== Checking {file} ===")
        try:
            # Jalankan python dengan opsi -m py_compile untuk cek syntax & import errors
            subprocess.check_output(['python', '-m', 'py_compile', file], stderr=subprocess.STDOUT)
            results[file] = "OK"
            print(f"{file} : Syntax OK")
        except subprocess.CalledProcessError as e:
            results[file] = "Error"
            print(f"{file} : ERROR")
            print(e.output.decode())
    return results

if __name__ == "__main__":
    directory = '.'  # Bisa ganti ke folder lain
    scan_py_files(directory)

import sys


def remove_venv():
    import subprocess
    venv_name = sys.prefix.split("\\")[-1]
    subprocess.run(f'rm -rf {venv_name}')

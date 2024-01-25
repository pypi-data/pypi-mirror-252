import subprocess

def test_pylint():
    result = subprocess.run(
        ['pylint', '.\\src\\vdot_calculator\\func_module.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Verificar se a execução foi bem-sucedida
    assert result.returncode == 0, f'Pylint execution failed:\n{result.stderr}'

    # Verificar se a saída contém o rating esperado
    assert 'Your code has been rated at 10.00/10' in result.stdout, \
        f'Unexpected Pylint rating:\n{result.stdout}'


def test_mypy():
    result = subprocess.run(
        ['mypy', '.\\src\\vdot_calculator\\func_module.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Verificar se a execução foi bem-sucedida
    assert result.returncode == 0, f'mypy execution failed:\n{result.stderr}'

    # Verificar se a saída contém o rating esperado
    assert 'Success: no issues found in 1 source file' in result.stdout, \
        f'issues found in mypy execution\n{result.stdout}'
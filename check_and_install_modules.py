import importlib.util
import subprocess

required_modules = [
    'yfinance',
    'pandas',
    'numpy',
    'matplotlib',
    # 'backtrader',
]

# Check if required modules are installed
missing_modules = [
    module for module in required_modules
    if not importlib.util.find_spec(module)
]

# Install missing modules using pip if any
if missing_modules:
    print(f"Installing missing modules: {', '.join(missing_modules)}")

    try:
        subprocess.run(['pip', 'install'] + missing_modules, check=True)
        print('Modules installed successfully.')
    except subprocess.CalledProcessError as e:
        print(f"Error installing modules: {e}")
        exit(1)
else:
    print('All Modules Exist.')

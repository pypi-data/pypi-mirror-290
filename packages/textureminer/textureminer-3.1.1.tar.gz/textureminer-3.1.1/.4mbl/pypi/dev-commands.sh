exit 0 #! this is a shell file because syntax highlighting is nice, but it's not meant to be run as a script

# install/upgrade utils
py -m pip install --upgrade pip build twine

# build
python -c "import toml; data=toml.load('pyproject.toml'); data['project']['version']='0.0.0'; toml.dump(data, open('pyproject.toml', 'w'))" && py -m build

# install from file
py -m pip uninstall textureminer -y && py -m pip install ./dist/textureminer-0.0.0-py3-none-any.whl

# install from pypi
rmrf .venv/ && py -m venv .venv/ && .venv/Scripts/activate && py -m pip install --upgrade textureminer


# single line (assumes venv is already active)
rmrf .venv/ && py -m venv .venv/ && .venv/Scripts/activate && py -m pip install --upgrade pip build && python -c "import toml; data=toml.load('pyproject.toml'); data['project']['version']='0.0.0'; toml.dump(data, open('pyproject.toml', 'w'))" && py -m build && pip uninstall textureminer -y && py -m pip install ./dist/textureminer-0.0.0-py3-none-any.whl && textureminer -v && textureminer --help && textureminer -j --scale 1 --flatten && textureminer -b --scale 1 --flatten



from setuptools import setup

if __name__ == "__main__":
    setup(cffi_modules="imm/_build_ext.py:ffibuilder")

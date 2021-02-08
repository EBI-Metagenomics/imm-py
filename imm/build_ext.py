import os
from os.path import join
from typing import List

from cffi import FFI

__all__ = ["ffibuilder", "imm_float"]

imm_float = "float"
IMM_DOUBLE_PRECISION = os.environ.get("IMM_DOUBLE_PRECISION", "False").lower()
if IMM_DOUBLE_PRECISION in ["true", "1", "on"]:
    imm_float = "double"

ffibuilder = FFI()
libs = ["imm"]

folder = os.path.dirname(os.path.abspath(__file__))

with open(join(folder, "imm.h"), "r") as f:
    ffibuilder.cdef(f.read().replace("__IMM_FLOAT__", imm_float))

extra_link_args: List[str] = []
if "IMM_EXTRA_LINK_ARGS" in os.environ:
    extra_link_args += os.environ["IMM_EXTRA_LINK_ARGS"].split(os.pathsep)

ffibuilder.set_source(
    "imm._ffi",
    r"""
    #include "imm/imm.h"
    """,
    libraries=libs,
    extra_link_args=extra_link_args,
    language="c",
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)

# SPDX-FileCopyrightText: Copyright 2021, Siavash Ameli <sameli@berkeley.edu>
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileType: SOURCE
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the license found in the LICENSE.txt file in the root
# directory of this source tree.


# =======
# Imports
# =======

from .._definitions.types cimport LongIndexType
from .cu_linear_operator cimport cuLinearOperator


# =======
# Externs
# =======

cdef extern from "cu_affine_matrix_function.h":

    cdef cppclass cuAffineMatrixFunction[DataType](cuLinearOperator):

        cuAffineMatrixFunction() except +

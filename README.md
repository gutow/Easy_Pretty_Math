# Easy_Pretty_Math
__Try in Binder:__
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gutow/Easy_Pretty_Math.git/master)

__Display Math Operations (DMO)__

Easy way(s) to get pretty math output in Jupyter notebooks. Defines a wrapper function to get nice
typesetting of math operations. Overrides most sympy functions to generate typesetting of math operations
, not just results. There is an option to make the typesetting automatic.

This is intended mostly to aid with teaching students, who often have difficulty translating code into the symbolic math operations they are used to.

If the file `algebraic_equations.py` is available `DMO` will also import and play nice with equations as defined in that
file.

The utility functions are:

* `dmo_auto()`: Calling this function causes dmo aware functions (most sympy functions plus `diff(expr)` and `integ(expr)`)
to display a typeset version of the operations carried out by the function. The call `dmo_auto(status=False)` turns this off. Turned on by default by the call `from Display_Math_Operations import *`.
* `dmo()`: Passing a valid sympy expression or assignment statement to this function causes the expression or assignment to be evaluated and the operation output as typeset math. Also takes the optional argument `code=True`, causing it to try to output the result of the operation as plain code as well. This will just yield another typeset version of the result if `init_printing(pretty_print=True)` is set rather than `init_printing(pretty_print=False)`.

_To suppress the display of typeset operations pass `display_op=False` to an operation or function._

__This automated operation display will only work inside a Jupyter or IPython environment__

The code making this work can be viewed in the file Display_Math_Operations.py. **_As this is not yet a pip package this file must be in the same directory as the notebook you wish to use it with._**


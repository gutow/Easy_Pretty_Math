"""
__Display Math Operations (DMO)__

author: Jonathan Gutow <gutow@uwosh.edu>
date: May 2020
license: GPL V3+

Easy way(s) to get pretty math output in Jupyter notebooks. Defines a wrapper function to get nice
typesetting of math operations. Overrides most sympy functions to generate typesetting of math operations
, not just results. There is an option to make the typesetting automatic.

This is intended mostly to aid with teaching students, who often have difficulty translating code into the symbolic math operations they are used to.

The utility functions are:

* `dmo_auto()`: Calling this function causes dmo aware functions (most sympy functions plus `diff(expr)` and `integ(expr)`)
to display a typeset version of the operations carried out by the function. The call `dmo_auto(status=False)` turns this off.
* `dmo()`: Passing a valid sympy expression or assignment statement to this function causes the expression or assignment to be evaluated and the operation output as typeset math. Also takes the optional argument `code=True`, causing it to try to output the result of the operation as plain code as well. This will just yield another typeset version of the result if `init_printing(pretty_print=True)` is set rather than `init_printing(pretty_print=False)`.

_To suppress the display of typeset operations pass `display_op=False` to an operation or function._

__Examples__

```
>>>from Display_Math_Operations import * #Loads DMO and sympy into the global namespace
    Algebraic equations and Sympy successfully imported.
    Automatic typesetting of output disabled so output code can be copied into code cells.
      To enable automatic typesetting of output issue the command `init_printing(pretty_print=True)`.
    Automatic display of math operation activated for `dmo aware` operations.
>>>sp.var('a b c')
>>>t=a-b/c
>>>dmo(t)
    will output a typeset version of t=a-b/c
>>>dmo(p=a/b+c)
    will output a typeset version of p=a/b+c
>>>sin(t)
    will output a typeset version of sin(t)=sin(a - b/c)
```

```
>>>integ(t,c)
    will output a typeset version of integral(t wrt c) = integral((a-b/c) wrt c) = a*c - b*log(c)
>>>diffdmo(t,c)
    will output a typeset version of derivative(t wrt c) = derivative((a-b/c) wrt c) = b/c**2
```

_`integ()` and `diffdmo()` are the only two dmo aware operations so far._

__This automated operation display will only work inside a Jupyter or IPython environment__
"""
try:
    from algebraic_equation import *
    print('Algebraic equations and Sympy successfully imported.')
except ImportError:
    from sympy import *
    print('WARNING: unable to import algebraic_equation. Defaulting to just Sympy.')
    print('Sympy successfully imported.')
from IPython.display import HTML
import inspect

def get_ipython_depth():
    is_not_ipython_global=True
    frame =inspect.currentframe()
    global_dict=frame.f_globals
    try:
        namestr=global_dict['__name__']
        docstr=global_dict['__doc__']
    except KeyError:
        namestr=''
    if (namestr=='__main__') and (docstr =='Automatically created module for IPython interactive environment'):
        is_not_ipython_global=False
    depth = 0
    try:
        while (is_not_ipython_global):
            nextframe = frame.f_back
            frame=nextframe
            depth+=1
            try:
                global_dict=frame.f_globals
                namestr=global_dict['__name__']
                docstr=global_dict['__doc__']
            except KeyError:
                namestr=''
            if (namestr=='__main__') and (docstr =='Automatically created module for IPython interactive environment'):
                is_not_ipython_global=False
    except AttributeError:
        raise AttributeError('Unable to find `__main__` of interactive session. Are you running in Jupyter or IPython?')
    return depth

def get_ipython_globals():
    is_not_ipython_global=True
    frame =inspect.currentframe()
    global_dict=frame.f_globals
    try:
        namestr=global_dict['__name__']
        docstr=global_dict['__doc__']
        #print(global_dict['__name__'])
        #print(docstr)
    except KeyError:
        namestr=''
    if (namestr=='__main__') and (docstr =='Automatically created module for IPython interactive environment'):
        is_not_ipython_global=False
    depth = 0
    try:
        while (is_not_ipython_global):
            nextframe = frame.f_back
            frame=nextframe
            depth+=1
            try:
                global_dict=frame.f_globals
                namestr=global_dict['__name__']
                docstr=global_dict['__doc__']
                #print(global_dict['__name__'])
            except KeyError:
                namestr=''
            if (namestr=='__main__') and (docstr =='Automatically created module for IPython interactive environment'):
                is_not_ipython_global=False
    except AttributeError:
        raise AttributeError('Unable to find `__main__` of interactive session. Are you running in Jupyter or IPython?')
    return(global_dict)

def search_ipython_globals(*var):
    string_names = list(var)
    global_dict=get_ipython_globals()
    for var_name in global_dict:
        #print(var_name+': '+str(global_dict[var_name]))
        for i in range(len(var)):
            if (str(global_dict[var_name])==str(string_names[i])) and not (var_name.startswith('_')):
                #print(var_name+': '+str(global_dict[var_name]))
                string_names[i] = var_name
    return string_names

def dmo_auto(status=True):
    '''
    sets the status of dmo (display math operation) to True by default or False if `status=False`
    is passed to the function. If true dmo aware functions will attempt to display typeset
    expressions for the operations carried out. If False they will only display typeset expressions
    for the operations if `display_op=True` is set in the function call. See the documentation for
    each function.
    '''
    global_dict=get_ipython_globals()
    global_dict['_dmo_auto_']=status
    return(print('Automatic display of math operation activated for `dmo aware` operations.'))

def dmo(*exprs,**kwarg): #Display math operation
    '''
    Pass one of:
    *exprs:     any valid symbolic math expression or function call (e.g. 2*x, sin(2*x)).
    **kwarg:    any valid symbol equal to an expression or function call (e.g. P=n*R*T/V,
                r=sin(theta)). This must be the first item with an equal sign appearing
                in the list of arguments.
                
                additionally you can add these options:
                code=True, if you want the code version of the evaluated expression to
                    appear in the cell output. Useful if you want to copy and edit into
                    another code cell. Note if `sympy.init_printing(pretty_print=True)` is
                    set the code will still be displayed as typeset. Call `sympy.init_printing`
                    with `pretty_print=False` to get non-typeset output.
    
    In an IPython/Jupyter notebook will display a typeset version of the operation and return
    the expression to the namespace for further operations. The function tries to identify
    the actual string (name) passed for the expression and output the typeset expression 
    `name=result of the operation`. If it cannot identify the actual string passed it just
    outputs the typeset result of the operation.
    
    J. Gutow May 2020.
    '''
    code = kwarg.pop('code', None)
    expr=None
    if(len(exprs) >= 1):
        expr = exprs[0] #ignore others.
        namestr=str(search_ipython_globals(expr)[0])
        if (namestr=='') or (namestr==str(expr)):
            display(HTML('$$'+latex(expr)+'$$'))
        else:
            display(HTML('$$'+latex(namestr)+'\equiv '+latex(expr)+'$$'))
    else:
        key = list(kwarg)[0] #ignore all but first.
        exprstr=str(kwarg[key])
        expr = kwarg[key]
        #print('string:'+exprstr+' expression:'+str(expr))
        ltop=''
        if not(exprstr==str(expr)):# Trying to get the expression without substitution/evaluation
            ltop=latex(exprstr)+'='
        display(HTML('$$'+(key)+'\equiv '+ltop+latex(expr)+'$$'))
        get_ipython_globals()[key]=expr #inject into namespace.
    # get_ipython_globals()['_']=expr #inject into last result messes with IPython.
    if (code):
        return(expr)
    pass

class Function(Function):
    def __new__(cls, *arg, **kwargs):
        display_op=kwargs.pop('display_op',None) # For getting nice display from bare function.
        try:
            dmo_auto = get_ipython_globals()['_dmo_auto_']
        except KeyError:
            dmo_auto=False
        if (get_ipython_depth() > 2):
            dmo_auto=False
        if (display_op==False): #force overide of dmo_auto
            dmo_auto=False
        if (dmo_auto) or (display_op):
            cls._dmo(cls,*arg,**kwargs)
        return(super().__new__(cls, *arg, **kwargs))
    
    def _dmo(cls, *arg, **kwargs):
        result=super().__new__(cls, *arg, **kwargs)
        namestr=search_ipython_globals(*arg)
        for i in range(len(arg)):
            temptype=type(arg[i])
            if (temptype is int) or (temptype is float):
                namestr[i]=arg[i]
        ltop1=''
        kwargs['evaluate']=False
        showoper1=False
        for val in namestr:
            if (type(val)==str):
                showoper1=True
        if (showoper1):
            oper1=super().__new__(cls, *namestr, **kwargs)
            ltop1=latex(oper1)+'='
        oper=super().__new__(cls, *arg, **kwargs)
        ltoper=''
        if not(oper==result):
            ltoper=latex(oper)+'='            
        display(HTML('$$'+ltop1+ltoper+latex(result)+'$$'))
        

for func in functions.__all__:
    execstr = 'class '+str(func)+'(Function, '+str(func)+'):\n    pass\n'
    #print(execstr)
    # listed in `skip` cannot be extended because of `mro` error or `metaclass conflict`.
    skip=['sqrt','root','Min','Max','Id','real_root','cbrt','unbranched_argument','polarify','unpolarify',
         'piecewise_fold','E1','Eijk','bspline_basis','bspline_basis_set','interpolating_spline','jn_zeros',
          'jacobi_normalized','Ynm_c']
    if func not in skip:
        exec(execstr,globals(),locals())
        
def integ(f, *args, **kwargs):
    '''
    Wrapper for `sympy.integrate()/Integral()`. That can output typeset expressions for the operations
    carried out before returning the result. Designed primarily for teaching and display purposes.
    
    This function is display math operation (dmo) aware. Thus if dmo_auto() is called at the beginning of
    a notebook all calls will result in typeset operation output unless the optional kwarg: `display_op` is
    set to False.
    
    Takes one additional optional kwarg that is not used by sympy.integrate():
        display_op: True generates typeset math operation output, False suppresses the output.

    '''
    display_op=kwargs.pop('display_op',None) # For getting nice display from bare function.
    result=integrate(f,*args,**kwargs)
    try:
        dmo_auto = get_ipython_globals()['_dmo_auto_']
    except KeyError:
        dmo_auto=False
    if (display_op==False): #force overide of dmo_auto
        dmo_auto=False
    oper=None
    if (dmo_auto) or (display_op):
        namestr=str(search_ipython_globals(f)[0])
        ltop1=''
        if not(namestr==''):
            oper1=Integral(namestr,*args)
            ltop1=latex(oper1)+'='
        oper=Integral(f,*args,**kwargs)
        ltop=''
        if not(oper==oper1) and not(oper==result):
            ltop=latex(oper)+'='
        # TODO show subtraction step in computing integrals with limits
        #      question: best way to represent this for multiple integrals?
        display(HTML('$$'+ltop1+ltop+latex(result)+'$$'))
    return(result)

def diffdmo(f,*symbols,**kwargs):
    '''
    Wrapper for sympy.diff(). That can output typeset expressions for the operations carried out before
    returning the result. Designed primarily for teaching and display purposes.
    
    This function is display math operation (dmo) aware. Thus if dmo_auto() is called at the beginning of
    a notebook all calls will result in typeset operation output unless the optional kwarg: display_op is
    set to False.
    
    Takes one additional optional kwarg that is not used by sympy.diff():
        display_op: True generates typeset math operation output, False suppresses the output.
    '''
    def symparse(symbols):
        syms=[]
        pwrs =[]
        for k in range(len(symbols)):
            tempsym = symbols[k]
            #print('tempsym = '+str(tempsym))
            if not (type(tempsym) is int):
                syms.append(tempsym)
                pwrs.append(1)
            else:
                pwrs[k-1]+=tempsym-1
        return(syms,pwrs)

    display_op=kwargs.pop('display_op',None) # For getting nice display from bare function.
    result=diff(f,*symbols,**kwargs)
    try:
        dmo_auto = get_ipython_globals()['_dmo_auto_']
    except KeyError:
        dmo_auto=False
    if (display_op==False): #force overide of dmo_auto
        dmo_auto=False
    oper=None
    if (dmo_auto) or (display_op):
        namestr=str(search_ipython_globals(f)[0])
        syms,pwrs = symparse(symbols)
        totpwr = sum(pwrs)
        totpwrstr=''
        if not(totpwr==1):
            totpwrstr=str(totpwr)
        ltop = ''
        ltdenom=''
        for i in range(len(syms)):
            pwrstr=''
            if not(pwrs[i]==1):
                pwrstr=str(pwrs[i])
            else:
                pwrstr=''
            ltdenom+='\\partial '+str(syms[i])+'^{'+pwrstr+'} '
        if (namestr=='') or (namestr==str(f)):
            ltnum='\\partial^{'+totpwrstr+'} '
            ltop='\\frac{'+ltnum+'}{'+ltdenom+'}{\\left('+latex(f)+'\\right)}'
        else:
            ltnum ='\\partial^{'+totpwrstr+'}'+str(namestr)+' '
            ltop ='\\frac{'+ltnum+'}{'+ltdenom+'}='
            ltnum='\\partial^{'+totpwrstr+'} '
            ltop+='\\frac{'+ltnum+'}{'+ltdenom+'}{\\left('+latex(f)+'\\right)}'
        display(HTML('$$'+ltop+'='+latex(result)+'$$'))
    return(result)


"""
def diff(f, *args, **kwargs):
    '''
    Wrapper for `sympy.diff()/Derivative()`. That can output typeset expressions for the operations
    carried out before returning the result. Designed primarily for teaching and display purposes.
    
    This function is display math operation (dmo) aware. Thus if dmo_auto() is called at the beginning of
    a notebook all calls will result in typeset operation output unless the optional kwarg: `display_op` is
    set to False.
    
    Takes one additional optional kwarg that is not used by sympy.integrate():
        display_op: True generates typeset math operation output, False suppresses the output.

    '''
    display_op=kwargs.pop('display_op',None) # For getting nice display from bare function.
    result=sp.diff(f,*args,**kwargs)
    try:
        dmo_auto = get_ipython_globals()['_dmo_auto_']
    except KeyError:
        dmo_auto=False
    if (display_op==False): #force overide of dmo_auto
        dmo_auto=False
    oper=None
    if (dmo_auto) or (display_op):
        namestr=search_ipython_globals(f)
        ltop1=''
        kwargs['evaluate']=False
        if not(namestr==''):
            oper1=sp.Derivative(namestr,*args,**kwargs)
            ltop1=sp.latex(oper1)+'='
        oper=sp.Derivative(f,*args,**kwargs)
        display(HTML('$$'+ltop1+sp.latex(oper)+'='+sp.latex(result)+'$$'))
    return(result)
"""
# Turning off sympy auto pretty printing as that seems to be the default in latest Jupyter/Sympy.
init_printing(pretty_print=False)
print('Automatic typesetting of output disabled so output code can be copied into code cells.')
print('    To enable automatic typesetting of output issue the command `init_printing(pretty_print=True)`.')
# Turning on auto display math operations
dmo_auto()
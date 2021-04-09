# A simple lambda translator and evaluator
# - Converts a lambda-expression into SKI-expression (translate)
#   and then reduce it using a combinator graph reduction engine (evaluate)
# - Lambda to SKI-expression conversion is done according to bracket abstraction

from functools import reduce

# Abstract Syntax for Lambda Expressions
_Lam_ = 'Lam'
_App_ = 'App'

def Lam(vars, exp): # Associates right
    if type(vars) == str:
        vars = [vars]
    return reduce(lambda w, a: (_Lam_, a, w), vars[::-1], exp)

def App(*exps):     # Associates left
    return reduce(lambda w, a: (_App_, w, a), exps[1:], exps[0])

def Var(name):
    return name

def is_lambda(exp):
    return type(exp) == tuple and exp[0] == _Lam_

def is_application(exp):
    return type(exp) == tuple and exp[0] == _App_

def is_variable(exp):
    return type(exp) == str

def ppLamExp(exp):      # Pretty-printer
    if is_lambda(exp):
        return f"(\\{''.join(exp[1])}.{ppLamExp(exp[2])})"
    elif is_application(exp):
        exp_1 = ppLamExp(exp[1])
        if exp_1[0] == '(' and exp_1[-1] == ')':
            exp_1 = exp_1[1:-1]
        return f"({exp_1} {ppLamExp(exp[2])})"
    elif is_variable(exp):
        return exp

# Translate a lambda-expression into an SKI-expression.
#   Implements so-called the bracket abstraction algorithm
def translate(exp):
    if is_variable(exp):
        return exp                                      # Rule 1
    if is_application(exp):                             # Rule 2
        return App(translate(exp[1]), translate(exp[2]))
    # if is_lambda(exp):
    var, eps = exp[1], exp[2]
    if var not in free_vars(eps):
        return App("K", translate(eps))                 # Rule 3
    if is_variable(eps) and eps == var:
        return "I"  # == App("S", "K", "K")             # Rule 4
    if is_lambda(eps) and var in free_vars(eps[2]):
        return translate(Lam(var, translate(eps)))      # Rule 5
    if is_application(eps):                             # Rule 6
        return App("S", translate(Lam(var, eps[1])), translate(Lam(var, eps[2])))

def free_vars(exp):
    def collect(vs, exp):
        if is_variable(exp):
            return [] if exp in vs else [exp]
        if is_application(exp):
            return collect(vs, exp[1]) + collect(vs, exp[2])
        if is_lambda(exp):
            return collect([exp[1]] + vs, exp[2])
    return set(collect([], exp))

def ppSkiExp(ski):      # Pretty-printer
    # Optimize S(KK)I which is equivalent to K
    ppExp = ppLamExp(ski).replace(" ", "").replace("(S(KK)I)", "K")
    if ppExp[0] == '(' and ppExp[-1] == ')':
        ppExp = ppExp[1:-1]
    return ppExp

# Naive evaluator for SKI-expressions
def evaluate(ski):
    if is_variable(ski):
        return ski
    if is_application(ski):
        ski1, ski2 = ski[1], ski[2]
        # App(I, x)
        if ski1 == 'I':
            return evaluate(ski2)
        # App((K x) y)
        if is_application(ski1) and ski1[1] == 'K':
            return evaluate(ski1[2])
        # (((S x) y) z)
        if is_application(ski1) and is_application(ski1[1]) and ski1[1][1] == 'S':
            return evaluate(App(App(ski1[1][2], ski2), App(ski1[2], ski2)))
        # All else
        red1 = evaluate(ski1)
        red2 = evaluate(ski2)
        if red1 == ski1 and red2 == ski2:
            return ski
        else:
            return evaluate(App(red1, red2))
    return ski

# Examples
true = Lam(["x", "y"], "x")
false = Lam(["x", "y"], "y")
zero = Lam(["f", "x"], "x")
one = Lam(["f", "x"], App("f", "x"))
two = Lam(["f", "x"], App("f", App("f", "x")))
add = Lam(["m", "n", "f", "x"], App("m", "f", App("n", "f", "x")))
three = App(add, one, two)
succ = Lam(["n", "f", "x"], App("f", App("n", "f", "x")))
pred = Lam(["n", "f", "x"], App("n", Lam(["g", "h"], App("h", App("g", "f"))),
                                     Lam(["u"], "x"), Lam(["u"], "u")))
mul = Lam(["m", "n", "f"], App("m", App("n", "f")))
square = Lam("n", App(mul, "n", "n"))
is0 = Lam("n", App("n", Lam("x", false), true))

# For Church numeral evaluation
# e.g. eval('s(s(s(s(s(s(s(s(s(s(s(sz)))))))))))') evaluates to 12
s = lambda n: n+1
z = 0
sz = s(z)

# A sequence of steps to calculate a lambda expression
def eval_lambda(demo_name, exp):
    ski = translate(exp)                                # Convert to an SKI-expression
    print(demo_name, "=", ppSkiExp(ski), end=" ==> ")
    eval_on_sz = ppSkiExp(evaluate(App(ski, "s", "z"))) # Evaluate using "s" "z" as arguments
    print(eval_on_sz, "which evaluates to", eval(eval_on_sz))
    print()

eval_lambda("add(one, two)", App(add, one, two))
eval_lambda("mul(two, three)", App(mul, two, three))
eval_lambda("square(three)", App(square, three))
eval_lambda("mul(add(one, two), square(three))",
    App(mul, App(add, one, two), App(square, three)))


"""
6.1010 Spring '23 Lab 10: Symbolic Algebra
"""
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.

# LOOKUP DICTIONARIES

operations = {"+": lambda x, y: x + y, 
              "-": lambda x, y: x - y, 
              "*": lambda x, y: x * y, 
              "/": lambda x, y: x / y,
              "**": lambda x, y: x ** y}

# HELPER FUNCTIONS

def to_symbol(numstr):
    """
    Converts a number or variable into their equivalent Symbols
    """
    if isinstance(numstr, (int, float)):
        return Num(numstr)
    elif isinstance(numstr, str):
        return Var(numstr)
    elif isinstance(numstr, Symbol):
        return numstr
    else:
        raise TypeError
    
def tokenize(expr_str):
    """
    Tokenize parts of an expression into a list
    """
    separate_pars = ""
    for char in expr_str:
        if char == "(":
            separate_pars += " ( "
        elif char == ")":
            separate_pars += " ) "
        else:
            separate_pars += char
    tokenized_list = separate_pars.split()
    return tokenized_list

def parse(tokenized_list):
    """
    Parse the elements of a tokenized list into an expression
    """
    def parse_expression(index):
        """
        Parses one expression of the tokenized list
        """
        try:
            float(tokenized_list[index])
            return Num(float(tokenized_list[index])), index + 1
        except ValueError:
            if tokenized_list[index] != "(":
                return Var(tokenized_list[index]), index + 1
            else:
                left_side, index = parse_expression(index + 1)
                operation = tokenized_list[index]
                right_side, index = parse_expression(index + 1)
                return operations[operation](left_side, right_side), index + 1
    parsed_expression = parse_expression(0)[0]
    return parsed_expression

def expression(expr):
    """
    Creates a symbolic expression from a string input
    """
    return parse(tokenize(expr))

# CLASSES

class Symbol:
    """
    Class representing symbolic expressions
    """
    precedence = 4
    left_parens = False
    right_parens = False
    
    def __add__(self, other):
        return Add(self, other)
    
    def __radd__(self, other):
        return Add(other, self)
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __rsub__(self, other):
        return Sub(other, self)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __rmul__(self, other):
        return Mul(other, self)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __rtruediv__(self, other):
        return Div(other, self)
    
    def __pow__(self, other):
        return Pow(self, other)
    
    def __rpow__(self, other):
        return Pow(other, self)
    
    def simplify(self):
        return self


class Var(Symbol):
    """
    Variable of string input.
    """
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var('{self.name}')"

    def eval(self, mapping):
        if self.name in mapping:
            return mapping[self.name]
        else:
            raise NameError
    
    def __eq__(self, other):
        if not isinstance(other, Var):
            return False
        return self.name == other.name
    
    def deriv(self, var):
        if var == self.name:
            return Num(1)
        else:
            return Num(0)



class Num(Symbol):
    """
    Numeric variable with int or float input
    """
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Num({self.n})"
    
    def eval(self, mapping):
        return self.n
    
    def __eq__(self, other):
        if isinstance(other, Num):
            return self.n == other.n
        elif isinstance(other, (int,float)):
            return self.n == other
        else:
            return False
    
    def deriv(self, var):
        return Num(0)
    
class BinOp(Symbol):
    """
    Operation of two symbolic expressions, with a left and right side
    """
    def __init__(self, left_sym, right_sym):
        self.left = to_symbol(left_sym)
        self.right = to_symbol(right_sym)

    def __str__(self):
        left_str = str(self.left)
        right_str = str(self.right)
        if self.left.precedence < self.precedence or \
            self.left.precedence <= self.precedence and self.left_parens:
            left_str = "(" + left_str + ")"
        if self.right.precedence < self.precedence or \
            self.right.precedence == self.precedence and self.right_parens:
            right_str = "(" + right_str + ")"
        return left_str + " " + self.operation + " " + right_str

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})"
    
    def eval(self, mapping):
        return operations[self.operation]\
            (self.left.eval(mapping), self.right.eval(mapping))
    
    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return False
        return self.left == other.left and self.right == other.right
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(operations[self.operation](left.n, right.n))
        else:
            return self.simplify_more(left, right)

class Add(BinOp):
    """
    Addition subclass of BinOp
    """
    operation = "+"
    precedence = 0
    left_parens = False
    right_parens = False

    def deriv(self, var):
        return self.left.deriv(var) + self.right.deriv(var)
        
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(operations[self.operation](left.n, right.n))
        else:
            if right == 0:
                return left
            elif left == 0:
                return right
            else:
                return left + right

class Sub(BinOp):
    """
    Subtraction subclass of BinOp
    """
    operation = "-"
    precedence = 0
    right_parens = True
    
    def deriv(self, var):
        return self.left.deriv(var) - self.right.deriv(var)
        
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(operations[self.operation](left.n, right.n))
        else:
            if right == 0:
                return left
            else:
                return left - right
    
class Mul(BinOp):
    """
    Multiplication subclass of BinOp
    """
    operation = "*"
    precedence = 1
    left_parens = False
    right_parens = False

    def deriv(self, var):
        return self.left.deriv(var) * self.right + self.left * self.right.deriv(var)
        
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(operations[self.operation](left.n, right.n))
        else:
            if right == 0 or left == 0:
                return Num(0)
            if right == 1:
                return left
            if left == 1:
                return right
            else:
                return left * right
    
class Div(BinOp):
    """
    Division subclass of BinOp
    """
    operation = "/"
    precedence = 1
    left_parens = False
    right_parens = True

    def deriv(self, var):
        return (self.left.deriv(var) * self.right - self.left \
                * self.right.deriv(var)) / (self.right * self.right)
        
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(operations[self.operation](left.n, right.n))
        else:
            if left == 0:
                return Num(0)
            elif right == 1:
                return left
            else:
                return left / right
        
class Pow(BinOp):
    """
    Power subclass of BinOp
    """
    operation = "**"
    precedence = 2
    left_parens = True
    right_parens = False

    def deriv(self, var):
        if not isinstance(self.right, Num):
            raise TypeError
        else:
            return self.right * self.left ** (self.right - 1) * self.left.deriv(var)
        
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(operations[self.operation](left.n, right.n))
        else:
            if right == 0:
                return Num(1)
            elif right == 1:
                return left
            elif left == 0:
                return Num(0)
            else:
                return left ** right


if __name__ == "__main__":
    #doctest.testmod()
    # exp = Add(Num(0), Var('x'))
    #print(repr(Add(Num(0), Var('x'))))
    #print(exp)
    # x = Add(Var("x"), Var("y"))
    # print(z.eval({"x": 3, "y": 5}))
    # z = Add(Var('x'), Sub(Var('y'), Mul(Var('z'), Num(2))))
    # print(z)
    # print(z.eval({'x': 7, 'y': 3, 'z': 9}))
    #print(z.eval({"x": 3, "y": 5}))
    # print(Num(2) != Var('v'))
    # a = Var("x") * Var("x")
    # print(a.deriv("x"))
    # print((Add("x", 0)).simplify())
    # x = Var('x')
    # y = Var('y')
    # z = 2 * x - x * y + 3 * y
    #print(repr(z))
    #print(z.simplify())
    #b = z.deriv('x')
    #print(repr(b))
    #print(b.simplify())
    # print(z.deriv('y'))
    # print(z.deriv('y').simplify())
    # print(Add(Add(Num(2), Num(-2)), Add(Var('x'), Num(0))).simplify())
    #print(Add(Num(2), Num(1)).simplify())
    #result = Mul(Add(Num(0), Var('x')), Var('z')).simplify()
    #expected = Mul(Var('x'), Var('z'))
    #print(result)
    #print(expected)
    #print(repr(Add(Num(3), Num(2)).simplify()))
    # a = tokenize("(3 + x) + -200.5 * (3 + y)")
    # print(a)
    # b = parse(a)
    # print(b)
    # c = "(3 + x) + -200.5 * (3 + y)"
    # d = expression(c)
    # print(d)

    #print(Num(0) == 0)
    #print(repr(Num(2) + Var("x")))

    # result = '((z * 3) + 0)'
    # print(tokenize(result))
    # print(expression(result))
    #expected = Add(Mul(Var('z'), Num(3)), Num(0))

    #print(Pow(Pow(Num(2), Num(3)), Num(4)))

    # print(Pow(Add(Var('x'), Var('y')), Num(1)).simplify())


    # result = Mul(Add(Num(0), Var('x')), Var('z')).simplify()
    # expected = Mul(Var('x'), Var('z'))
    # print(result)
    #print(expected)
    #print(Add(Num(0), Var('x')).simplify())

    # exp = Div(Num(1), Sub(Num(0), Sub(Var('x'), \
    #   Add(Sub(Num(0), Mul(Div(Num(0), Var('x')), Num(1))), Num(0)))))
    # cn = [Add, Sub, Mul, Div]
    # for i, c1 in enumerate(cn):
    #     for c2 in cn[i+1:]:
    #         e1 = c1.simplify(exp)
    #         e2 = c2.simplify(exp)
    #         print(e1)
    #         print(e2)
    pass

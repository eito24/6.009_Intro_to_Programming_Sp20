def _sympify(x):
    if isinstance(x,(int,float)):
        return Num(x)
    elif isinstance(x,str):
        return Var(x)
    elif isinstance(x,Expr):
        return x
    else:
        raise TypeError(f"can't cast {x!r} into Expr")

class Expr:
    right_same_prec_parens=False
    def _combine(self,other,class_,reverse=False):
        if reverse:
            return class_(other,self)
        else:
            return class_(self,other)
    def __add__(self,other):
        return self._combine(other,Add)
    
    def __sub__(self,other):
        return self._combine(other,Sub)
    
    def __mul__(self,other):
        return self._combine(other,Mul)
    
    def __truediv__(self,other):
        return self._combine(other,Div)
    
    def __radd__(self,other):
        return self._combine(other,Add,reverse=True)
    
    def __rsub__(self,other):
        return self._combine(other,Sub,reverse=True)
    
    def __rmul__(self,other):
        return self._combine(other,Mul,reverse=True)
    
    def __rtruediv__(self,other):
        return self._combine(other,Div,reverse=True)

class Var(Expr):
    prec=float('inf')
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Var({self.name!r})'
    
    def deriv(self,var):
        return Num(1 if self.name == var else 0)

class Num(Expr):
    prec=float('inf')
    def __init__(self, n):
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f'Num({self.n!r})'
    
    def deriv(self,var):
        return Num(0)

class BinOp(Expr):
    def __init__(self,left,right):
        self.left=_sympify(left)
        self.right=_sympify(right)

    def __str__(self):
        lstr=str(self.left)
        if self.left.prec < self.prec:
            lstr=f'({lstr})'
        rstr=str(self.right)
        if (self.right.prec < self.prec or self.right_same_prec_parens and self.right.prec==self.prec):
            rstr=f'({rstr})'
        return f'{lstr} {self.op_string} {rstr}'
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.left!r},{self.right!r})'

class Add(BinOp):
    prec=1
    op_string='+'
    def deriv(self,var):
        return self.left.deriv(var) + self.right.deriv(var)

class Sub(BinOp):
    prec=1
    right_same_prec_parens=True
    op_string='-'
    def deriv(self,var):
        return self.left.deriv(var) - self.right.deriv(var)

class Mul(BinOp):
    prec=2
    op_string='*'
    def deriv(self,var):
        dleft=self.left.deriv(var)
        dright=self.right.deriv(var)
        return (self.left*dright)+(self.right*dleft)

class Div(BinOp):
    prec=2
    right_same_prec_parens=True
    op_string='/'
    def deriv(self,var):
        dleft=self.left.deriv(var)
        dright=self.right.deriv(var)
        return ((self.right*dleft)-(self.left*dright))/(self.right*self.right)

def sym(exp):

    def tokenize(exp):
        exp=exp.strip() #removes whitespace from both ends of string
        if exp=='':
            return []
        elif exp[0] in '()':
            return [exp[0]]+tokenize(exp[1:])
        for ix,char in enumerate(exp):
            if char in ' ()':
                return [exp[:ix]]+tokenize(exp[ix:])
        return [exp]
    def try_int(x):
        try:
            return Num(int(x))
        except ValueError:
            return Var(x)
    opmap={'+':Add, '-':Sub, '*':Mul, '/':Div}
    def parse(tokens):
        def parse_expression(index):
            tok=tokens[index]
            if tok=='(':
                left,op_index=parse_expression(index+1)
                operator=tokens[op_index]
                assert operator in opmap
                right,end=parse_expression(op_index+1)
                assert tokens[end]==')'
                return opmap[operator](left,right), end+1
            return try_int(tok), index+1
        return parse_expression(0)[0]
    return parse(tokenize(exp))
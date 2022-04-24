"""6.009 Lab 8: carlae Interpreter Part 2"""
import sys
import doctest


class EvaluationError(Exception):
    """
    Exception to be raised if there is an error during evaluation other than a
    NameError.
    """
    pass

carlae_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': lambda args: mul(args),
    '/': lambda args: div(args),
    '=?': lambda args: equal(args),
    '>': lambda args: greater(args),
    '<': lambda args: smaller(args),
    '>=': lambda args: greaterorequal(args),
    '<=': lambda args: smallerorequal(args),
    'not': lambda args: notfunc(args),
    '#t': '#t',
    '#f': '#f',
    'car': lambda args: carfunc(args),
    'cdr': lambda args: cdrfunc(args),
    'cons': lambda args: consfunc(args),
    'list': lambda args: listfunc(args),
    'length': lambda args: lengthfunc(args),
    'nil': None,
    'elt-at-index': lambda args: listindex(args),
    'concat': lambda args: concatfunc(args),
    'map': lambda args: mapfunc(args),
    'filter': lambda args: filterfunc(args),
    'reduce': lambda args: reducefunc(args),
    'begin': lambda args: beginfunc(args),}

def REPL():
    newenv=Environment(builtins)
    source=input('> ')
    while source!='quit':
        tokens=tokenize(source)
        tree=parse(tokens)
        tot=evaluate(tree,newenv)
        print(tot)
        source=input('> ')

class Environment():
    def __init__(self,other):
        #dict that connects all var:val pairs in this environment
        self.dict={}
        #so that we can lookup in parent if var not defined in current environment
        self.parent=other
    def __getitem__(self,var):
        try:
            return self.dict[var]
        except KeyError:
            #recursively keeps looking at parent's environment
            try:
                return self.parent[var]
            except:
                raise NameError
    def __setitem__(self,var,val):
        self.dict[var]=val

builtins=Environment(None)
builtins.dict.update(carlae_builtins)
builtins.parent=None

class functions():
    #making of the function via lambda; func is one thing that 
    def __init__(self,environment,parameters,func):
        self.environment=environment
        self.parameters=parameters
        #func is the function itself e.g. (* x x)
        self.func=func

    #calling of the function via functionname(input)
    def __call__(self,input):
        if len(input)!=len(self.parameters):
            raise EvaluationError
        #makes new environment to call function variables in
        newenvironment=Environment(self.environment)
        for i in range(len(self.parameters)):
            newenvironment[self.parameters[i]]=input[i]
        return evaluate(self.func,newenvironment)

def tokenize(source):
    source=source.strip() #removes whitespace from both ends of string
    if source=='':
        return []
    #looks for linebreak, tokenizes everything after
    elif source[0] in ' ()\n':
        return [source[0]]+tokenize(source[1:])
    #ignores comment
    elif source[0] in ';':
        linebreak=source.find('\n')
        if linebreak==-1:
            return []
        else:
            return tokenize(source[linebreak+1:])
    else:
        for i,char in enumerate(source):
            if char in ' ()\n':
                return [source[:i]]+tokenize(source[i:])
    return [source]
    """for ix,char in enumerate(source):
        if char in ' ()':
            return [source[:ix]]+tokenize(source[ix:])
        else:
            currentlist.append(char)
    return str(currentlist"""
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a carlae
                      expression
    """

#finds index of the other side of a given parenthesis
def findparenthesis(tokens,index):
    if index==0:
        return len(tokens)-1
    depth=0
    for i in range(len(tokens[index:])):
        tok=tokens[i+index]
        if tok=='(':
            depth=depth+1
        elif tok==')':
            depth=depth-1
        if depth==0:
            return i+index
    raise SyntaxError('parenthesis not closed')

def parse(tokens):
    if len(tokens)>1 and tokens[0]!='(':
        raise SyntaxError('not starting with parenthesis')
    def parse_expression(index):
        tok=tokens[index]
        if tok!='(' and tok!=')':
            try:
                newtok=float(tok)
                if newtok==int(newtok):
                    return int(newtok),index+1
                else:
                    return newtok, index+1
            except:
                return tok, index+1
        elif tok in ')':
            raise SyntaxError('too many parenthesis')
        else:
            rightpar=findparenthesis(tokens,index)
            intok=[]
            index=index+1
            while index!=rightpar:
                value,next_index=parse_expression(index)
                intok.append(value)
                index=next_index
            return intok, rightpar+1
    return parse_expression(0)[0]
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """

#different helper functions to implement functions in carlae_builtins:
def mul(args):
    currentval=1
    for val in args:
        currentval=currentval*val
    return currentval
def div(args):
    if len(args)==0:
        raise Exception
    elif len(args)==1:
        return 1/args[0]
    currentval=args[0]
    for val in args[1:]:
        currentval=currentval/val
    return currentval
def equal(args):
    if len(args)==0:
        raise Exception
    currentval=args[0]
    currentstate='#t'
    for arg in args[1:]:
        if currentval!=arg:
            return '#f'
    return currentstate
def greater(args):
    if len(args)==0:
        raise Exception
    currentval=args[0]
    currentstate='#t'
    for arg in args[1:]:
        if currentval<=arg:
            return '#f'
        currentval=arg
    return currentstate
def smaller(args):
    if len(args)==0:
        raise Exception
    currentval=args[0]
    currentstate='#t'
    for arg in args[1:]:
        if currentval>=arg:
            return '#f'
        currentval=arg
    return currentstate
def greaterorequal(args):
    if len(args)==0:
        raise Exception
    currentval=args[0]
    currentstate='#t'
    for arg in args[1:]:
        if currentval<arg:
            return '#f'
        currentval=arg
    return currentstate
def smallerorequal(args):
    if len(args)==0:
        raise Exception
    currentval=args[0]
    currentstate='#t'
    for arg in args[1:]:
        if currentval>arg:
            return '#f'
        currentval=arg
    return currentstate
def notfunc(args):
    if len(args)!=1:
        raise EvaluationError
    expr=evaluate(args[0])
    if expr=='#t':
        return '#f'
    elif expr=='#f':
        return '#t'

#helper functions to look for unittruths/falses e.g. #t or #f in arguments
def anytrue(args):
    for arg in args:
        if arg=='#t':
            return '#t'
    return '#f'
def anyfalse(args):
    for arg in args:
        if arg=='#f':
            return '#f'
    return '#t'

#for making of lists:
class Pair():
    def __init__(self,pair):
        self.car=pair[0]
        self.cdr=pair[1]
    
#constructs the car and cdr pairs
def consfunc(args):
    return Pair(args)
def carfunc(pair):
    try:
        return pair[0].car
    except:
        raise EvaluationError
def cdrfunc(pair):
    try:
        return pair[0].cdr
    except:
        raise EvaluationError
def listfunc(args):
    if len(args)==0:
        #empty list is none (in builtins, 'nil':None)
        return None
    else:
        return consfunc((args[0],listfunc(args[1:])))
def lengthfunc(args):
    count=0
    if isinstance(args[0],Pair):
        count=1+lengthfunc([args[0].cdr])
    elif args[0]!=None:
        raise EvaluationError
    return count
def listindex(args):
    if isinstance(args[0],Pair):
        if args[1]==0:
            return args[0].car
        else:
            return listindex([args[0].cdr,args[1]-1])
    else:
        raise EvaluationError
def concatfunc(args):
    if args==[]:
        return None
    if isinstance(args[0],Pair) or args[0]==None:
        if args[0]==None:
            return concatfunc(args[1:])
        firstelement=args[0].car
        restoflist=args[0].cdr
        return Pair((firstelement,concatfunc([restoflist]+args[1:])))
    else:
        raise EvaluationError

def mapfunc(args):
    func=args[0]
    #checks if args is a list, if not:
    if isinstance(args[1],Pair)!=True:
        #even if not list, None is the base case so return None
        if args[1]==None:
            return None
        else:
            raise EvaluationError
    else:
        first=func([args[1].car])
        return concatfunc([Pair((first,None)),mapfunc([func,args[1].cdr])])
def filterfunc(args):
    func=args[0]
    if isinstance(args[1],Pair)!=True:
        if args[1]==None:
            return None
        else:
            raise EvaluationError
    else:
        #if first element meets condition, adds that+rest, if not just rest
        if func([args[1].car])=='#t':
            return concatfunc([Pair((args[1].car,None)),filterfunc([func,args[1].cdr])])
        else:
            return filterfunc([func,args[1].cdr])
def reducefunc(args):
    func=args[0]
    if isinstance(args[1],Pair)!=True:
        if args[1]==None:
            return args[2]
        else:
            raise EvaluationError
    else:
        first=args[1].car
        firstval=func([args[2],first])
        if args[1].cdr==None:
            return firstval
        else:
            return reducefunc([func,args[1].cdr,firstval])

def beginfunc(args):
    return args[-1]
def evaluate_file(filename,environment=None):
    f=open(filename,"r")
    filestuff=f.read()
    tokens=tokenize(filestuff)
    tree=parse(tokens)
    tot=evaluate(tree,environment)
    return tot

def evaluate(tree,environment=None):
    #if number returns number
    if environment==None:
        environment=Environment(builtins)
    if isinstance(tree,int) or isinstance(tree,float) or isinstance(tree,functions):
        return tree
    elif isinstance(tree,str):
        return environment[tree]
    elif tree=='#f' or tree=='#t' or tree=='nil':
        return carlae_builtins[tree]
    elif tree==[]:
        raise EvaluationError
    else:
        operator=tree[0]
        if operator=='define':
            #if tree[1] is a string, then variable so add to environment and return value
            if len(tree)!=3:
                raise EvaluationError
            if isinstance(tree[1],str):
                val=evaluate(tree[2],environment)
                environment[tree[1]]=val
                return val
            #if it's a function name:
            else:
                environment[tree[1][0]]=functions(environment,tree[1][1:],tree[2])
                return environment[tree[1][0]]
        if operator=='lambda':
            return functions(environment,tree[1],tree[2])
        if operator=='and':
            args=tree[1:]
            currentstate='#t'
            #only checks until one false bc if one is false total is false
            for arg in args:
                currentstate=evaluate(arg,environment)
                if currentstate=='#f':
                    return '#f'
            return currentstate
        if operator=='or':
            args=tree[1:]
            currentstate='#f'
            #only checks until one true bc if one is true total is true
            for arg in args:
                currentstate=evaluate(arg,environment)
                if currentstate=='#t':
                    return '#t'
            return currentstate
        if operator=='if':
            #if cond true false
            args=tree[1:]
            if len(args)!=3:
                raise EvaluationError
            cond=evaluate(args[0],environment)
            if cond=='#t':
                return evaluate(args[1],environment)
            elif cond=='#f':
                return evaluate(args[2],environment)
        if operator=='let':
            args=tree[1]
            newenv=Environment(environment)
            for i in range(len(args)):
                #defines each var to val in newenv
                minitree=['define', args[i][0], args[i][1]]
                evaluate(minitree,newenv)
            #evaluates body
            return evaluate(tree[2],newenv)
        if operator=='set!':
            args=tree[1:]
            foundenvi='notfound'
            value=evaluate(args[1],environment)
            tryenvironment=environment
            while foundenvi=='notfound':
                if tryenvironment==None:
                    raise NameError
                if args[0] in tryenvironment.dict.keys():
                    foundenvi=tryenvironment
                else:
                    tryenvironment=tryenvironment.parent
            tryenvironment[args[0]]=value
            return value
        if isinstance(operator,int) or isinstance(operator,float):
            raise EvaluationError
        operation=evaluate(operator,environment)
        #for every [] in the largest [] recursively calls evaluate
        stufftoadd=[]
        for branch in tree[1:]:
            stufftoadd.append(evaluate(branch,environment))
        return operation(stufftoadd)

def result_and_env(tree,environment=None):
    if environment==None:
        environment=Environment(builtins)
    return (evaluate(tree,environment),environment)     

if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()
    #print(parse(tokenize('(let ((x 1) (y 2) (z 3)) (+ x y z))')))
    for i in range(len(sys.argv)-1):
        evaluate_file(sys.argv[i+1],builtins)
    REPL()
    pass
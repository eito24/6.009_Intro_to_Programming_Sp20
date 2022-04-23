#!/usr/bin/env python3
"""6.009 Lab 7: carlae Interpreter"""

import doctest
# NO ADDITIONAL IMPORTS!

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
}

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
#making mul and div functions so that I can put in carlae_builtins
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


def evaluate(tree,environment=None):
    #if number returns number
    if environment==None:
        environment=Environment(builtins)
    if isinstance(tree,int) or isinstance(tree,float):
        return tree
    elif isinstance(tree,str):
        return environment[tree]
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
        
"""
    Evaluate the given syntax tree according to the rules of the carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """


if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()
    REPL()
    pass

# Postfix Calculator
# Uses Calculator class to convert input expression to postfix, and solve expression
# Uses AdvancedCalculator class to support expressions over multiple lines, as well as the use of variables

class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__

class Stack:
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        #if top is empty, return True, else return False
        if self.top == None:
            return True
        else:
            return False

    def __len__(self):
        #add to counter while there are remaining nodes, return counter at end
        current = self.top
        counter = 0
        while current is not None:
            current = current.next
            counter += 1
        return counter
        

    def push(self,value):
        temp = self.top                 #assign top to temp
        self.top = Node(value)          #then set top equal to Node of input value
        self.top.next = temp            #assign next Node to the temp

     
    def pop(self):
        if not self.isEmpty():
            temp = self.top             #assign current top Node to temp
            self.top = self.top.next    #replace current top Node with next Node
            return temp.value           #return value of Node that is removed using temp

    def peek(self):
        if self.top != None:            #if top is None, means Stack is empty, do not return anything
            return self.top.value


class Calculator:
    def __init__(self):
        self.__expr = None

    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        #try to typecast txt as float, return True if it works, False if it doesn't
        try:
            float(txt)
            return True
        except:
            return False

    def prec(self, ch):
        #helper method to define precedence of operators
        if ch == '+' or ch == '-':
            return 1
        elif ch == '*' or ch == '/':
            return 2
        elif ch == '^':
            return 3
        else:
            return 0

    def _getPostfix(self, txt):
        postfixStack = Stack()
        postfix = ''
        txt = txt.strip()
        txtsplt = txt.split()
        #list of numbers and period, which are acceptable in number/float strings
        numlst = ['0','1','2','3','4','5','6','7','8','9','.']
        #list containing all open parentheses
        openparlst = ['(','[','{','<']
        #list containing all close parentheses
        closeparlst = [')',']','}','>']
        last = ''
        for ch in txtsplt:
            if (not self._isNumber(ch) and ch not in '+-*/^()[]{}<>'):
                #if not a valid input character, return None
                return None
            if (last in '+-*/^' and ch in '+-*/^') or (self._isNumber(last) and self._isNumber(ch)):
                #if last item and current item are both operators or both operands, return None
                return None
            condition = False
            for ch2 in ch:
                if ch2 in numlst:
                    #if item is a number, set condition to True
                    condition = True
            if condition == True:
                #turn item into float for decimal form
                ch = float(ch)
                #then turn item back into string, now in decimal form
                ch = str(ch)
                postfix += ch + ' '
            elif ch in openparlst:
                if last not in '+-*/^([{<':
                    postfixStack.push('*')
                    #implied multiplication
                postfixStack.push(ch)
            elif ch == '^':
                postfixStack.push('^')
            elif ch in closeparlst:
                while not postfixStack.isEmpty() and postfixStack.top.value not in openparlst:
                    postfix += postfixStack.top.value + ' '
                    postfixStack.pop()
                #if parentheses do not match return None
                if ch == ')':
                    if postfixStack.peek() != '(':
                        return None
                if ch == ']':
                    if postfixStack.peek() != '[':
                        return None
                if ch == '}':
                    if postfixStack.peek() != '{':
                        return None    
                if ch == '>':
                    if postfixStack.peek() != '<':
                        return None
                postfixStack.pop()
            else:
                if postfixStack.top == None:
                    value = 0
                else:
                    value = postfixStack.top.value
                if self.prec(ch) > self.prec(value):
                    postfixStack.push(ch)
                else:
                    while not postfixStack.isEmpty() and self.prec(ch) <= self.prec(postfixStack.top.value):
                        postfix += postfixStack.top.value + ' '
                        postfixStack.pop()
                    postfixStack.push(ch)
            last = ch
        if last in '+-*/^':
            return None
        while not postfixStack.isEmpty():
            #empty stack after going through all items/characters
            if not postfixStack.peek() == "":
                postfix += postfixStack.top.value + ' '
            if postfixStack.peek() in openparlst:
                return None
            postfixStack.pop()
        #because spaces are added after each item added to postfix, return postfix minus last character
        return postfix[:-1] 



    @property
    def calculate(self):
        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None
        calcStack = Stack()
        expr = self._getPostfix(self.__expr)
        if expr == None:
            #if expression is None return None
            return None
        expr = expr.split(' ')
        for ch in expr:
            if self._isNumber(ch):
                calcStack.push(ch)
            else:
                #first value is top Node value
                first = float(calcStack.top.value)
                #second value is next Node value
                second = float(calcStack.top.next.value)
                #remove first and second from the Stack
                calcStack.pop()
                calcStack.pop()
                if ch == '+':
                    #addition order does not matter
                    calcStack.push(first+second)
                if ch == '-':
                    #subtraction must be second minus first
                    calcStack.push(second-first)
                if ch == '*':
                    #multiplication order does not matter
                    calcStack.push(first*second)
                if ch == '/':
                    #division must be second divided by first
                    calcStack.push(second/first)
                if ch == '^':
                    #exponent must be second to the power of the first
                    calcStack.push(second**first)
        #return new top value that was pushed by if statements     
        return calcStack.top.value

class AdvancedCalculator:
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        if not word == '' and word[0].isalpha() and word.isalnum():
            #if string is not empty, is all alphanumeric, and first character is alphabetical, return True         
            return True
        return False
       

    def _replaceVariables(self, expr):
        exprsplt = expr.split()
        expr2 = []
        for ch in exprsplt:
            if ch in self.states:
                expr2 += str(self.states[ch]) + ' '
            elif self._isVariable(ch):
                #if item not in self.states but is a variable, return None          
                return None
            else:
                #if not a variable, add it as is
                expr2 += ch + ' '               
        exprjoin = ''.join(expr2)
        #return exprjoin minus last character because space is added to end of every entry
        return exprjoin[:-1]            


    
    def calculateExpressions(self):
        self.states = {} 
        calcObj = Calculator()
        exprdict = {}
        #split self.expressions by semicolon (assumed that input lines are properly split by semicolons) 
        expr = self.expressions.split(';')        
        for line in expr:
            try:
                #split each line into variable (before =) and expression (after =)
                spltline = line.split('=')          
                variable = spltline[0].strip()
                expression = spltline[1].strip()
            except:
                #if normal split does not work, will be return
                spltline = line.split('return')     
                expression = spltline[1].strip()
                #variable is always return for return split
                variable = '_return_'               
            if not self._isVariable(variable) and variable != '_return_':
                #if "variable" is not a valid variable and is not _return_, return None       
                self.states = {}
                return None
            expression = self._replaceVariables(expression)
            if expression == None:
                #if expression None return None          
                self.states = {}
                return None
            calcObj.setExpr(expression)
            exprcalc = float(calcObj.calculate)
            if exprcalc == None:
                #if calculated expression None return None            
                self.states = {}
                return None
            if variable != '_return_':
                #if variable is not _return_, update self.states and add to dictionary with copy of self.states
                self.states[variable] = exprcalc
                exprdict[line] = self.states.copy()
            else:
                #if variable is _return_, add to dictionary with variable of '_return_' as key                           
                exprdict[variable] = exprcalc
        return exprdict
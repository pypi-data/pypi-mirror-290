def evaluate(expression, mode='return'):
    expression = expression.replace(" ", "")
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '/':
            values.append(left / right)
    
    def evaluate_expression(expression):
        operators = []
        values = []
        i = 0
        while i < len(expression):
            if expression[i].isdigit() or expression[i] == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                values.append(float(expression[i:j]))
                i = j
            elif expression[i] in precedence:
                while (operators and operators[-1] in precedence and
                       precedence[operators[-1]] >= precedence[expression[i]]):
                    apply_operator(operators, values)
                operators.append(expression[i])
                i += 1
            else:
                raise ValueError("Invalid character in expression")
        while operators:
            apply_operator(operators, values)
        return values[0]
    
    result = evaluate_expression(expression)
    
    if mode == 'print':
        print(result)
    elif mode == 'return':
        return result
    else:
        raise ValueError("Invalid mode. Choose 'print', 'return', or 'none'.")

def eval(expression, mode='return'):
    expression = expression.replace(" ", "")
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '/':
            values.append(left / right)
    
    def evaluate_expression(expression):
        operators = []
        values = []
        i = 0
        while i < len(expression):
            if expression[i].isdigit() or expression[i] == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                values.append(float(expression[i:j]))
                i = j
            elif expression[i] in precedence:
                while (operators and operators[-1] in precedence and
                       precedence[operators[-1]] >= precedence[expression[i]]):
                    apply_operator(operators, values)
                operators.append(expression[i])
                i += 1
            else:
                raise ValueError("Invalid character in expression")
        while operators:
            apply_operator(operators, values)
        return values[0]
    
    result = evaluate_expression(expression)
    
    if mode == 'print':
        print(result)
    elif mode == 'return':
        return result
    else:
        raise ValueError("Invalid mode. Choose 'print', 'return', or 'none'.")
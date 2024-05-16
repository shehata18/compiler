import re


TOKENS = [
    ("NUMBER", r"\d+"),
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),

    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MULTIPLY", r"\*"),
    ("DIVIDE", r"/"),

    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),

    ("ASSIGNMENT", r"="),
    ("WHITESPACE", r"\s+"),
    ("SEMICOLON", r";"),

]


def tokenize(src) -> list:
    tokens = []
    while src:
        for token_type, pattern in TOKENS:
            match = re.match(pattern, src)
            if match:
                token_value = match.group(0)
                if token_type != "WHITESPACE":
                    tokens.append((token_type, token_value))
                src = src[match.end() :]
                break
        else:
            raise Exception("Invalid character: " + src[0])
    return tokens

def print_tokens(tokens):
    print("{:<15}{}".format("Lexeme", "Token"))
    print("-" * 25)
    for token_type, token_value in tokens:
        print("{:<15}{}".format(token_value, token_type))

def parse_statement(tokens):
    if tokens[0][0] == 'IDENTIFIER' and tokens[1][0] == 'ASSIGNMENT':
        # Assignment statement
        identifier = tokens[0][1]
        expression, remaining_tokens = parse_expression(tokens[2:])
        if remaining_tokens[0][0] == 'SEMICOLON':
            return ['assignment_statement', identifier, expression], remaining_tokens[1:]
    elif tokens[0][0] == 'IDENTIFIER' or tokens[0][0] == 'NUMBER':
        # Expression statement
        expression, remaining_tokens = parse_expression(tokens)
        if remaining_tokens[0][0] == 'SEMICOLON':
            return ['expression_statement', expression], remaining_tokens[1:]
    return None, tokens

def parse_expression(tokens):
    term, remaining_tokens = parse_term(tokens)
    if remaining_tokens and remaining_tokens[0][0] in ["PLUS", "MINUS", "MULTIPLY", "DIVIDE"]:
        operator = remaining_tokens[0][1]
        next_term, remaining_tokens = parse_expression(remaining_tokens[1:])
        return ['expression', term, operator, next_term], remaining_tokens
    return term, remaining_tokens

def parse_term(tokens):
    if tokens[0][0] == 'NUMBER' or tokens[0][0] == 'IDENTIFIER':
        return tokens[0][1], tokens[1:]
    elif tokens[0][0] == 'LPAREN':
        expression, remaining_tokens = parse_expression(tokens[1:])
        if remaining_tokens[0][0] == 'RPAREN':
            return ['parenthesized_expression', expression], remaining_tokens[1:]
    return None, tokens

def parse(tokens):
    statements = []
    while tokens:
        statement, tokens = parse_statement(tokens)
        if statement:
            statements.append(statement)
    return statements


src = open("file.txt").read()
tokens = tokenize(src)
print_tokens(tokens)
print("-"*70)

parse_tree = parse(tokens)

print("Parse Tree: \n")
print(parse_tree)
print("-"*70)

# print("Symbol Table: \n")

# symbol_table = generate_symbol_table(parse_tree)
# symbol_table.display()

print('-'*70)

def unordered_symbol_table(statements):
    symbol_table = {}
    for statement in statements:
        if statement[0] == 'assignment_statement':
            identifier = statement[1]
            symbol_table[identifier] = evaluate_expression(statement[2], symbol_table)
    return symbol_table


def ordered_symbol_table(statements):
    symbol_table = {}
    ordered_table = []
    for statement in statements:
        if statement[0] == 'assignment_statement':
            identifier = statement[1]
            value = evaluate_expression(statement[2], symbol_table)
            symbol_table[identifier] = value
    for identifier, value in sorted(symbol_table.items()):
        ordered_table.append((identifier, value))
    return ordered_table


def evaluate_expression(expression, symbol_table):
    if isinstance(expression, str):
        if expression.isdigit():
            return int(expression)
        elif expression in symbol_table:
            return symbol_table[expression]
        else:
            return None
    if expression[0] == 'expression':
        left = evaluate_expression(expression[1], symbol_table)
        right = evaluate_expression(expression[3], symbol_table)
        operator = expression[2]
        if left is not None and right is not None:
            if operator == '+':
                return left + right
            elif operator == '-':
                return left - right
            elif operator == '*':
                return left * right
            elif operator == '/':
                return left / right if right != 0 else None
    elif expression[0] == 'parenthesized_expression':
        return evaluate_expression(expression[1], symbol_table)
    return None


# Parse the tokens
parsed_statements = parse(tokens)

# Create unordered symbol table
unordered_table = unordered_symbol_table(parsed_statements)
print("Unordered Symbol Table:")
print(unordered_table)

# Create ordered symbol table
ordered_table = ordered_symbol_table(parsed_statements)
print("\nOrdered Symbol Table:")
print(ordered_table)


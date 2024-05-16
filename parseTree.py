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


tokens = [
    ('IDENTIFIER', 'x'),
    ('ASSIGNMENT', '='),
    ('NUMBER', '10'),
    ('SEMICOLON', ';'),
    ('IDENTIFIER', 'y'),
    ('ASSIGNMENT', '='), 
    ('IDENTIFIER', 'x'),
    ('PLUS', '+'),
    ('NUMBER', '5'),
    ('SEMICOLON', ';'),
    ('IDENTIFIER', 'i'),
    ('ASSIGNMENT', '='),
    ('IDENTIFIER', 'y'),
    ('MINUS', '-'),
    ('IDENTIFIER', 'x'),
    ('MULTIPLY', '*'),
    ('NUMBER', '50'),
    ('DIVIDE', '/'), ('IDENTIFIER', 'x'),
    ('SEMICOLON', ';')
    ]
print(parse(tokens))
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
print('=> Unordered Symbol Table:')
print('-'*27)

class UnorderedSymbolTable:
    def __init__(self):
        self.table = {}

    def insert(self, symbol, symbol_type, declaration_line):
        self.table[symbol] = {'type': symbol_type, 'declaration_line': declaration_line, 'references': set()}

    def add_reference(self, symbol, line):
        self.table[symbol]['references'].add(line)

    def print_table(self):
        print("Counter  Variable Name     Type      Declaration Line    Line Reference")
        for counter, (symbol, info) in enumerate(self.table.items(), start=1):
            print(f"{counter:<9}{symbol:<20}{info['type']:<10}{info['declaration_line']:<20}{', '.join(map(str, info['references']))}")

# Create an instance of UnorderedSymbolTable
unordered_table = UnorderedSymbolTable()

# Parse tokens and insert identifiers into the symbol table
line_number = 1
for token_type, token_value in tokens:
    if token_type == 'IDENTIFIER':
        if token_value not in unordered_table.table:
            unordered_table.insert(token_value, 'integer', line_number)
        else:
            unordered_table.add_reference(token_value, line_number)
    elif token_type == 'SEMICOLON':
        line_number += 1

# Print the contents of the symbol table
unordered_table.print_table()

print('-'*70)
print('=> ordered Symbol Table:')
print('-'*27)

class OrderedSymbolTable:
    def __init__(self):
        self.table = []

    def insert(self, symbol, symbol_type, declaration_line):
        self.table.append({'symbol': symbol, 'type': symbol_type, 'declaration_line': declaration_line, 'references': set()})
        self.table.sort(key=lambda x: x['symbol'])

    def add_reference(self, symbol, line):
        for entry in self.table:
            if entry['symbol'] == symbol:
                entry['references'].add(line)

    def print_table(self):
        print("Counter  Variable Name     Type      Declaration Line    Line Reference")
        for counter, entry in enumerate(self.table, start=1):
            print(f"{counter:<9}{entry['symbol']:<20}{entry['type']:<10}{entry['declaration_line']:<20}{', '.join(map(str, entry['references']))}")

# Create an instance of OrderedSymbolTable
ordered_table = OrderedSymbolTable()

# Parse tokens and insert identifiers into the symbol table
line_number = 1
for token_type, token_value in tokens:
    if token_type == 'IDENTIFIER':
        if token_value not in [entry['symbol'] for entry in ordered_table.table]:
            ordered_table.insert(token_value, 'integer', line_number)
        else:
            ordered_table.add_reference(token_value, line_number)
    elif token_type == 'SEMICOLON':
        line_number += 1

# Print the contents of the symbol table
ordered_table.print_table()
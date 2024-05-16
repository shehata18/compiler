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

src = open("file.txt").read()
tokens = tokenize(src)
# print(tokens)
print_tokens(tokens)
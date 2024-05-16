def calculate_first(grammar):
    first = {nt: set() for nt in grammar}
    changed = True
    while changed:
        changed = False
        for nt in grammar:
            original = first[nt].copy()
            for production in grammar[nt]:
                for symbol in production:
                    if symbol in grammar:
                        first[nt].update(first[symbol] - {''})
                        if '' not in first[symbol]:
                            break
                    else:
                        first[nt].add(symbol)
                        break
                else:
                    first[nt].add('')
            if original != first[nt]:
                changed = True
    return first

def calculate_follow(grammar, start_symbol):
    first = calculate_first(grammar)
    follow = {nt: set() for nt in grammar}
    follow[start_symbol].add('$')
    changed = True
    while changed:
        changed = False
        for nt in grammar:
            for production in grammar[nt]:
                trail = set(follow[nt])
                for symbol in reversed(production):
                    if symbol in grammar:
                        if trail != follow[symbol]:
                            before_update = len(follow[symbol])
                            follow[symbol].update(trail)
                            if len(follow[symbol]) > before_update:
                                changed = True
                        if '' in first[symbol]:
                            trail.update(first[symbol] - {''})
                        else:
                            trail = first[symbol]
                    else:
                        trail = {symbol}  # Reset trail to just the terminal symbol
    return follow

grammar = {
    'S': [['A', 'B', 'C']],
    'A': [['a', 'A'], ['']],
    'B': [['b', 'B'], ['']],
    'C': [['c', 'C'], ['']]
}

first_sets = calculate_first(grammar)
follow_sets = calculate_follow(grammar, 'S')

print("FIRST Sets:")
for non_terminal, first_set in first_sets.items():
    print(non_terminal, "->", first_set)

print("\nFOLLOW Sets:")
for non_terminal, follow_set in follow_sets.items():
    print(non_terminal, "->", follow_set)



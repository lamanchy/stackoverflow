from rules import get_rules
from values import values


def get_result(rule, value):
    try:
        return int(rule(value))
    except ZeroDivisionError:
        return 'zd'


def view_results():
    print('r', end='\t')
    for value in values:
        print(value, end='\t')
    print()

    for i, rule in enumerate(get_rules()):
        print(i, end='\t')
        for value in values:
            print(get_result(rule, value), end='\t')
        print()







view_results()









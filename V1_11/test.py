from ast import literal_eval
a = 3
x = 0
#try:
x = input('input x: ')
if 'e' in x:
    x = literal_eval(x)
    print(x)

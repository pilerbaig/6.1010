def flatten_tuple(x):
    if not x:
        return x
    if type(x[0]) != tuple:
        return (x[0],) + flatten_tuple(x[1:])
    else:
        return flatten_tuple(x[0]) + flatten_tuple(x[1:])


x = (1, (2, 3), (4,), (5, 6, 7))
print(flatten_tuple(x))

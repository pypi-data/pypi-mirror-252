def f(**kwargs):
    kwargs['a'] = 7


d = {'b': 4}

f(**d)

print(d)

class C:
    d = {}

    def __init__(self):
        self.d = {'a': 1}


print(C.d)
c = C()
print(C.d)

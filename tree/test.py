

def children():
    for x in range(10):
        yield x
        print(chr(x + ord("A")))
    print("wfgoiiuwbehoi gu ")


for child in children():
    print(child)
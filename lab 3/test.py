import itertools

x = itertools.combinations('abcde', 2)
for i in x:
    print(''.join(i))
print('extra') 

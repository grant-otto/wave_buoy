import numpy as np

tup=(1,2,3,4,5,6,7)
if len(tup) % 2 != 0:
    lis=list(tup)
    del lis[-1]
    tup=tuple(lis)
print(tup)
tup=np.array(tup)
multtest=5*tup
print(multtest)
tup=tuple(multtest)
print(tup)
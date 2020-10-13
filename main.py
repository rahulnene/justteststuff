from time import perf_counter
# from primefactors import factorize
from math import sqrt, factorial, log10, floor

t0 = perf_counter()

def checkBounce(n):
    nStr = str(n)
    nList = []
    for digit in nStr:
        nList.append(int(digit))
    nsorted = sorted(nList)
    if nList == nsorted or nList == nsorted[::-1]:
        return False
    return True


ans = 0
for i in range(1,10000000000):
    bouncy = checkBounce(i)
    if not bouncy:
        ans += 1

print(ans)

# print(checkBounce(132))

tf = perf_counter() - t0
print(tf, "seconds")

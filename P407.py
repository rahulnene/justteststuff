from time import perf_counter
from math import sqrt
from primefactors import factorize

t0 = perf_counter()

lim = 10 ** 3

out = 0


def check(n):
    nCache = 1
    if nCache == n - 1:
        return n - 1
    else:
        for i in range(n - 2, -1, -1):
            temp = nCache
            temp -= (2 * i + 1)
            temp %= n
            nCache = temp
            # print(i,temp)
            if temp == i:
                return i


def check2(n):
    nCache = 1
    for i in range(0, int(n - sqrt(n))):
        temp = nCache
        temp += (2 * i - 1)
        temp %= n
        nCache = temp
        # print(n-i,temp)
        if temp == n - i:
            return n - i
    return 1




def check3(n):
    # factors = factorize(n)
    p = max(factorize(n))
    # print(n,p)
    x = n - p
    while x > sqrt(n) - 1:
        if x % p == 0:
            if pow(x, 2, n) == x:
                # print(x,n)
                return x
        if (x + 1) % p == 0:
            if pow(x + 1, 2, n) == x:
                # print(x+1,n)
                return x + 1
        x -= p
    return 1


print(check3(6))
exp = 3
out = -1
# for i in range(10 ** exp, 0, -1):
#     temp = check3(i)
#     # print(i, temp)
#     out += temp

print(out)

tf = perf_counter()
print(tf - t0, "seconds")

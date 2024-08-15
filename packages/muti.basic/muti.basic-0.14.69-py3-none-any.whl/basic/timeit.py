import timeit


Q=lambda x,t=1024:timeit.timeit(x, number=t)
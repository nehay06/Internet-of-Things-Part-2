import time
from multiprocessing.pool import ThreadPool

ctr = 0

#
# def foo():
#     itr = 0
#     while(itr < 10):
#         time.sleep(2)
#         print "iter: ", itr
#         itr += 1
#         if (bar() == True):
#             print "True Bar"
#             break
#
#
# def bar():
#     global ctr
#     if (ctr != 5):
#         return False
#     return True
#
#
# pool = ThreadPool(processes=1)
#
# async_result = pool.apply_async(foo) # tuple of args for foo
#
# # do some other stuff in the main process
# print "Hi My name is Ayush\n"
# time.sleep(5)
# global ctr
# ctr = 5
#
# return_val = async_result.get()  # get the return value from your function.
# print return_val

def ret():
    return True

re = ret()

print "done"
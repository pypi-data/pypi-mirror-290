import ctypes
import os
 
class CTH_OBJ():
    ptr = 0
    current_path = os.getcwd()

    fib = ctypes.cdll.LoadLibrary("%s/simple.so"%current_path)
    def __init__(self, modelname):
        model = ctypes.c_char_p()
        model.value = modelname.encode ('utf-8')
        self.fib.initmodel.restype = ctypes.POINTER(ctypes.c_int)
        self.ptr = self.fib.initmodel(model)
    def get_rest_str(self, strs, rate, k):
        strcs = []
        for str in strs:
            strc = ctypes.c_char_p()
            strc.value = str.encode('utf-8')
            strcs.append(strc)
        self.fib.getnums.restype = ctypes.POINTER(ctypes.c_int)
        my_strs = (ctypes.c_char_p * len(strcs))(*strcs)
        nums = self.fib.getnums(my_strs, len(strcs), self.ptr, ctypes.c_float(rate), k)
        sum = nums[0]
        ans = [nums[i + 1] for i in range(sum)]
        return ans
    def is_similar_str(self, str, rate, k):
        self.fib.is_similar_str.restype = ctypes.c_bool
        input = ctypes.c_char_p()
        input.value = str.encode('utf-8')
        ans = self.fib.is_similar_str(input, self.ptr, ctypes.c_float(rate), k)
        return ans

#fib = ctypes.cdll.LoadLibrary("./simple.so")
#def initmodel():
    
#stri = ctypes.c_char_p()

#stri.value = b'as a relabel config to the corresponding scrape config. As per the regex value, only pods with "kvrocks" in their name will be relabelled as such.'
#strs = []
#for i in range(20):
#    strs.append(stri)
#my_strs = (ctypes.c_char_p * len(strs))(*strs)
#fib.getnums.restype = ctypes.POINTER(ctypes.c_int)
#model = ctypes.c_char_p()
#model.value = b"gpt-4"
#fib.initmodel.restype = ctypes.POINTER(ctypes.c_int)
#ptr = fib.initmodel(model)
#print(ptr)   
#nums = fib.getnums(my_strs, 20, ptr)
#len = nums[0]
#ans = [nums[i + 1] for i in range(len)]
#print(ans)

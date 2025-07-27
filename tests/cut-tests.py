#!/bin/python3

import fops as fo

test0 = """first,last,number
Braden,Carlson,2
Brynnli,Carlson,2
Arlee,Carlson,4
Troy,Rice,5
Hannah,Rice,4"""


print(fo.cut(test0,f="1-2"))
print(fo.cut(test0,f="2-3"))
print(fo.cut(test0,f="1,3"))
print(fo.cut(test0,f="1,4"))

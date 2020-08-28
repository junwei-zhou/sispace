# import os,re

# #所在目录
# path = 'C:/Users/junwei_zhou/Desktop/string-data'

# file_names = os.listdir(path)
# count = 0
# for name in file_names:
# 	count +=1
# 	res = str(count)+".png"
# 	os.rename(os.path.join(path,name),os.path.join(path,res))

a="i am you"
a=a[::-1]
print(a)
a=a.split(" ")
print(a)
a.reverse()
print(a)

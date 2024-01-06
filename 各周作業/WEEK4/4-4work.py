#錯誤版
'''
i = 0
while (i < 5):
    print(i)
    print("hi")
    continue
    i = i + 1
    print("You can't see me.")
'''

#正確版
i = 0
while (i < 5):
    print(i)
    print("hi")
    i = i + 1
    continue
    print("You can't see me.")
x = int(input("x = "))
y = int(input("y = "))
if x > 0 and y > 0:
    print("一")

if x < 0 and y > 0:
    print("二")

if x < 0 and y < 0:
    print("三")

if x > 0 and y < 0:
    print("四")

if x == 0 or y == 0:
    print("不要判斷")
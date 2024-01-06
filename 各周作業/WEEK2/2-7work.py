x = float(input("時針"))
y = float(input("分針"))
a = (360/60) * y #分針角度
b = (360/12) * x + 10.5
print(b - a)
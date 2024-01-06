x = 1
summ = float()
while x <= 5:
    print("科目分數",x,'= ',end='')
    y = float(input())
    summ = summ + y
    x = x + 1
print("平均 = ", summ / 5)
"""
有一分数序列：2/1，3/2，5/3，8/5，13/8，21/13…求出这个数列的前20项之和。
"""
a_1 = 1
a_2 = 1
a_3 = a_1+a_2
a_4 = 0
sum = 0
for i in range(20):
    sum +=a_3/a_2
    a_4 = a_3+a_2
    a_2 = a_3
    a_3 = a_4
print(sum)






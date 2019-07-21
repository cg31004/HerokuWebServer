def test(x,y):
    for i in range(x):
        for j in range(y):
            a = i*10 + j

            if a == 5:
                pass
            if a == 11:
                continue
            if a == 20:
                break
            print(a)
    return 0


print(test(3,9))
print('end')

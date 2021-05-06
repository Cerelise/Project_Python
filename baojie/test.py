l = list(range(5))
l1 = list(range(6,11))

l5 = []
l4 = zip(l,l1)
for i,j in l4:
    l5.append([i,j])
    print(l5[i])

l2 = []
for i in range(len(l)):
    l3 = tuple([l[i],l1[i]])
    l2.append(l3)
print(l2)






people=[(1,2),(1,0),(2,1),(3,2)]
output = []
for p in people:

    output.insert(p[1], p)
    print(p[1])
    print(output)
print(output)
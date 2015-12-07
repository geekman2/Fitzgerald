# -------------------------------------------------------------------------------
# Name:        ''
# Purpose:
# author =     'Geekman2'
# Created:     '10/29/2015'
# -------------------------------------------------------------------------------
ls1 = ["abc","123"]
ls2 = [1,2]
ls3 =[]
for i in ls1:
    for it in ls2:
        if i in ls3:
            break
        else:
            for x in ls1:
                ls3.append(x)

print ls3

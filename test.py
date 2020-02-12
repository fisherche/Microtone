

E = [0]
A = [480]
D = [960]
G = [240]
B = [720]
e = [1200]
all = [E,A,D,G,B,e]
for ea in all:
    for i in range(1,12):
        ea += [(ea[0]+(i*100))%1200]

print(all)


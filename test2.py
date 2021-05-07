a = {"naman":1,"manish":2}
a["naman"]+=2
try:
    a["abdul"]+=11
except KeyError:
    a["abdul"]=5
print(a)
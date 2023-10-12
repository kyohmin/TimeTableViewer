a = {}
a.update({"A":"C"})
a.update({"A":"D"})
a.update({"C":"D"})


if "D" in a:
    print("exist")
else:
    print("NO")

print(a)
# def func(**kwargs):
#     kwargs = kwargs or {x: x for x in range(10)}
#     print(kwargs)


# func()

x = {"x": {1: 2}, "y": {2: 3}}
y = x.copy()
print("x: ", x)
print("y: ", y)
del y["x"]
print("del in y")
print("x: ", x)
print("y: ", y)
del x["y"]
print("del in x")
print("x: ", x)
print("y: ", y)

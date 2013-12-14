

def clamp(x,a,b):
    if a > b:
        a,b = b,a
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return x

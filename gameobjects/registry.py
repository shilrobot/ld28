goRegistry = {}

def register(name):
    exec ("from gameobjects.%s import %s as GOCLASS" % (name.lower(), name))
    goRegistry[name.lower()] = GOCLASS

goTypes = [
    'Button',
    'ButtonMount',
    'Oak',
    'Player',
    'Willow'
]

for goType in goTypes:
    register(goType)

__all__ = ['goRegistry']
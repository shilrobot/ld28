goRegistry = {}

def register(name):
    exec ("from gameobjects.%s import %s as GOCLASS" % (name.lower(), name))
    goRegistry[name.lower()] = GOCLASS
    #print name.lower(), GOCLASS

goTypes = [
    'Button',
    'ButtonMount',
    'Oak',
    'Player',
    'Willow',
    'Door',
    'BustedDoor',
    'Bridge'
]

for goType in goTypes:
    #print 'Registering %s' % goType
    register(goType)

__all__ = ['goRegistry']
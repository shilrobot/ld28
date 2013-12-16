from gameobjects.button import Button
from gameobjects.buttonmount import ButtonMount
from gameobjects.oak import Oak
from gameobjects.player import Player
from gameobjects.willow import Willow
from gameobjects.door import Door
from gameobjects.busteddoor import BustedDoor
from gameobjects.bridge import Bridge

goRegistry = {
    'button':Button,
    'buttonmount':ButtonMount,
    'oak':Oak,
    'player':Player,
    'willow':Willow,
    'door':Door,
    'busteddoor':BustedDoor,
    'bridge':Bridge,    
}

__all__ = ['goRegistry']
from enum import Enum


class entityTypes(Enum):
    SHOT = 0
    ASSET = 1


def create_entity(entity_type):
    print('Creating entity')
    if not type(entity_type) == entityTypes:
        raise TypeError('Entity is of wrong type.')


def remove_entity():
    print('Removing entity')
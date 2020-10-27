import json

# This global dictionary stores the name of the room as the key and the dictionary describing the room as the value.
ROOMS = {}

def create_room(name, description):
    assert (name not in ROOMS)
    room = {
        'name': name,
        'description': description,
        'exits': [],
        'ends_game': False,
    }
    ROOMS[name] = room
    return room

def create_exit(source, destination, description):
    exit = {
        'destination': destination,
        'description': description
    }
    ROOMS[source]['exits'].append(exit)
    return exit
    
create_room("START", """You are in the grand entrance hall of a large building.
The front door appears to be locked...
How did you get here?""")
create_exit("START", "basement", "There are stairs leading down.")
create_exit("START", "attic", "There are stairs leading up.")
create_exit("START", "kitchen", "There is a red door.")

create_room("basement", """You have found the basement of the mansion.
It is darker down here.
You get the sense a secret is nearby, but you only see the stairs you came from.""")
create_exit("basement", "START", "There are stairs leading up.")

create_room("attic", """Something rustles in the rafters as you enter the attic. Creepy.
It's big and dark up here.""")
create_exit("attic", "START", "There are stairs leading down.")
create_exit("attic", "attic2", "There is an archway.")

create_room("attic2", """There's definitely a bat in here somewhere.
This part of the attic is brighter, so maybe you're safe here.""")
create_exit("attic2", "attic", "There is an archway.")
create_exit("attic2", "balcony", "A small door rattles in the wind.")
create_exit("attic2", "dumbwaiter", "There is a dumbwaiter near the chimney.")

create_room("balcony", """There's a strange light here on the balcony.""")
create_exit("balcony", "aliens", "Step into the light.")

aliens = create_room("aliens", """The aliens take you aboard their spaceship.
...
I guess you escaped.""")
aliens['ends_game'] = True

create_room("kitchen", """You've found the kitchen. You smell moldy food and some kind of animal.""")
create_exit("kitchen", "entranceHall", "There is a red door.")
create_exit("kitchen", "dumbwaiter", "There is a dumbwaiter.")

create_room("dumbwaiter", """You crawl into the dumbwaiter. What are you doing?""")
create_exit("dumbwaiter", "attic2", "Exit at the top.")
create_exit("dumbwaiter", "kitchen", "Exit on the first-floor.")
create_exit("dumbwaiter", "secretRoom", "Exit at the bottom.")

create_room("secretRoom", """You have found the secret room.
Who thought a green rug was a good idea?""")
create_exit("secretRoom", "hallway0", "A long hallway leads away.")
create_exit("secretRoom", "basement", "A trapdoor opens downward. You could hop down...?")
create_exit("secretRoom", "dumbwaiter", "Get back in the dumbwaiter.")

crypt = create_room("crypt", """You've found your way into a crypt. You smell dirt.""")
create_exit("crypt", "outside", "There are stairs leading up.")
outside = create_room("outside", """You step out into the night.

It smells like freedom.
""")
outside["ends_game"] = True

hallway_length = 3
for i in range(hallway_length):
    here = "hallway{}".format(i)
    forward = "hallway{}".format(i+1)
    backward = "hallway{}".format(i-1)
    if i == 0:
        backward = "secretRoom"
    elif i == hallway_length - 1:
        forward = "crypt"
    create_room(here, """This is a very long hallway.""")
    create_exit(here, backward, """Go back.""")
    create_exit(here, forward, """Go forward.""")

##
# Save our text-adventure to a file:
##
with open('spooky_mansion.json', 'w') as out:
    json.dump(ROOMS, out, indent=2)


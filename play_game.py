import json
import os
import random
import time
start_time = time.time()

black_cat = {
    'name': '',
    }

def find_non_win_rooms(game):
    keep = []
    for room_name in game.keys():
        # skip if it is the "fake" metadata room that has title & start
        if room_name == '__metadata__':
            continue
        # skip if it ends the game
        if game[room_name].get('ends_game', False):
            continue
        # keep everything else:
        keep.append(room_name)
    return keep

def main():
    # TODO: allow them to choose from multiple JSON files?
    path = os.getcwd()
    dir_list = os.listdir(path)
    jsons = []
    for file in dir_list:
        if file.endswith(".json"):
            jsons.append(file)
    print("Choose a game.")
    print("")
    for j in jsons:
        #print(jsons.index(j)+1, ".", j)
        print("{}. {}".format(jsons.index(j)+1, j))

    option = input("> ").lower().strip()
    try:
        num = int(option) -1 
        selected_game = jsons[num]
        print("...")
        print(selected_game)

    except:
         print("I don't understand '{}'...".format(action))

    with open(selected_game) as fp:
        game = json.load(fp)
    print_instructions()
    
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)


def play(game):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = game['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...', 'Cat treat']
    visited = {}

    room_list = find_non_win_rooms(game)
    black_cat["name"] = random.choice(room_list) 
    
    while True:
        print("")

        # Figure out what room we're in -- current_place is a name.
        here = game[current_place]
        # Print the description.
        print(here["description"])
        
        # Cat
        if black_cat["name"] == here["name"]:
            print("!!! There is a cat here !!!")
            if "Cat treat" not in stuff:
                cat_exit = random.choice(here["exits"])
                black_cat["name"] = cat_exit["destination"]
        

        # Keep track of location
        if current_place in visited:
            print("... You've been in this room before.")
        visited[current_place] = True
        
        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.
        if here["items"] != []:
            for i in here["items"]:
                print("!!! There is a", i, "that you can take!!!")
                continue
        
        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here)

        
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()
        print("you typed:" , action)

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        
        # Print instructions
        if action == "help":
            print_instructions()
            continue
        

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        if action == "stuff":
            if len(stuff) != 0:
                print("... You have: ", stuff)
            else:
                print("... You have nothing.")
            continue
            
        # TODO: if they type "take", grab any items in the room.
        if action == "take":
            if here["items"] != []:
                for i in here["items"]:
                    stuff.append(i)
                    print("You grabbed the", i)
                    here["items"] = []
            else:
                print("... There is nothing to take here.")
            continue
        
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        if action in ["search", "find"]:
            x = find_hidden_exits(here)
            find_usable_exits(here)
            if x == True:
                print("You discovered a secret room.")
            else:
                print("There are no secret rooms here.")
            continue
          
        # Drop
        if action == "drop":
            if len(stuff) != 0:
                print("... Choose the item you want to drop ... or type 99 to go back to the room")
                for item in stuff:
                    print("{}. {}".format(stuff.index(item)+1, item))
                while True:
                    try:
                        x = int(input("> "))
                        if x == 99: 
                            break
                        elif x <= len(stuff):
                            print(len(stuff))
                            here["items"].append(stuff[x-1])
                            stuff.pop(x-1)
                            break
                        else:
                            print(x, "is not in the range.")
                    except:
                        print("Enter an integer")
                    
            else:
                print("You have nothing to drop.")
            continue
        
         # Find the cat
        if action == "where is the cat":
            print("The cat is in", black_cat["name"])
            continue
            
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            if selected.get("required_key") != None and "Mansion Key" not in stuff:
                print("You try to open the door, but it's locked!")
            else:
                current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    # Time
    time_spent = time.time() - start_time
    minutes = int(time_spent/60)
    seconds = time_spent - (minutes * 60)
    if minutes == 0:
        print("You were trapped in the game for", round(seconds), "seconds")
    elif minutea == 1:
        print("You were trapped in the game for", minutes, "minute", round(seconds), "seconds")
    elif minutes > 1:
        print("You were trapped in the game for", minutes, "minutes", round(seconds), "seconds")
    print("=== GAME OVER ===")

def find_usable_exits(room):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS 
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        usable.append(exit)
    return usable

def find_hidden_exits(room):
    found = False
    for exit in room['exits']:
        if exit.get("hidden", False) == True:
            found = True
            exit["hidden"] = False
    return found
            
            

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'help' to view the instructions.")
    print(" - Type 'drop' to drop your stuff here.")
    print(" - Type 'where is the cat' to find the location of the cat.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()

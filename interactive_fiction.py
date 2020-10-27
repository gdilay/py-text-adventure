import json

def main():
    games = [
        "spooky_mansion.json"
    ]
    index = choose_from_list("Which game do you want to play?", games)
    if index < 0:
        print("Ok, bye!")
        return
    with open(games[index]) as fp:
        rooms = json.load(fp)
    play(rooms)

def choose_from_list(qtext, opts):
    print(qtext)
    # the (+4) challenge here is the available list.
    available = []
    # I did show enumerate on the quiz, which might be better.
    for i in range(len(opts)):
        num = str(i+1)
        available.append(num)
        print("  ", num, ". ", opts[i], sep="")
    # slightly more clever than they achieve:
    return available.index(input("> "))
    # OK for the 8 points
    return int(input("> ")) + 1 

def play(rooms):
    current_place = 'START'

    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])
        # Is this a game-over?
        if 'ends_game' in here and here["ends_game"] == True:
            break

        # Allow the user to choose an exit:
        exits = here['exits']
        for i, exit in enumerate(exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = exits[num]
            current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")

if __name__ == '__main__':
    main()
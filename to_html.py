import os
import json

game = 'spooky_mansion'
with open(game+".json") as fp:
    rooms = json.load(fp)
#os.makedirs(game)

for name in rooms:
    room = rooms[name]
    with open(os.path.join(game, name+".html"), 'w') as out:
        print("<html>", file=out)
        print("<head><title>Spooky Mansion</title></head>", file=out)
        print("<body>", file=out)
        for line in room["description"].splitlines():
            print("<p>{}</p>".format(line), file=out)
        print("<ul>", file=out)
        for exit in room["exits"]:
            print('<li><a href="{}.html">{}</a></li>'.format(exit['destination'], exit['description']), file=out)
        print("</ul>", file=out)
        print("</body>", file=out)
        print("</html>", file=out)
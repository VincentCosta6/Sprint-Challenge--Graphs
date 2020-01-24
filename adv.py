from room import Room
from player import Player
from world import World

from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

visited_rooms = set()
player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

######
# UNCOMMENT TO WALK AROUND
######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")


graph = {}

def bfs(current_room, next_room):
    visited = {}

    q = Queue()
    q.enqueue( [current_room] )

    while next_room not in visited:
        path = q.dequeue()
        current_room = path[-1]

        if current_room not in visited:
            visited[current_room] = path

            for direction in graph[current_room]:
                if graph[current_room][direction] != '?':
                    new_path = path.copy()
                    new_path.append(graph[current_room][direction])

                    q.enqueue(new_path)


    return visited[next_room]
    
def reverse(direction):
    if direction is 'n':
        return 's'
    elif direction is 's':
        return 'n'
    elif direction is 'e':
        return 'w'
    elif direction is 'w':
        return 'e'

def traverse_maze():
    directions = ['n', 's', 'e', 'w']
    final_path = []

    unvisited = Stack()
    last_room = (0,'direction')

    while True:

        # if current room isnt in the graph, put it in with '?' and connect the previous room to this one and vice versa
        # else the current room is already in, set the last rooms direction towards the current room to the current room
        if player.current_room.id not in graph:
            graph[player.current_room.id] = {}
            for direction in player.current_room.get_exits():
                if direction == last_room[1]:
                    graph[last_room[0]][reverse(last_room[1])] = player.current_room.id
                    graph[player.current_room.id][direction] = last_room[0]
                else:
                    graph[player.current_room.id][direction] = '?'
        else:
            graph[last_room[0]][reverse(last_room[1])] = player.current_room.id
            graph[player.current_room.id][last_room[1]] = last_room[0]

        # if the room hasnt been visited yet, add all of its directions that have a '?' to the stack
        if player.current_room not in visited_rooms:
            # shuffle n,s,e,w to randomize the path
            random.shuffle(directions)
            for direc in directions:
                if direc in graph[player.current_room.id] and graph[player.current_room.id][direc] == '?':
                    unvisited.push( (player.current_room.id, direc) )

        visited_rooms.add(player.current_room)
        next_room = unvisited.pop()

        # stack was empty, return final path
        if next_room is None:
            return final_path

        last_room = (player.current_room.id, reverse(next_room[1]))

        # if were in the next room just travel there
        # else do a bfs to find a path to the next '?', and convert all rooms to directions and travel at the same time
        if player.current_room.id == next_room[0]:
            player.travel(next_room[1])
            final_path.append(next_room[1])
        else:
            path_to_next = bfs(player.current_room.id, next_room[0])[1:]
            
            for room in path_to_next:
                for direc in directions:
                    if direc in graph[player.current_room.id] and graph[player.current_room.id][direc] == room:
                        last_room = (player.current_room.id, reverse(direc))

                        player.travel(direc)
                        final_path.append(direc)
                
            unvisited.push(next_room)

        if len(visited_rooms) == len(room_graph):
            return final_path


mini = 2000

while True:
    graph = {}
    visited_rooms = set()

    traversal_path = traverse_maze()

    if len(traversal_path) < mini:
        mini = len(traversal_path)
        print(mini)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
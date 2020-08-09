from pathlib import Path
from json import dump, load
from time import time
from sys import argv, exit
from os import path

from Vertex import Vertex
""" Class represented with adjacency list which have required methods for creating graph
and modified bfs and dfs for finding all shortest paths
 """
from Graph import Graph

# input value is list of lists where each list is shortest path from source to destination vertex
# output result is array of dictonary with key "points" and value of list where each element is new dictionary
# which represent one cell on the shortest route from source to destination


def generate_dict_shortest_paths(shortest_paths):
    dict_shortest_paths = []
    for shortest_path in shortest_paths:
        dict_shortest_path = {}
        dict_shortest_path['points'] = []
        for vertex in shortest_path:
            dict_shortest_path['points'].append({
                'row': vertex.vertex[0],
                # convert back column number to column letter
                'col': chr(vertex.vertex[1]+64)
            })
        dict_shortest_paths.append(dict_shortest_path)
    return dict_shortest_paths

# generate dictionary with all shortest routes and execution time in ms


def generate_task_solution_file_content(shortest_paths, start_time):
    task_solution_file_content = {}
    # diff between current time on the end of execution and time on start of program execution
    # time() return value in seconds
    task_solution_file_content["execution_time_in_ms"] = ((time() - start_time) * 1000)
    task_solution_file_content['paths'] = shortest_paths
    return task_solution_file_content


def parse_map_description_lines(lines):
    # checks for validation of open and closed tag in file
    if lines[0] != "<map>\n":
        raise ValueError("Map description file must start with open tag <map>")
    if lines[-1] != "</map>\n" and lines[-1] != "</map>":
        raise ValueError("Map description file must end with close tag </map>")

    # passing cell lines to new function for parsing and if everything is okay retrieving generated adjacency list
    adjacency_list = parse_input_cells(lines)

    # passing start point line for parsing
    start_point_line = lines[-3].split()
    start_point_row_number, start_point_col_number = parse_point(start_point_line, "start-point")
    # passing end point line for parsing
    end_point_line = lines[-2].split()
    end_point_row_number, end_point_col_number = parse_point(end_point_line, "end-point")

    # generating source and destination vertex from start and end points
    source = Vertex(start_point_row_number, start_point_col_number)
    if not source in adjacency_list.adjacency_list:
        raise ValueError(f"Map description file doesn't contain start point ({start_point_row_number},{chr(start_point_col_number+64)})")
    destination = Vertex(end_point_row_number, end_point_col_number)
    if not destination in adjacency_list.adjacency_list:
        raise ValueError(f"Map description file doesn't contain end point ({end_point_row_number},{chr(end_point_col_number+64)})")
    return adjacency_list, source, destination


def parse_input_cells(lines):
    # adjacency list initialization
    adjacency_list = Graph()
    # validation also checks for valid intend with four spaces
    if lines[1] != "    <cells>\n":
        raise ValueError("Cells in map description file must start with open tag <cells>")
    if lines[-4] != '    </cells>\t\n' and lines[-4] != '    </cells>\n':
        raise ValueError("Cells in map description file must end with close tag </cells>")
    # passing lines which starts with <cell to other function and return values inserting into adjacency list
    for cell in lines[2:-4]:
        splitted_cell = cell.split()
        row_number, col_number = parse_cell(splitted_cell)
        adjacency_list.add_vertex(row_number, col_number)
        adjacency_list.check_for_adding_edges(row_number, col_number)
    return adjacency_list

# function parses all lines that start with <cell tag


def parse_cell(splitted_cell):
    if splitted_cell[0] != '<cell':
        raise ValueError('Inside cells each cell must start with open tag <cell, example of valid cell : <cell row="1" col= "A" />')
    if splitted_cell[2] != 'col=':
        raise ValueError('Inside cells second argument for each cell must be col=, example of valid cell : <cell row="1" col= "A" />')
    if splitted_cell[4] != '/>':
        raise ValueError('Inside cells every cell must end with close tag />, example of valid cell : <cell row="1" col= "A" />')
    # columng letter is upper letter
    if not splitted_cell[3][1].isupper() or not splitted_cell[3][0] == '"' or not splitted_cell[3][2] == '"':
        raise ValueError('Inside cells every cell after attribute col= must have space and then one capital letter between "" which represents id of that column, example of valid cell : <cell row="1" col= "A" />')
    # row number is integer
    if not splitted_cell[1].startswith("row=\"") or not splitted_cell[1][5:-1].isdigit():
        raise ValueError('Inside cells first argument for every cell must be row="integer" where integer is number which represents id for that row, example of valid cell : <cell row="1" col= "A" />')
    row_number = int(splitted_cell[1][5:-1])
    # mapping: A-> 1, B-> 2...
    col_number = ord(splitted_cell[3][1]) - 64
    return row_number, col_number

# parse start point and end point based on point_name


def parse_point(splitted_line, point_name):
    if splitted_line[0] != f'<{point_name}':
        raise ValueError(f'{point_name} must start with open tag <{point_name}')
    if splitted_line[2] != "col=":
        raise ValueError(f'Second argument for {point_name} must be col=')
    if splitted_line[4] != "/>":
        raise ValueError(f'{point_name} must close with end tag />')
    if not splitted_line[3][1].isupper() or not splitted_line[3][0] == '"' or not splitted_line[3][2] == '"':
        raise ValueError(f'For {point_name} after attribute col= must be space and then one capital letter between "" which represents id of {point_name} column')
    if not splitted_line[1].startswith("row=\"") or not splitted_line[1][5:-1].isdigit():
        raise ValueError(f'For {point_name} first argument must be row="integer" where integer is number which represents id for {point_name} row')
    row_number = int(splitted_line[1][5:-1])
    col_number = ord(splitted_line[3][1]) - 64
    return row_number, col_number


# user only gave path to the map description file as command line argument
if len(argv) == 2:
    map_description_file_path = argv[1]
    task_solution_file_path = 'shortest_paths.json'
# user gave path to the map description file as second command line argument
# user gave path to the map task solution file as third command line argument
elif len(argv) == 3:
    map_description_file_path = argv[1]
    task_solution_file_path = argv[2]
# user didn't give paths as command line arguments
else:
    map_description_file_path = input("Enter path to map description file : ")
    task_solution_file_path = input("""Enter path for task solution file with shortest paths 
    (Optional - press Enter to skip step) : """) or "shortest_paths.json"
# time at the start of algorithm
start_time = time()

try:
    with open(map_description_file_path, "r") as map_description_file:
        map_description_lines = map_description_file.readlines()
except PermissionError:
    print(f"There is no permission to read map description file {map_description_file_path}")
    exit()
except FileNotFoundError:
    print(f"Map description file on path {map_description_file_path} is not found")
    exit()
try:
    adjacency_list, source, destination = parse_map_description_lines(map_description_lines)
except ValueError as v:
    print(v)
    exit()
# result is dictionary where key-value pair is vertex and array of his parent
# over which is the shortest distance from the source vertex
bfs_result = adjacency_list.bfs(source)
# will be populated with lists of shortest paths as a result of all_shortest_paths function
shortest_paths = []
# helper list for all_shortest_path function
current_shortest_path = []
# populate shortest_paths list
adjacency_list.all_shortest_paths(shortest_paths, current_shortest_path, bfs_result, source, destination)
# case when there is no shortest path
if len(shortest_paths) == 0:
    print('There is no shortest path between these two vertices')
else:
    dict_shortest_paths = generate_dict_shortest_paths(shortest_paths)
    task_solution_file_content = generate_task_solution_file_content(dict_shortest_paths, start_time)
    try:
        with open(task_solution_file_path, "w") as task_solution_file:
            # save as json
            dump(task_solution_file_content, task_solution_file, indent=4)
            print(f"Path of task solution file: {Path(task_solution_file.name).absolute()}")
    except PermissionError:
        print(f"There is no permission to write result with shortest paths to the file {task_solution_file_path}")
    except FileNotFoundError:
        print(f"One or more directory on path {task_solution_file_path} for task solution file not exist")

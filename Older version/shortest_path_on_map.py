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


def generate_output_file_content(shortest_paths, start_time):
    output_file_content = {}
    # diff between current time on the end of execution and time on start of program execution
    # time() return value in seconds
    output_file_content["execution_time_in_ms"] = ((time() - start_time) * 1000)
    output_file_content['paths'] = shortest_paths
    return output_file_content


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
    destination = Vertex(end_point_row_number, end_point_col_number)
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


# time at the start of algorithm
start_time = time()

# map description file and possible solution file paths are received as command line arguments
# case when only map description file is given
if len(argv) == 2:
    # argv[0] is script path, argv[1] is map description file path
    try:
        with open(argv[1], "r") as map_description_file:
            map_description_lines = map_description_file.readlines()
    except PermissionError:
        print("There is no permission to read map description file")
        exit()
    except FileNotFoundError:
        print("Map description file which is given with path as second command line argument is not found")
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
        output_file_content = generate_output_file_content(dict_shortest_paths, start_time)
        try:
            with open("shortest_paths.json", "w") as output_file:
                # save as json
                dump(output_file_content, output_file, indent=4)
                print(f"Path of output file: {Path(output_file.name).absolute()}")
        except PermissionError:
            print("There is no permission to write result with shortest paths to the file in this directory. Please move script to other directory")

# case when are given and map description file and possible solution as command line arguments
elif len(argv) == 3:
    try:
        # argv[1] is map description file path
        with open(argv[1], "r") as map_description_file:
            map_description_lines = map_description_file.readlines()
    except PermissionError:
        print("There is no permission to read map description file")
        exit()
    except FileNotFoundError:
        print("Map description file which is given with path as second command line argument is not found")
        exit()
    try:
        # argv[2] is the path to possible solution file
        with open(argv[2], "r") as possible_solution_file:
            possible_solution_parsed = load(possible_solution_file)
    except PermissionError:
        print("There is no permission to read possible solution file")
        exit()
    except FileNotFoundError:
        print("Possible solution file which is given with path as third command line argument is not found. This file and optional and you could try again without")
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
        # length of paths list from user's solution
        number_of_user_shortest_paths = len(possible_solution_parsed["paths"])
        # length of paths list which our algorithm generated
        number_of_app_generated_shortest_paths = len(dict_shortest_paths)
        # this will be set to True if user provided at list one shortest path
        found_at_least_one = False
        # this will be set to True if user provided all shortest paths
        found_all = True
        # iterating through shortest paths generated from app
        for current_shortest_path_app in dict_shortest_paths:
            # this will be set to True if user provided this path in his solution
            found_this = False
            # iteratig through user's shortest paths
            for current_shortest_path_user in possible_solution_parsed["paths"]:
                # == checks for equality between dictionaries in this keys
                # only path with right order from source to destination are valid
                if current_shortest_path_app["points"] == current_shortest_path_user["points"]:
                    if not found_at_least_one:
                        found_at_least_one = True
                    found_this = True
                    # path found in user's path, break inner loop
                    break
            # break outer loop if at least one path user didn't provide and at least one correct user did provide
            if not found_this:
                found_all = False
            if not found_all and found_at_least_one:
                break
        # second condition checks if the user has in addition to all valid and a excess in the form of an invalid path
        if found_all and number_of_app_generated_shortest_paths == number_of_user_shortest_paths:
            print("Excellent! Your solution is completely correct")
            exit()
        # if user's solution is partially corrent or completely incorrect print a message
        # and path to complete solution provided by our app
        if found_at_least_one:
            print("Your solution is partially correct, you can find all shortest paths in result file.")
        else:
            print("Your solution is wrong, you can find all shortest paths in result file.")
        output_file_content = generate_output_file_content(dict_shortest_paths, start_time)
        try:
            with open("shortest_paths.json", "w") as output_file:
                # save as json
                dump(output_file_content, output_file, indent=4)
                print(f"Path of result file: {Path(output_file.name).absolute()}")
        except PermissionError:
            print("There is no permission to write result with shortest paths to the file in this directory. Please move script to other directory")
else:
    # given invalid number of command line arguments
    print("App execution is possible as two arguments (second argument is the path to map description file) or three arguments (third argument is the path to possible solution)")

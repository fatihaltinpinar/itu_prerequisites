import json
import parser

# We are using classes for management of data and stuff. I wanted to put everything into a 20by15 array
# so everything will a have coordinate which will make path finding very easy.


# Lecture class contains lecture code, name, it's prerequisites and position of it in the array.
class Lecture:
    def __init__(self, lecture_code=None, lecture_name=None, prerequisites: list = [], y=None, x=None) -> None:
        self.lecture_code = lecture_code
        self.lecture_name = lecture_name
        self.prerequisites = prerequisites
        self.y = y
        self.x = x

    def set_lecture(self, lecture_code, lecture_name, prerequisites=[]):
        self.lecture_code = lecture_code
        self.lecture_name = lecture_name
        self.prerequisites = prerequisites


# Class do not need any information other than their positions.
class Node:
    def __init__(self, y, x):
        self.x = x
        self.y = y


# This function creates the 20by15 matrix that contains all the lectures and nodes
# It returns a list of 20 lists(rows)
def create_array(program_data, lecture_data):

    arr = []
    # Creating the empty list of lists since Python does not have arrays.
    for row in range(20):
        r = []
        for column in range(15):
            # If the row number is odd it's going to be a node.
            if row % 2 != 0:
                r.append(Node(row, column))
            # If column number is odd it's going to be a node.
            elif column % 2 != 0:
                r.append(Node(row, column))
            # Any other position will have a lecture in it.
            # We initialize with a empty lecture that just contains it's positions
            else:
                r.append(Lecture(y=row, x=column))
        # We add the list r which was the row that we created to the list arr which is the matrix.
        arr.append(r)

    # Filling the array by going over program_data.
    # program_data is a dict formatted as following:
    # {
    # '0' : ['blg101', 'mat103', 'mat281' ....]
    # '1' : ['blg231', 'blgsomethingelse', ....]
    #  .
    #  .
    # '8' : ['you get it right?']
    # }

    # We have to put the lectures into the cells which have even y and x.
    # Because of that we hold the data column and row and increase them by 2.
    # Also we fill the array column by column since our data comes as semester by semester which should

    column = 0
    for value in program_data.values():
        row = 0
        for lecture in value:
            # If a lecture is in the lecture_data we do have it's name in there so we put it
            # Otherwise we put the lecture code we get from the program page. This is required because of the
            # lessons that doesn't have a code like Semester Elect. Courses
            if lecture in lecture_data.keys():
                arr[row][column].set_lecture(lecture, lecture_data[lecture]['lecture_name'],
                                             lecture_data[lecture]['lecture_preq'])
            else:
                arr[row][column].set_lecture(lecture, lecture)
            row += 2
        column += 2

    return arr


# Creates the table element that we'll put in every prerequisite page.
def create_table(arr):

    # First row contains cells that show which column shows which semester.
    table = '<table class="onsart"><tr>'
    for column in range(15):
        if column % 2 == 0:
            table += '<td class="semester">' + str(int(column / 2) + 1) + '. Dönem</td>'
        else:
            table += '<td></td>'
    table += '</tr>'

    for row in arr:
        # Creating first row.
        table += '<tr>'
        for column in row:
            # If an item in arr is a lecture we create the lecture_cell element as follows.
            # If you want better visualization you should check BLG.html in a browser by inspecting elements.
            if type(column) == Lecture:
                table += '<td class="lecture_cell">'
                if column.lecture_code is not None:
                    table += f'''<div id="{column.y}_{column.x}" class="lecture_container">
                                    <div class="lecture_code">{column.lecture_code}</div>
                                    <div class="lecture_name">{column.lecture_name}</div>
                                </div>'''
                table += '</td>'
            else:
                table += f'<td class="node_cell"><div class="node" id="{column.y}_{column.x}"></div></td>'

        table += '</tr></table>'
    return table


def find_location(preq_lecture, arr, column):
    for x in range(0, column, 2):
        for y in range(0, 20, 2):
            if arr[y][x].lecture_code == preq_lecture:
                return x, y
    return -1, -1


def find_connections(arr, lecture_data):
    script = ''
    for column in range(2, 15, 2):
        for row in range(0, 20, 2):
            lecture_code = arr[row][column].lecture_code
            if lecture_code is not None:
                try:
                    prerequisites = lecture_data[lecture_code]['lecture_preq']
                    print(prerequisites)
                except KeyError:
                    continue
                if len(prerequisites) == 0:
                    continue
                else:
                    for preq_lecture in prerequisites:
                        preq_x, preq_y = find_location(preq_lecture, arr, column)
                        if preq_x != -1:
                            script += f"connect_lectures({preq_y}, {preq_x}, {row}, {column});\n"
                            # print(f'lecture {lecture_code} is connected to {arr[preq_y][preq_x].lecture_code} located'
                            #       f' at row= {preq_y}, column={preq_x}')
    return script


# Printing the array in console for debugging.
def print_array(arr):
    for row in arr:
        for column in row:
            if type(column) == Lecture:
                print(f'{column.lecture_code}', end='\t')
            else:
                print('x', end='\t')
        print()


def create_page(title, table, script):
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta name="description" content="Fancy charts instead of http://www.sis.itu.edu.tr/eng/prerequisites/">
    <meta name="keywords" content="sis, itu, ön şart, on sart, prerequisites, istanbul teknik üniversitesi, itü">

	<meta name="author" content="faati">
	<link rel="shortcut icon" type="image/x-icon" href="../favicon.ico" />

    <link rel="stylesheet" type="text/css" href="../css/preq.css"/>


</head>
<body>
<div class="topBar"></div>
<div class="content">
    
    <canvas id="canvas" height="1200px" width="1300px"></canvas>
    {table}
</div>
<div class="bottomBar"></div>
<script src="../javascript/draw.js"></script>
<script>
    {script}
</script>
</body>
</html>'''
    return html


# Hope this we can write something into this function lmao
def update_pages():
    with open('lectures.json') as lectures_file:
        lecture_data = json.load(lectures_file)
    with open('programs.json') as programs_file:
        programs_data = programs_file

    for faculty_dict in programs_data.values():
        for program_code, program_link in faculty_dict.items():
            print(f'Creating the prerequisite page of {program_code} which located at {program_link}')
            title = program_code
            program_data = parser.parse_program(program_link)
            arr = create_array(program_data, lecture_data)
            table = create_table(arr)
            script = find_connections(arr, lecture_data)

            with open('onsart/prerequisite_pages/' + program_code + '.html', 'w') as htmlfile:
                htmlfile.write(create_page(title, table, script))


if __name__ == '__main__':
    with open('lectures.json') as lectures_file:
        l_data = json.load(lectures_file)
    with open('test.json') as program_file:
        p_data = json.load(program_file)
    arr_ = create_array(p_data, l_data)

    # find_connections(arr_, l_data)

    # table_ = create_table(arr_)

    # with open('test.html', 'w') as test_file:
    #     test_file.write(table_)

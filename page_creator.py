import json


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


# Printing the array in console for debugging.
def print_array(arr):
    for row in arr:
        for column in row:
            if type(column) == Lecture:
                print(f'{column.lecture_code}', end='\t')
            else:
                print('x', end='\t')
        print()


# Hope this we can write something into this function lmao
def update_pages():
    print('HI. I\'ll update every page one day wohoo!')


if __name__ == '__main__':
    with open('lectures.json') as lectures_file:
        l_data = json.load(lectures_file)
    with open('test.json') as program_file:
        p_data = json.load(program_file)
    arr_ = create_array(p_data, l_data)
    table_ = create_table(arr_)

    with open('test.html', 'w') as test_file:
        test_file.write(table_)

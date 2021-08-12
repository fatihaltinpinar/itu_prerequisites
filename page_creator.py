import json
import os
def get_course_constructor(course_id, course_name, semester, course_type, preqs):
    constructor = f"""courseDict["{course_id}"] = new Course("{course_id}", "{course_name}", {semester}, "{course_type}", {str(preqs)});\n"""
    return constructor


def create_page(program_name, program_data, preqs, template):
    constructors = ''
    for _semester in program_data.keys():
        semester = int(_semester) + 1
        for code, course_name in program_data[_semester].items():
            if 'sec' not in code:
                constructors += get_course_constructor(code, course_name, semester, 'Zorunlu', preqs.get(code, []))
            else:
                course_type = 'Secmeli ' + program_data[_semester][code]['type']
                for key, val in program_data[_semester][code]['0'].items():
                    constructors += get_course_constructor(key, val, semester, course_type, preqs.get(key, []))

    with open(os.path.join('onsart', program_name) + '.html', 'w') as f:
        f.write(template % (program_name, program_name, constructors))

def create_pages(program_data, preqs, template):
    for key, val in program_data.items():
        create_page(key, val, preqs, template)

if __name__ == '__main__':
    program_data = {}
    with open('blg_program.json', 'r') as f:
        program_data = json.load(f)
    preqs = {}
    with open('preqs.json', 'r') as f:
        preqs = json.load(f)
    template = ''
    with open('onsart/template.html', 'r') as f:
        template = f.read()
    create_pages(program_data, preqs, template)
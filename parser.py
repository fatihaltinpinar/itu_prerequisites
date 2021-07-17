import requests
import json
from bs4 import BeautifulSoup

# Code for acquiring tuple below.
def get_course_codes():
    page = requests.get('https://www.sis.itu.edu.tr/TR/ogrenci/lisans/onsartlar/onsartlar.php')
    soup = BeautifulSoup(page.text, 'html.parser')
    options = soup.find_all('option')

    course_codes = []

    for option in options:
        opt = option.attrs['value']
        if opt != '':
            course_codes.append(opt)
    return course_codes

# page = requests.get('http://www.sis.itu.edu.tr/tr/onsart/').text
# soup = BeautifulSoup(page, 'html.parser')
# options = soup.find('option')
# for i in options:
#   print(i.attrs['value']
#
# course_codes = ('AKM', 'ATA', 'BED', 'BIL', 'BIO', 'BLG', 'BUS', 'CAB', 'CEV', 'CHZ', 'CIE', 'CMP', 'COM', 'DEN', 'DFH',
#                 'DNK', 'DUI', 'EAS', 'ECO', 'ECN', 'EHB', 'EHN', 'EKO', 'ELE', 'ELH', 'ELK', 'END', 'ENR', 'ESL', 'ETH',
#                 'ETK', 'EUT', 'FIZ', 'GED', 'GEM', 'GEO', 'GID', 'GMI', 'GSB', 'GUV', 'HUK', 'HSS', 'ICM', 'ILT', 'IML',
#                 'ING', 'INS', 'ISE', 'ISL', 'ISH', 'ITB', 'JDF', 'JEF', 'JEO', 'KIM', 'KMM', 'KMP', 'KON', 'MAD', 'MAK',
#                 'MAL', 'MAR', 'MAT', 'MCH', 'MEK', 'MEN', 'MET', 'MIM', 'MOD', 'MRE', 'MRT', 'MTO', 'MTH', 'MTM', 'MTR',
#                 'MST', 'MUH', 'MUK', 'MUT', 'MUZ', 'NAE', 'NTH', 'PAZ', 'PEM', 'PET', 'PHE', 'PHY', 'RES', 'SBP', 'SES',
#                 'STA', 'STI', 'TEB', 'TEK', 'TEL', 'TER', 'TES', 'THO', 'TUR', 'UCK', 'UZB', 'YTO')


program_codes = ('INS', 'INSE', 'GEO', 'GEOE', 'CEV', 'CEVE',   # insaat
                'MIM', 'MIME', 'SBP', 'SBPE', 'EUT', 'EUTE', 'ENTE', 'ICM', 'PEM', 'PEME', #mimarlik
                'MAK', 'MAKE', 'IML', 'IMLE',  #makina
                'ELH', 'EHB', 'EHBE', 'ELK', 'ELKE', 'ELE', 'TEL', 'KOM', 'KOME', # Elektrik Elektronik
                'JEO', 'JEOE', 'JEF', 'JEFE', 'MAD', 'MADE', 'PET', 'PETE', 'CHZ', 'CHZE', #maden
                'KMM', 'KMME', 'GID', 'GIDE', 'MET', 'METE', # kimya
                'ISL', 'ISLE', 'END', 'ENDE', 'ECNE', #isletme
                'DEN', 'DENE', 'GEM', 'GEME',  #gemi
                'MAT', 'MATE', 'FIZ', 'FIZE', 'KIM', 'KIME', 'BIO', 'BIOE', #fen edebiyat
                'MTO', 'MTOE', 'UZB', 'UZBE', 'UCK', 'UCKE', #ucka
                'TEB', 'MTR', 'SES', 'KMP', 'BST', 'MUT', 'MZT', 'MUZ', 'MUZE', 'CAB', 'CEB', 'THO', # turk musikisi
                'DUI', 'DUIE', 'GMI', 'GMIE', #deniz
                'TEK', 'TEKE', #tekstil
                'BLG', 'BLGE', 'YZVE', #XD
                'SIS', 'SEK', 'SIN', 'AIN', 'SBL', 'SDU', 'SGM', 'SGI', 'SMT', 'STP', 'SCE', 'MBI', 'MCB', 'SEN', 'EHN', #hala elle yaziyorum
                'MTM', 'MEN', 'NAE') # yani neden sitenin burasi dinamik? niye cavaciprit calistirionuz bida tobest

# Checks if string_to_remove exists inside string. If it does, it removes it otherwise returns the string back.
def check_and_remove(string, string_to_remove):
    if string_to_remove in string:
        return string.replace(string_to_remove, '')
    return string


# Parse function for prerequisite string given.
def parse_preq(preq_string, course_codes):
    preq_list = []

    # If prerequisites are given as 'Yok' it means no prerequisite for this lecture, returns empty list.
    if 'Yok' in preq_string:
        return preq_list

    # Checking for special cases. Adding them to the preq_list. For
    # bitirme_onsart : http://www.sis.itu.edu.tr/bitirme_onsart.html,
    # ingonsart : http://www.sis.itu.edu.tr/ingonsart.html
    # will be used later.
    if '  Diğer Şartlar' in preq_string:
        preq_string = preq_string.replace('  Diğer Şartlar', '')
        preq_list.append('bitirme_onsart')
    if ' Önşartı için tıklayınız.' in preq_string:
        preq_string = preq_string.replace(' Önşartı için tıklayınız.', '')
        preq_list.append('ingonsart')

    # Cleaning unnecessary stuff from the preq_string. (, ), MIN DC-DD.
    # ve and veya are also removed since we'll be drawing the graph based on programs which wont contain both lectures
    # at the same time. Since it makes no sense. We'll look for every lecture in preq_list while drawing. Which lets
    # us cover 've'.
    preq_string = check_and_remove(preq_string, '(')
    preq_string = check_and_remove(preq_string, ')')
    preq_string = check_and_remove(preq_string, 'MIN DD')
    preq_string = check_and_remove(preq_string, 'MIN DC')
    preq_string = check_and_remove(preq_string, 'veya ')
    preq_string = check_and_remove(preq_string, 've')

    # Lecture codes does have a space between number and letter part of the lecture. Deleting those will help us to
    # get codes by splitting the string.
    for course_code in course_codes:
        if course_code in preq_string:
            preq_string = preq_string.replace((course_code + ' '), course_code)

    # Splitting preq_string by spaces will give us lecture list. We add that list to the preq_list.
    if len(preq_string) > 0:
        preq_list.extend(preq_string.split(' '))

    # Every value has a different way of writing. Some of them have a space after it like 'veya ', every lecture code
    # has a space after it and so on. I tried covering them as much as I can. Still we can have spaces at the end of
    # preq_string which adds a empty string to the list. We remove them with this code.
    preq_list = list(filter(None, preq_list))

    # Returning the list
    return preq_list


def parse_lectures(course_codes):

    data = {}
    # Going over every course_code in the tuple given above.
    for course_code in course_codes:

        print('\nLooking for', course_code)
        # Getting page data from sis.itu.edu.tr
        try:
            page = requests.post('https://www.sis.itu.edu.tr/TR/ogrenci/lisans/onsartlar/onsartlar.php',
                                 data={'derskodu': course_code}).content
        except requests.exceptions.ConnectionError as error:
            print('Can not connect to sis.itu.edu.tr', error)
        except Exception:
            print('Unexpected error while loading prerequisite page.')
            raise

        print('Making soup of', course_code)
        # Making the soup and finding the table part of the soup. Since we only need the table that contains,
        # lectures and their prerequisites.
        soup = BeautifulSoup(page, 'html.parser')
        preq_table = soup.find('table', {'class': ['table','table-bordered', 'table-striped', 'table-hover']})

        print('Parsing lectures of', course_code)
        lecture_data = {}

        try:
            rows = preq_table.find_all('tr')
            rows.pop(0)
            # Going over every row.
            for tr in rows:
                td = tr.find_all('td')

                # Taking the first column of the row which contains lecture id.
                lecture_id = td[0].get_text().replace(' ', '')

                # Taking the second column of the row which contains full name of that lecture.
                # not needed
                # lecture_name = td[1].get_text()

                # Getting the string from the third column of the row which contains the prerequisites as a string.
                # We send that string to be parsed in parse_preq function. Which will return a list of prerequisites.
                lecture_preq = parse_preq(td[2].get_text(), course_codes)

                # We add these information into a temporary dictionary.
                lecture_data = {lecture_id: lecture_preq}

                data.update(lecture_data)
        except AttributeError as error:
            print('This page is missing stuff! Lecture: ', course_code)
            print(error)

        except Exception:
            print('Unexpected error while parsing.')
            raise

        # Updating data which contains all lectures by a format
        # lecture_id: {
        #               'lecture_name' : lecture_name
        #               'lecture_preq' : lecture_preq
        # }

    return data


# Parses program pages and returns a dictionary that contains semesters and lectures
# should be taken that semester.
def parse_program(program_link):
    # Gets link and creates the soup.
    program = program_link[:program_link.rfind('/')+1]
    response = requests.get(program_link)
    program_page = BeautifulSoup(response.content, 'html.parser')

    # Finding the tables which contains curriculum for that semester.
    semester_tables = program_page.find_all('table', {'id': 'myTable'})

    semester_number = 0
    program_data = {}

    # Every table that we found in semester_tables represent that semester. We give it a number and parse it one by one.
    for semester in semester_tables:
        # Going over every row. Every row contains one lecture in it.
        rows = semester.find_all('tr')
        course_list = {}
        elective_no = 1

        for row in rows:
            # In a given row first column contains the lecture code and the second one contains the lecture's full name.
            # We need the second column only if the first column is empty for the given lecture. This occurs for the
            # elective courses.
            cols = row.find_all('td')
            course_code = cols[0].get_text().replace(' ', '')
            if course_code == 'DersKodu':
                continue
            course_name = cols[1]
            elective_link = course_name.find_all('a')
            if (len(elective_link) > 0):
                link = program + elective_link[0]['href']
                text = elective_link[0].text
                elec_type = cols[7].text
                data = {'type':elec_type,
                'semester':semester_number}
                data.update(parse_program(link))
                course_list.update({
                    'sec'+str(elective_no): data})
                elective_no += 1
            else:
                course_list.update({course_code: course_name.text})

            # print(course_code)

            # elif course_code == ' ':
            #     course_code = cols[1].get_text()
        program_data.update({semester_number: course_list})
        semester_number += 1
    return program_data


def parse_preqs():
    with open('preqs.json', 'w') as lectures_file:
        course_codes = get_course_codes()
        json.dump(parse_lectures(course_codes), lectures_file, indent=2, ensure_ascii=False)

def parse_programs(program_codes):
    program_data = {}
    plan = 'https://www.sis.itu.edu.tr/TR/ogrenci/lisans/ders-planlari/plan/'
    for program_code in program_codes:
        print(f'Parsing {program_code}...')
        program_link = plan + program_code + '/'
        r = requests.get(program_link)
        soup = BeautifulSoup(r.content, 'html.parser')
        links = soup.find_all('a',{'title':'Ders Planını Görmek İçin Tıklayınız'})
        if len(links) == 0:
            print("\nThis is not supposed to happen")
            print("Happened with", program_code, '\n')
        else:
            program_link += links[-1]['href']
            program_data.update({program_code: parse_program(program_link)})

    with open('program_data.json', 'w') as f:
        json.dump(program_data, f, indent=2, ensure_ascii=False)

# For running parser.py alone
if __name__ == '__main__':
    # parse_preqs()
    parse_programs(program_codes)
    # program = parse_program('https://www.sis.itu.edu.tr/TR/ogrenci/lisans/ders-planlari/plan/BLGE/201810.html')
    # print(program)
    # print('it takes really long if you really want to update it change the source code and uncomment line above')

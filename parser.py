import requests
import json
from bs4 import BeautifulSoup

# Code for acquiring tuple below.
# page = requests.get('http://www.sis.itu.edu.tr/tr/onsart/').text
# soup = BeautifulSoup(page, 'html.parser')
# options = soup.find('option')
# for i in options:
#   print(i.attrs['value']

programCodes = ('AKM', 'ATA', 'BED', 'BIL', 'BIO', 'BLG', 'BUS', 'CAB', 'CEV', 'CHZ', 'CIE', 'CMP', 'COM', 'DEN', 'DFH',
                'DNK', 'DUI', 'EAS', 'ECO', 'ECN', 'EHB', 'EHN', 'EKO', 'ELE', 'ELH', 'ELK', 'END', 'ENR', 'ESL', 'ETH',
                'ETK', 'EUT', 'FIZ', 'GED', 'GEM', 'GEO', 'GID', 'GMI', 'GSB', 'GUV', 'HUK', 'HSS', 'ICM', 'ILT', 'IML',
                'ING', 'INS', 'ISE', 'ISL', 'ISH', 'ITB', 'JDF', 'JEF', 'JEO', 'KIM', 'KMM', 'KMP', 'KON', 'MAD', 'MAK',
                'MAL', 'MAR', 'MAT', 'MCH', 'MEK', 'MEN', 'MET', 'MIM', 'MOD', 'MRE', 'MRT', 'MTO', 'MTH', 'MTM', 'MTR',
                'MST', 'MUH', 'MUK', 'MUT', 'MUZ', 'NAE', 'NTH', 'PAZ', 'PEM', 'PET', 'PHE', 'PHY', 'RES', 'SBP', 'SES',
                'STA', 'STI', 'TEB', 'TEK', 'TEL', 'TER', 'TES', 'THO', 'TUR', 'UCK', 'UZB', 'YTO')


# Checks if string_to_remove exists inside string. If it does, it removes it otherwise returns the string back.
def check_and_remove(string, string_to_remove):
    if string_to_remove in string:
        return string.replace(string_to_remove, '')
    return string


# Parse function for prerequisite string given.
def parse_preq(preq_string):
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
    for program_code in programCodes:
        if program_code in preq_string:
            preq_string = preq_string.replace((program_code + ' '), program_code)

    # Splitting preq_string by spaces will give us lecture list. We add that list to the preq_list.
    if len(preq_string) > 0:
        preq_list.extend(preq_string.split(' '))

    # Every value has a different way of writing. Some of them have a space after it like 'veya ', every lecture code
    # has a space after it and so on. I tried covering them as much as I can. Still we can have spaces at the end of
    # preq_string which adds a empty string to the list. We remove them with this code.
    preq_list = list(filter(None, preq_list))

    # Returning the list
    return preq_list


def parse_lectures(program_codes):

    data = {}
    # Going over every program_code in the tuple given above.
    for program_code in program_codes:

        print('\nLooking for', program_code)
        # Getting page data from sis.itu.edu.tr
        try:
            page = requests.post('http://www.sis.itu.edu.tr/tr/onsart/onsart_tr.php',
                                 data={'ders_kodu': program_code}).content
        except requests.exceptions.ConnectionError as error:
            print('Can not connect to sis.itu.edu.tr', error)
        except Exception:
            print('Unexpected error while loading prerequisite page.')
            raise

        print('Making soup of', program_code)
        # Making the soup and finding the table part of the soup. Since we only need the table that contains,
        # lectures and their prerequisites.
        soup = BeautifulSoup(page, 'html.parser')
        preq_table = soup.find('table', {'class': 'onsart'})

        print('Parsing lectures of', program_code)
        lecture_data = {}

        try:
            rows = preq_table.findAll('tr')
            rows.pop(0)
            # Going over every row.
            for tr in rows:
                td = tr.findAll('td')

                # Taking the first column of the row which contains lecture id.
                lecture_id = td[0].get_text().replace(' ', '')

                # Taking the second column of the row which contains full name of that lecture.
                lecture_name = td[1].get_text()

                # Getting the string from the third column of the row which contains the prerequisites as a string.
                # We send that string to be parsed in parse_preq function. Which will return a list of prerequisites.
                lecture_preq = parse_preq(td[2].get_text())

                # We add these information into a temporary dictionary.
                lecture_data = {lecture_id: {'lecture_name': lecture_name,
                                             'lecture_preq': lecture_preq
                                             }}
        except AttributeError as error:
            print('This page is missing stuff! Lecture: ', program_code)
            print(error)

        except Exception:
            print('Unexpected error while parsing.')
            raise

        # Updating data which contains all lectures by a format
        # lecture_id: {
        #               'lecture_name' : lecture_name
        #               'lecture_preq' : lecture_preq
        # }
        data.update(lecture_data)

    return data


def update_lectures():
    with open('lectures.json', 'w') as f:
            json.dump(parse_lectures(programCodes), f, indent=2, ensure_ascii=False)


# For running parser.py alone
if __name__ == '__main__':
    update_lectures()

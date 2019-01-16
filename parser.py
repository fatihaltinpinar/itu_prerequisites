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

#   dersler {
#       'BLG 101E' : {
#                   'ders-adi' : (ders-kodu + ders-adi)
#                   'dersin onsarlari' : ['blg100e', 'blg31']
#               }
#
#       }

# "AKM 214 MIN DDveya AKM 214E MIN DD"
# "Yok  "
#   " Önşartı için tıklayınız.": "http://www.sis.itu.edu.tr/ingonsart.html",
# "  Diğer Şartlar": "http://www.sis.itu.edu.tr/bitirme_onsart.htm",


def check_and_remove(string, string_to_remove):
    if string_to_remove in string:
        return string.replace(string_to_remove, '')
    return string


# noinspection SpellCheckingInspection
def parse_preq(preq_string):
    preq_list = []
    if 'Yok' in preq_string:
        return preq_list
    # noinspection SpellCheckingInspection
    if '  Diğer Şartlar' in preq_string:
        preq_string = preq_string.replace('  Diğer Şartlar', '')
        preq_list.append('bitirme_onsart')
    if ' Önşartı için tıklayınız.' in preq_string:
        preq_string = preq_string.replace(' Önşartı için tıklayınız.', '')
        preq_list.append('ingonsart')

    preq_string = check_and_remove(preq_string, '(')
    preq_string = check_and_remove(preq_string, ')')
    preq_string = check_and_remove(preq_string, 'MIN DD')
    preq_string = check_and_remove(preq_string, 'MIN DC')
    preq_string = check_and_remove(preq_string, 'veya ')
    preq_string = check_and_remove(preq_string, 've')

    for program_code in programCodes:
        if program_code in preq_string:
            preq_string = preq_string.replace((program_code + ' '), program_code)
    try:
        if preq_string[-1] == ' ':
            preq_string = preq_string[:-1]
    except IndexError:
        preq_list = list(filter(None, preq_list))
        return preq_list
    preq_list.extend(preq_string.split(' '))
    preq_list = list(filter(None, preq_list))
    return preq_list


def parse_lectures(program_codes):

    data = {}
    for program_code in program_codes:

        print('\nLooking for', program_code)
        try:
            page = requests.post('http://www.sis.itu.edu.tr/tr/onsart/onsart_tr.php',
                                 data={'ders_kodu': program_code}).content
        except requests.exceptions.ConnectionError as error:
            print('Can not connect to sis.itu.edu.tr', error)
        except Exception:
            print('Unexpected error while loading prerequisite page.')
            raise

        print('Making soup of', program_code)
        soup = BeautifulSoup(page, 'html.parser')
        preq_table = soup.find('table', {'class': 'onsart'})

        print('Parsing lectures of', program_code)
        lecture_data = {}
        try:
            rows = preq_table.findAll('tr')
            rows.pop(0)
            for tr in rows:
                td = tr.findAll('td')

                lecture_id = td[0].get_text().replace(' ', '')
                lecture_name = td[1].get_text()
                lecture_preq = parse_preq(td[2].get_text())

                lecture_data = {lecture_id: {'lecture_name': lecture_name,
                                             'lecture_preq': lecture_preq
                                             }}
        except AttributeError as error:
            print('This page is missing stuff! Lecture: ', program_code)
            print(error)

        except Exception:
            print('Unexpected error while parsing.')
            raise

        data.update(lecture_data)

    return data


if __name__ == '__main__':
    with open('lectures.json', 'w') as f:
            json.dump(parse_lectures(programCodes), f, indent=2, ensure_ascii=False)

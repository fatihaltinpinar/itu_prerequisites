import requests
from bs4 import BeautifulSoup

courseCodes = ('AKM', 'ATA', 'BED', 'BIL', 'BIO', 'BLG', 'BUS', 'CAB', 'CEV', 'CHZ', 'CIE', 'CMP', 'COM', 'DEN', 'DFH',
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


def parse_lectures(course_code):
    lectureData = {}
    page = requests.post('http://www.sis.itu.edu.tr/tr/onsart/onsart_tr.php', data={'ders_kodu': course_code}).content
    soup = BeautifulSoup(page, 'html.parser')
    preqTable = soup.find('table', {'class': 'onsart'})

    lecture = preqTable.findChildren('tr')

    print(soup)

    return lectureData

if __name__ == '__main__':
    parse_lectures('BLG')

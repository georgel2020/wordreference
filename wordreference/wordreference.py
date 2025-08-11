import requests
from bs4 import BeautifulSoup

def get_dictionary(word: str) -> tuple:
    url = f'https://www.wordreference.com/enzh/{word}'
    response = requests.get(url)
    if response.status_code != 200:
        return '', ''

    soup = BeautifulSoup(response.text, 'html.parser')
    article_wrd = soup.find('div', id='articleWRD')
    table_rows = article_wrd.find_all('tr', class_=['odd', 'even', 'wrtopsection'])

    meanings = []
    sections = []
    current_section = -1
    current_index = 0
    last_class = 'odd'
    for row in table_rows:
        if 'wrtopsection' in row.get('class'):
            sections.append(row.get_text().strip('：'))
            current_section += 1
            meanings.append([])
            current_index = 0
            last_class = 'odd'
            continue
        if last_class not in row.get('class'):
            last_class = row.get('class')[0]
            current_index += 1

        if len(row.find_all('td')) >= 3:
            columns = row.find_all('td')
            if columns[0].get('class') == ['FrWrd']:
                meanings[current_section].append({})
                meanings[current_section][current_index]['source'] = columns[0].find('strong').get_text()
                if columns[0].find('em', class_='POS2'):
                    meanings[current_section][current_index]['part_of_speech'] = columns[0].find('em', class_='POS2').get_text()
                meanings[current_section][current_index]['synonym'] = columns[1].get_text()
            if columns[2].get('class') == ['ToWrd']:
                zhgroups = columns[2].find_all('span', class_='zhgroup')
                simplified_zhgroups = [zhgroup for zhgroup in zhgroups if zhgroup.find('span', class_='simplified')]
                for simplified_zhgroup in simplified_zhgroups:
                    if simplified_zhgroup.find('span', class_='simplified'):
                        simplified_zhgroup.find('span', class_='simplified').extract()
                    if simplified_zhgroup.find('span', class_='pinyintxt'):
                        simplified_zhgroup.find('span', class_='pinyintxt').extract()
                translation = '，'.join([simplified_zhgroup.get_text().strip() for simplified_zhgroup in simplified_zhgroups])
                if 'translations' in meanings[current_section][current_index].keys():
                    meanings[current_section][current_index]['translation'] += '，' + translation
                else:
                    meanings[current_section][current_index]['translation'] = translation

        if len(row.find_all('td')) == 2:
            sentence_td = row.find('td', colspan='2')
            if sentence_td:
                if sentence_td.get('class') == ['FrEx']:
                    meanings[current_section][current_index]['example'] = sentence_td.get_text()
                if sentence_td.get('class') == ['ToEx']:
                    meanings[current_section][current_index]['example_translation'] = sentence_td.get_text()

    return sections, meanings
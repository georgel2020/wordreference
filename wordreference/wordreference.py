import requests
from bs4 import BeautifulSoup

def get_soup(word: str) -> BeautifulSoup:
    """Get BeautifulSoup object from WordReference. """
    url = f'https://www.wordreference.com/enzh/{word}'
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_dictionary(word: str) -> dict:
    """Get dictionary from WordReference.

    Return tuple of UK pronunciation, US pronunciation, sections and meanings.
    """
    soup = get_soup(word)

    dictionary = {}

    # Handle invalid words.
    no_trans_found = soup.find('div', id='noTransFound')
    if no_trans_found:
        return {
            'error': True
        }

    # Extract pronunciations.
    dictionary['pronunciation'] = {}
    dictionary['pronunciation']['uk'] = ''
    dictionary['pronunciation']['us'] = ''
    pronunciation_widget = soup.find('div', id='pronunciation_widget')
    if pronunciation_widget:
        if pronunciation_widget.find('input', class_='more-pron-state'):
            pronunciation_widget.find('div', class_='more-pron-target').extract()   # Remove hidden pronunciations.

        uk_pronunciation_span = pronunciation_widget.find('span', class_='pronWR')
        if uk_pronunciation_span:
            if uk_pronunciation_span.find('span', style='font-size:12px'):
                uk_pronunciation_span.find('span', style='font-size:12px').extract()
            dictionary['pronunciation']['uk'] = uk_pronunciation_span.get_text().strip()
        us_pronunciation_span = pronunciation_widget.find('span', class_='pronRH')
        if us_pronunciation_span:   # Sometimes only UK pronunciation is available.
            if us_pronunciation_span.find('span', style='font-size:12px'):
                us_pronunciation_span.find('span', style='font-size:12px').extract()
            dictionary['pronunciation']['us'] = us_pronunciation_span.get_text().strip()

    # Extract meanings.
    article_wrd = soup.find('div', id='articleWRD')
    table_rows = article_wrd.find_all('tr', class_=['odd', 'even', 'wrtopsection'])     # `wrtopsection` is a section header.

    dictionary['meanings'] = []
    sections = []   # Certain sections may not have any meanings.
    current_section = -1
    current_index = 0   # Index of the current meaning in the current section.
    last_class = 'odd'  # The first row of each section is always odd.
    for row in table_rows:
        # New section.
        if 'wrtopsection' in row.get('class'):
            sections.append(row.get_text().strip('：'))  # The 复合形式 section has a colon at the end.
            current_section += 1
            dictionary['meanings'].append([])
            current_index = 0
            last_class = 'odd'
            continue
        # New meaning.
        if last_class not in row.get('class'):
            last_class = row.get('class')[0]
            current_index += 1

        # Translation.
        if len(row.find_all('td')) >= 3:
            columns = row.find_all('td')
            # The first line of a meaning.
            if columns[0].get('class') == ['FrWrd']:
                dictionary['meanings'][current_section].append({})
                dictionary['meanings'][current_section][current_index]['source'] = columns[0].find('strong').get_text().strip('⇒')    # Remove conjugate button.
                if columns[0].find('em', class_='POS2'):
                    dictionary['meanings'][current_section][current_index]['part_of_speech'] = columns[0].find('em', class_='POS2').get_text()
                dictionary['meanings'][current_section][current_index]['synonym'] = columns[1].get_text()
            # More lines of a meaning.
            if columns[2].get('class') == ['ToWrd']:
                zhgroups = columns[2].find_all('span', class_='zhgroup')
                simplified_zhgroups = [zhgroup for zhgroup in zhgroups if zhgroup.find('span', class_='simplified')]
                for simplified_zhgroup in simplified_zhgroups:
                    if simplified_zhgroup.find('span', class_='simplified'):
                        simplified_zhgroup.find('span', class_='simplified').extract()
                    if simplified_zhgroup.find('span', class_='pinyintxt'):
                        simplified_zhgroup.find('span', class_='pinyintxt').extract()
                translation = '，'.join([simplified_zhgroup.get_text().strip() for simplified_zhgroup in simplified_zhgroups])
                if 'translations' in dictionary['meanings'][current_section][current_index].keys():   # Handle multiple lines of meaning.
                    dictionary['meanings'][current_section][current_index]['translation'] += '，' + translation
                else:
                    dictionary['meanings'][current_section][current_index]['translation'] = translation

        # Example.
        if len(row.find_all('td')) == 2:
            sentence_td = row.find('td', colspan='2')
            if sentence_td:
                if sentence_td.get('class') == ['FrEx']:    # English sentence.
                    dictionary['meanings'][current_section][current_index]['example'] = sentence_td.get_text()
                if sentence_td.get('class') == ['ToEx']:    # Chinese translation.
                    if 'ⓘ这句话不是该英语句子的翻译。' not in sentence_td.get_text():
                        dictionary['meanings'][current_section][current_index]['example_translation'] = sentence_td.get_text()

    dictionary['sections'] = sections
    dictionary['error'] = False

    return dictionary

import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, URL_PEP
from exceptions import ParserFindTagException, MainException
from outputs import control_output
from utils import find_tag, get_response, get_soup


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]

    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)

        response_section = get_response(session, version_link)
        if response_section is None:
            continue
        soup_section = BeautifulSoup(response_section.text, features='lxml')
        h1 = find_tag(soup_section, 'h1').text
        dl = find_tag(soup_section, 'dl').text.replace('\n', ' ')

        results.append(
            (version_link, h1, dl)
        )

    return results


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
        else:
            raise ParserFindTagException

    for a_tag in a_tags:
        link = a_tag['href']
        regex = re.search(pattern, a_tag.text)
        if regex is not None:
            version = regex.group('version')
            status = regex.group('status')
        else:
            version = a_tag.text
            status = ''
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)
    table = find_tag(soup, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(table, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_tag_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_tag_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response_archive = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response_archive.content)
    logging.info(f'Архив был загружен и сохранен: {archive_path}')


def pep(session):
    total_peps = 0
    status_sum = defaultdict(int)
    results = [('Статус', 'Количество')]

    soup = get_soup(session, URL_PEP)
    section_pep = find_tag(soup, 'section', attrs={'id': 'pep-content'})
    section_index = find_tag(
        section_pep,
        'section',
        attrs={'id': 'numerical-index'}
    )
    tbody_tag = find_tag(section_index, 'tbody')
    tr_tags = tbody_tag.find_all('tr')

    for tr_tag in tr_tags:
        preview_status = find_tag(tr_tag, 'td').text[1:]
        a_href = find_tag(tr_tag, 'a')['href']
        card_link = urljoin(URL_PEP, a_href)
        response = session.get(card_link)
        soup = BeautifulSoup(response.text, features='lxml')
        dt_tags = soup.find_all('dt')

        for dt_tag in dt_tags:
            if dt_tag.text == 'Status:':
                total_peps += 1
                card_status = dt_tag.find_next_sibling().string
                status_sum[card_status] += 1

                if card_status not in EXPECTED_STATUS[preview_status]:
                    error_msg = (
                        'Несовпадающие статусы:\n'
                        f'{card_link}\n'
                        f'Статус в картрочке {card_status}\n'
                        f'Ожидаемые статусы: {EXPECTED_STATUS[preview_status]}'
                    )
                    logging.warning(error_msg)

    for status in status_sum:
        results.append((status, status_sum[status]))
    results.append(('Total', total_peps))

    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()

        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except MainException as error:
        logging.exception(
            f'Возникла ошибка в работе программы {error}',
            stack_info=True,
        )
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()

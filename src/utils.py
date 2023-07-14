from bs4 import BeautifulSoup
from exceptions import ParserFindTagException
from requests import RequestException

import logging


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        print('Что-то пошло не так', error)
        logging.exception(
            f'Возникла ошибка при загрузки страницы {url}',
            stack_info=True,
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs} '
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def get_soup(session, url, encoding='utf-8'):
    response = get_response(session, url, encoding)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    return soup

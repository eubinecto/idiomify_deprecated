# experimenting with functional programming in python
from typing import List, Optional
import requests
import traceback
from bs4 import BeautifulSoup, Tag
from requests import HTTPError


class Failure:
    """
    code reference: https://medium.com/swlh/monads-in-python-e3c9592285d6
    the only difference is that I'm overriding rshift, not or.
    """
    def __init__(self, data, failed: bool = False, failed_msg: str = None):
        self.data = data
        self.failed = failed
        self.failed_msg = failed_msg

    def __str__(self):
        return " ".join([str(self.data), str(self.failed)])

    def __rshift__(self, f):  # >>
        return self.bind(f)

    def bind(self, f):
        if self.failed:
            return self
        try:
            x = f(self.data)
            return Failure(x)
        # If an exception occurs, then the fail flag goes up.
        except Exception as e:
            # print out the exception
            print(traceback.format_exc())
            # because you don't want a big, big job to fail in the middle of the night.
            # you may want to be absolutely sure that the job won't fail at least, albeit
            # the results might be None. Better have something than nothing.
            return Failure(None, failed=True, failed_msg=str(e))


class ThefreeRawsScraper:
    """
    scrapes the definitions of idioms from The Free Dictionary.
    """
    THEFREE_URL = "https://idioms.thefreedictionary.com/{idiom}"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X_batch 10_15_6)'
                      'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3'
                      ' Safari/605.1.15'
    }

    @classmethod
    def fetch(cls, idiom: str, proxy: str = None) -> List[str]:
        # should be able to find the definition div tag.
        # first, try with hyphen (if exists)
        raws = cls.fetch_routine(idiom, proxy)
        if len(raws) > 0:
            return raws
        # else, try without hyphens
        return cls.fetch_routine(idiom.replace("-", " "), proxy)

    @classmethod
    def fetch_routine(cls, idiom: str, proxy: str = None) -> List[str]:
        request_url = cls.THEFREE_URL.format(idiom=idiom)
        if proxy:
            r = requests.get(request_url,
                             headers=cls.HEADERS,
                             proxies={'http': proxy})
        else:
            r = requests.get(request_url,
                             headers=cls.HEADERS)
        try:
            r.raise_for_status()
        except HTTPError:
            print(traceback.format_exc())
            return list()
        else:
            html = r.text
        up_to_def_div: Failure = (
            Failure(html)
            >> cls.build_soup
            >> cls.find_def_div
            >> cls.delete_illustrations
        )
        # case 1: definitions are laid out in different sections.
        raws_case_1: Optional[List[str]] = (
                up_to_def_div
                >> cls.find_def_tags
                >> cls.collect_texts
        ).data
        if isinstance(raws_case_1, list) and len(raws_case_1) > 0:
            # if this did not fail, then return case 1
            return raws_case_1
        # case 2: definitions start with "may refer to:"
        raws_case_2: Optional[List[str]] = (
                up_to_def_div
                >> cls.find_mw_parser_div
                >> cls.find_ul
                >> cls.find_all_lists
                >> cls.collect_texts
        ).data
        if isinstance(raws_case_2, list) and len(raws_case_2) > 0:
            return raws_case_2

        # else, returns an empty list. There is no definitions
        return list()

    @classmethod
    def build_soup(cls, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')

    @classmethod
    def find_def_div(cls, soup: BeautifulSoup) -> Tag:
        return soup.find('div', attrs={'id': 'Definition'})

    @classmethod
    def delete_illustrations(cls, def_div: Tag) -> Tag:
        for illustration in def_div.find_all('span', attrs={"class": "illustration"}):
            illustration.decompose()
        return def_div

    @classmethod
    def find_def_tags(cls, def_div: Tag) -> List[Tag]:
        ds_singles = cls.find_ds_singles(def_div)
        ds_lists = cls.find_ds_lists(def_div)
        return ds_singles + ds_lists

    @classmethod
    def find_ds_singles(cls, def_div: Tag) -> List[Tag]:
        return def_div.find_all('div', attrs={'class': 'ds-single'})

    @classmethod
    def find_ds_lists(cls, def_div: Tag) -> List[Tag]:
        return def_div.find_all('div', attrs={'class': 'ds-list'})

    @classmethod
    def collect_texts(cls, tags: List[Tag]) -> List[str]:
        return [
            tag.get_text()
            for tag in tags
        ]

    # for case 2
    @classmethod
    def find_mw_parser_div(cls, def_div: Tag) -> Tag:
        return def_div.find('div', attrs={'class': 'mw-parser-output'})

    @classmethod
    def find_ul(cls, mw_parser_div: Tag) -> Tag:
        return mw_parser_div.find('ul')

    @classmethod
    def find_all_lists(cls, ul: Tag) -> List[Tag]:
        return ul.find_all('li')

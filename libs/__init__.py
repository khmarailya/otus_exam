import random
import string
from typing import Iterable, Iterator


class XHelper:

    @staticmethod
    def dummy(function):
        return function

    @staticmethod
    def parse_str_table(table_with_headers: str):
        list_table_rows = table_with_headers.split("\n")
        list_headers = str(list_table_rows[0]).strip("|").split("|")
        dict_table = {}
        for header in list_headers:
            header_text = header.strip()
            lst_row = []
            for i in range(1, list_table_rows.__len__()):
                list_temp = list_table_rows[i].strip("|").split("|")
                lst_row.append(list_temp[list_headers.index(header)].strip())

            dict_table[header_text] = lst_row

        return dict_table

    @staticmethod
    def iter(*args: Iterable):
        for i in args:
            yield from iter(i)

    @classmethod
    def random_string(cls, length=10):
        return "".join([random.choice(string.ascii_letters) for _ in range(length)])

    @staticmethod
    def random_phone():
        return "".join([random.choice(string.digits) for _ in range(10)])

    @classmethod
    def random_email(cls):
        return cls.random_string() + "@" + cls.random_string(5) + "." + random.choice(["com", "ua", "org", "ru"])


class Str:

    @classmethod
    def strip_split(cls, s: str, sep: str = None) -> Iterator[str]:
        yield from (s.strip() for s in s.split(sep=sep))

    @classmethod
    def strip_splits(cls, *s: str, sep: str = None) -> Iterator[Iterator[str]]:
        for s_ in s:
            yield cls.strip_split(s_, sep=sep)

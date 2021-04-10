from typing import List, Tuple, Union
import csv
import json


class Loader:

    def load(self, *params):
        raise NotImplementedError


class ApiKeyLoader(Loader):

    def load(self, key_path: str) -> str:
        """
        load a str key from local data.
        :return:
        """
        with open(key_path, 'r') as fh:
            return fh.read().strip()


class SlideIdiomsLoader(Loader):
    def load(self, tsv_path: str) -> List[str]:
        idioms = list()
        with open(tsv_path, 'r') as fh:
            tsv_reader = csv.reader(fh, delimiter="\t")
            # skip the header
            next(tsv_reader)  # skip the header
            for row in tsv_reader:
                idiom = row[0]
                idioms.append(idiom)
        return idioms


class TargetIdiomsLoader(Loader):
    def load(self, txt_path: str, norm: bool = False) -> List[str]:
        idioms = list()
        with open(txt_path, 'r') as fh:
            for line in fh:
                idiom = line.strip()
                if norm:
                    idioms.append(self.norm_case(idiom))
                else:
                    idioms.append(idiom)
        return idioms

    @staticmethod
    def norm_case(idiom: str) -> str:
        return idiom.lower() \
            .replace("i ", "I ") \
            .replace(" i ", " I ") \
            .replace("i'm", "I'm") \
            .replace("i'll", "I'll") \
            .replace("i\'d", "I'd")


class TsvTuplesLoader(Loader):
    """
    all of those with (str, json) tuples.
    """
    def load(self, tsv_path: str) -> List[Tuple[str, Union[list, dict]]]:
        rows = list()
        with open(tsv_path, 'r') as fh:
            tsv_reader = csv.reader(fh, delimiter="\t")
            for row in tsv_reader:
                idiom = row[0]
                # the second column is always json.
                raws = json.loads(row[1])
                rows.append((idiom, raws))
        return rows

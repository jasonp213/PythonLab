from abc import ABC, abstractmethod
from typing import IO


class EOF:
    pass


class Data(ABC):
    @abstractmethod
    def __getitem__(self, idx: int):
        raise NotImplementedError


class StringData(Data):
    def __init__(self, txt: str):
        self._txt = txt

    def __getitem__(self, idx: int):
        return EOF if idx < 0 or idx >= len(self._txt) else self._txt[idx]


class FileData(Data):
    def __init__(self, fp: IO):
        self._fp = fp

    def __getitem__(self, i: int):
        self._fp.seek(i, 0)
        char = self._fp.read(1)
        return EOF if char == "" else char

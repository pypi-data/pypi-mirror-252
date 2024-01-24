import io

from .block import Block, BlockType
from .captionsFormat import CaptionsFormat
from .microTime import MicroTime as MT
from bs4 import BeautifulSoup


EXTENSIONS = [".sami"]


@staticmethod
def detectSAMI(content: str | io.IOBase) -> bool:
    """
    Used to detect Synchronized Accessible Media Interchange caption format.

    It returns True if:
     - the first line starts with <SAMI>
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    if content.readline().lstrip().startswith("<SAMI>"):
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def readSAMI(self, content: str | io.IOBase, languages: list[str] = None, **kwargs):
    content = self.checkContent(content=content, **kwargs)
    languages = languages or [self.default_language]
    time_offset = kwargs.get("time_offset") or MT()
    raise ValueError("Not Implemented")


def saveSAMI(self, filename: str, languages: list[str] = None, **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.SAMI,
                                 languages=languages, **kwargs)
    encoding = kwargs.get("file_encoding") or "UTF-8"
    languages = languages or [self.default_language]
    if kwargs.get("no_styling"):
        generator = (((data.get(i) for i in languages), data) for data in self)
    else:
        generator = (((data.get_style(i).getUSF() for i in languages), data) for data in self)
    try:
        with open(filename, "w", encoding=encoding) as file:
            pass
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error {e}")
    raise ValueError("Not Implemented")


class SAMI(CaptionsFormat):
    """
    Synchronized Accessible Media Interchange

    Read more about it https://learn.microsoft.com/en-us/previous-versions/windows/desktop/dnacc/understanding-sami-1.0

    Example:

    with SAMI("path/to/file.sami") as sami:
        sami.saveSRT("file")
    """
    detect = staticmethod(detectSAMI)
    read = readSAMI
    save = saveSAMI

    from .lrc import saveLRC
    from .srt import saveSRT
    from .sub import saveSUB
    from .ttml import saveTTML
    from .usf import saveUSF
    from .vtt import saveVTT

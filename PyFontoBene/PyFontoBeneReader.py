from typing import Tuple


class PyFontoBeneReader:
    def __init__(self) -> None:
        self.file_name: str = None
        self.file = None
        self.line_text: str = None
        self.line_number: int = 0

    def open(self, file_name: str) -> None:
        self.file_name = file_name
        self.file = open(file_name, mode='r', encoding="UTF-8")

    def close(self) -> None:
        self.file.close()

    def readLine(self) -> bool:
        self.line_text = self.file.readline()
        self.line_number += 1
        if not self.line_text:
            return False
        self.line_text = self.line_text.strip()
        return True

    def parseKeyValue(self) -> Tuple[str, str]:
        import re
        tokens = re.findall(r'(\S+)[ ]*=[ ]*(.+)\Z', self.line_text)
        kv_pair: Tuple[str, str] = (tokens[0][0], tokens[0][1])
        return kv_pair

    def parseGlyph(self) -> int:
        import re
        tokens = re.findall(r'[\[]([0-9A-Z]+)[\]]', self.line_text)
        if not tokens:
            return 0
        # print(tokens[0])
        glyph_code: int = int(tokens[0], 16)
        return glyph_code

    def parseGlyphItemReference(self) -> int:
        import re
        tokens = re.findall(r'@([0-9A-Z]+)', self.line_text)
        if not tokens:
            return 0
        # print(tokens[0])
        glyph_code: int = int(tokens[0], 16)
        return glyph_code

    def parseGlyphItemSpacing(self) -> float:
        import re
        tokens = re.findall(r'~([.0-9]+)', self.line_text)
        if not tokens:
            return 0
        # print(tokens[0])
        spacing: float = float(tokens[0])
        return spacing

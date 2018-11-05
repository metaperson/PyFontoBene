class PyFontoBeneWriter:
    def __init__(self) -> None:
        self.file_name: str = None
        self.file = None

    def open(self, file_name: str) -> bool:
        self.file_name = file_name
        # self.file = open(file_name, mode='w', encoding="ascii")
        self.file = open(file_name, mode='w', encoding="UTF-8", newline="\n")
        if not self.file:
            return False
        return True

    def close(self) -> None:
        if self.file:
            self.file.close()

    def putComment(self, text: str) -> bool:
        if not self.file:
            return False
        self.file.write("#")
        self.file.write(text)
        self.file.write("\n")
        return True

    def putSection(self, text: str) -> bool:
        if not self.file:
            return False
        self.file.write("\n")
        self.file.write("[%s]" % text)
        self.file.write("\n")
        return True

    def putSectionBody(self) -> bool:
        if not self.file:
            return False
        self.file.write("\n")
        self.file.write("---")
        self.file.write("\n")
        return True

    @staticmethod
    def floatToStr(value: float):
        if value == 0.0:
            return "0"
        if value == int(value):
            value_str = str(int(value))
        else:
            value_str = str(value)
        if value_str[0] == "-":
            value_str = "-" + value_str[1:].lstrip("0")
        else:
            value_str = value_str.lstrip("0")
        return value_str


    def putKeyValue(self, key: str, value) -> bool:
        self.file.write(key)
        self.file.write(" = ")
        type_value = type(value)
        if type_value == str:
            self.file.write(value)
        elif type_value == float:
            self.file.write(__class__.floatToStr(value))
        else:
            self.file.write(str(value))
        self.file.write("\n")
        return True

    def putGlyph(self, code: int) -> bool:
        if not self.file:
            return False
        self.file.write("\n")
        self.file.write("[%04X] %c" % (code, code))
        self.file.write("\n")
        return True

    def putGlyphItemReference(self, code: int) -> bool:
        if not self.file:
            return False
        self.file.write("@%04X" % code)
        self.file.write("\n")
        return True

    def putGlyphItemSpacing(self, gap: float) -> bool:
        if not self.file:
            return False
        self.file.write("~")
        self.file.write(__class__.floatToStr(gap))
        self.file.write("\n")
        return True

    def putSegmentLine(self, x: float, y: float) -> bool:
        if not self.file:
            return False
        self.file.write(__class__.floatToStr(x))
        self.file.write(",")
        self.file.write(__class__.floatToStr(y))
        return True

    def putSegmentArc(self, x: float, y: float, bulge: float) -> bool:
        if not self.file:
            return False
        self.file.write(__class__.floatToStr(x))
        self.file.write(",")
        self.file.write(__class__.floatToStr(y))
        self.file.write(",")
        self.file.write(__class__.floatToStr(bulge))
        return True

    def putSegmentDelimiter(self) -> bool:
        if not self.file:
            return False
        self.file.write(";")
        return True

    def putCRLF(self) -> bool:
        self.file.write("\n")
        return True

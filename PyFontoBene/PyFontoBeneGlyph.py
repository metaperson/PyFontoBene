from typing import List
from PyFontoBeneGlyphItem import *
from PyFontoBeneReader import PyFontoBeneReader
from PyFontoBeneWriter import PyFontoBeneWriter


class PyFontoBeneGlyph:
    def __init__(self, *, code: int, items: List[PyFontoBeneGlyphItem]) -> None:
        self.code: int = code
        self.items: List[PyFontoBeneGlyphItem] = items

    def writeTo(self, writer: PyFontoBeneWriter) -> bool:
        writer.putGlyph(self.code)
        for item in self.items:
            item.writeTo(writer)
        return True

    @staticmethod
    def createFrom(reader: PyFontoBeneReader) -> 'PyFontoBeneGlyph':
        code = reader.parseGlyph()
        if code == 0:
            none_class: 'PyFontoBeneGlyph' = None
            return none_class

        items: List[PyFontoBeneGlyphItem] = list()
        while reader.readLine():
            if reader.line_text.strip() == "":
                break
            if reader.line_text[0] == "@":
                reference = PyFontoBeneGlyphItemReference.createFrom(reader)
                if reference is not None:
                    items.append(reference)
            elif reader.line_text[0] == "~":
                spacing = PyFontoBeneGlyphItemSpacing.createFrom(reader)
                if spacing is not None:
                    items.append(spacing)
            else:
                polyline = PyFontoBeneGlyphItemPolyline.createFrom(reader)
                if polyline is not None:
                    items.append(polyline)

        return __class__(code=code, items=items)


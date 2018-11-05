from typing import List, Tuple
from PyFontoBeneGeometry import *
from PyFontoBeneGlyph import *
from PyFontoBeneReader import PyFontoBeneReader
from PyFontoBeneWriter import PyFontoBeneWriter


class PyFontoBeneFont:
    def __init__(self, *, file_format: str, file_format_version: str, file_comments: List[str]
                 , font_name: str, font_id: str, font_version: str
                 , authors: List[str], licenses: List[str]
                 , letter_spacing: float, line_spacing: float
                 , user_attributes: List[Tuple[str, str]]
                 , glyphs: List[PyFontoBeneGlyph]):
        self.file_format: str = file_format
        self.file_format_version: str = file_format_version
        self.file_comments: List[str] = file_comments
        self.font_name: str = font_name
        self.font_id: str = font_id
        self.font_version: str = font_version
        self.authors: List[str] = authors
        self.licenses: List[str] = licenses
        self.letter_spacing: float = letter_spacing
        self.line_spacing: float = line_spacing
        self.user_attributes: List[Tuple[str, str]] = user_attributes
        self.glyphs: List[PyFontoBeneGlyph] = glyphs

    def writeToFile(self, file_name: str) -> bool:
        writer = PyFontoBeneWriter()
        if not writer.open(file_name):
            return False
        if not self.writeTo(writer):
            writer.close()
            return False
        writer.close()
        return True

    def writeTo(self, writer: PyFontoBeneWriter) -> bool:
        for comment_item in self.file_comments:
            writer.putComment(comment_item)

        writer.putSection("format")
        writer.putKeyValue("format", self.file_format)
        writer.putKeyValue("format_version", self.file_format_version)

        writer.putSection("font")
        writer.putKeyValue("name", self.font_name)
        writer.putKeyValue("id", self.font_id)
        writer.putKeyValue("version", self.font_version)
        for author_item in self.authors:
            writer.putKeyValue("author", author_item)
        for license_item in self.licenses:
            writer.putKeyValue("license", license_item)
        writer.putKeyValue("letter_spacing", self.letter_spacing)
        writer.putKeyValue("line_spacing", self.line_spacing)

        writer.putSectionBody()
        for glyph in self.glyphs:
            glyph.writeTo(writer)
        writer.putCRLF()
        return True

    @staticmethod
    def createFromFile(file_name: str) -> 'PyFontoBeneFont':
        reader = PyFontoBeneReader()
        reader.open(file_name)
        font = __class__.createFrom(reader)
        reader.close()
        return font

    @staticmethod
    def createFrom(reader: PyFontoBeneReader) -> 'PyFontoBeneFont':
        from enum import Enum, unique, auto

        @unique
        class FileSection(Enum):
            SOF = auto()
            HEADER_FORMAT = auto()
            HEADER_FONT = auto()
            HEADER_USER = auto()
            BODY = auto()
            EOF = auto()

        file_section: FileSection = FileSection.SOF

        file_comments: List[str] = list()
        authors: List[str] = list()
        licenses: List[str] = list()
        user_attributes: List[Tuple[str, str]] = list()
        glyphs: List[PyFontoBeneGlyph] = list()

        while reader.readLine():
            if reader.line_text.strip() == "":
                continue
            if reader.line_text[0] == "#":
                file_comments.append(reader.line_text[1:])
                continue

            if reader.line_text == "[format]":
                file_section = FileSection.HEADER_FORMAT
                continue
            elif reader.line_text == "[font]":
                file_section = FileSection.HEADER_FONT
                continue
            elif reader.line_text == "[user]":
                file_section = FileSection.HEADER_USER
                continue
            elif reader.line_text == "---":
                file_section = FileSection.BODY
                continue

            if file_section == FileSection.SOF:
                #print(parser.line_text, end="")
                pass
            elif file_section == FileSection.HEADER_FORMAT:
                #print(parser.line_text, end="")
                kv_pair = reader.parseKeyValue()
                key = kv_pair[0]
                value = kv_pair[1]
                if key == "format":
                    file_format = value
                elif key == "format_version":
                    file_format_version = value
                #print(key, value)
            elif file_section == FileSection.HEADER_FONT:
                #print(parser.line_text, end="")
                kv_pair = reader.parseKeyValue()
                key = kv_pair[0]
                value = kv_pair[1]
                if key == "name":
                    font_name = value
                elif key == "id":
                    font_id = value
                elif key == "version":
                    font_version = value
                elif key == "author":
                    authors.append(value)
                elif key == "license":
                    licenses.append(value)
                elif key == "letter_spacing":
                    letter_spacing = float(value)
                elif key == "line_spacing":
                    line_spacing = float(value)
                # print(key, value)
            elif file_section == FileSection.HEADER_USER:
                kv_pair = reader.parseKeyValue()
                user_attributes.append(kv_pair)
            elif file_section == FileSection.BODY:
                glyph = PyFontoBeneGlyph.createFrom(reader)
                if glyph is not None:
                    glyphs.append(glyph)
            #print(parser_state)
            # print(parser.line_text)
        return __class__(file_format=file_format, file_format_version=file_format_version, file_comments=file_comments
                         , font_name=font_name, font_id=font_id, font_version=font_version
                         , authors=authors, licenses=licenses
                         , letter_spacing=letter_spacing, line_spacing=line_spacing, user_attributes=user_attributes
                         , glyphs=glyphs)

    def findGylph(self, char_code: int) -> PyFontoBeneGlyph:
        for glyph in self.glyphs:
            if char_code == glyph.code:
                return glyph
        none_return: PyFontoBeneGlyph = None
        return none_return

    def stringToGylphList(self, text: str) -> List[PyFontoBeneGlyph]:
        glyphs: List[PyFontoBeneGlyph] = list()
        for char in text:
            glyph = self.findGylph(char_code=ord(char))
            glyphs.append(glyph)
        return glyphs

    def getGlyphBoxSpan(self, glyph: PyFontoBeneGlyph) -> (float, float, float, float):
        x_min: float = 0.0
        x_max: float = 0.0
        y_min: float = 0.0
        y_max: float = 0.0

        for item in glyph.items:
            item_type = type(item)
            if item_type is PyFontoBeneGlyphItemPolyline:
                polyline: PyFontoBeneGlyphItemPolyline = item
                for segment in polyline.segments:
                    if x_min > segment.x:
                        x_min = segment.x
                    if x_max < segment.x:
                        x_max = segment.x
                    if y_min > segment.y:
                        y_min = segment.y
                    if y_max < segment.y:
                        y_max = segment.y
            elif item_type is PyFontoBeneGlyphItemSpacing:
                spacing: PyFontoBeneGlyphItemSpacing = item
                if x_min > spacing.gap:
                    x_min = spacing.gap
                if x_max < spacing.gap:
                    x_max = spacing.gap
            elif item_type is PyFontoBeneGlyphItemReference:
                reference: PyFontoBeneGlyphItemReference = item
                ref_glyph = self.findGylph(reference.code)
                if ref_glyph is not None:
                    glyph_x_min, glyph_y_min, glyph_x_max, glyph_y_max = self.getGlyphBoxSpan(glyph)
                    if x_min > glyph_x_min:
                        x_min = glyph_x_min
                    if x_max < glyph_x_max:
                        x_max = glyph_x_max
                    if y_min > glyph_y_min:
                        y_min = glyph_y_min
                    if y_max < glyph_y_max:
                        y_max = glyph_y_max



        return x_min, y_min, x_max, y_max

    def getStringBoxSpan(self, text: str) -> (float, float, float, float):
        glyphs: List[PyFontoBeneGlyph] = self.stringToGylphList(text)

        spacing: bool = False
        x_min: float = 0.0
        x_max: float = 0.0
        y_min: float = 0.0
        y_max: float = 0.0

        for glyph in glyphs:
            glyph_x_min, glyph_y_min, glyph_x_max, glyph_y_max = self.getGlyphBoxSpan(glyph)
            if spacing:
                glyph_x_min += x_max + self.letter_spacing
                glyph_x_max += x_max + self.letter_spacing
            else:
                glyph_x_min += x_max
                glyph_x_max += x_max
                spacing = True

            if x_min > glyph_x_min:
                x_min = glyph_x_min
            if x_max < glyph_x_max:
                x_max = glyph_x_max
            if y_min > glyph_y_min:
                y_min = glyph_y_min
            if y_max < glyph_y_max:
                y_max = glyph_y_max

        return x_min, y_min, x_max, y_max

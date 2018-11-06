from typing import List
from PyFontoBeneReader import PyFontoBeneReader
from PyFontoBeneWriter import PyFontoBeneWriter


class PyFontoBeneGlyph:
    class GlyphItem:
        def __init__(self) -> None:
            pass

        def writeTo(self, writer: PyFontoBeneWriter) -> bool:
            raise NotImplementedError

    class GlyphItemReference(GlyphItem):
        def __init__(self, *, code: int) -> None:
            super(__class__, self).__init__()
            self.code = code

        def writeTo(self, writer: PyFontoBeneWriter) -> bool:
            writer.putGlyphItemReference(self.code)
            return True

        @staticmethod
        def createFrom(reader: PyFontoBeneReader) -> 'PyFontoBeneGlyph.GlyphItemReference':
            code = reader.parseGlyphItemReference()
            return __class__(code=code)

    class GlyphItemSpacing(GlyphItem):
        def __init__(self, *, gap: float) -> None:
            super(__class__, self).__init__()
            self.gap = gap

        def writeTo(self, writer: PyFontoBeneWriter) -> bool:
            writer.putGlyphItemSpacing(self.gap)
            return True

        @staticmethod
        def createFrom(reader: PyFontoBeneReader) -> 'PyFontoBeneGlyph.GlyphItemSpacing':
            gap = reader.parseGlyphItemSpacing()
            return __class__(gap=gap)

    class GlyphItemPolyline(GlyphItem):
        def __init__(self, *, segments: List['PyFontoBeneGlyph.GlyphItemPolyline.Segment']) -> None:
            super(__class__, self).__init__()
            self.segments: List['PyFontoBeneGlyph.GlyphItemPolyline.Segment'] = segments

        class Segment:
            def __init__(self, *, x: float, y: float) -> None:
                self.x: float = x
                self.y: float = y

            def writeTo(self, writer: PyFontoBeneWriter) -> bool:
                raise NotImplementedError

        class SegmentLine(Segment):
            def __init__(self, *, x: float, y: float) -> None:
                super(__class__, self).__init__(x=x, y=y)

            def writeTo(self, writer: PyFontoBeneWriter) -> bool:
                writer.putSegmentLine(x=self.x, y=self.y)
                return True

        class SegmentArc(Segment):
            def __init__(self, *, x: float, y: float, bulge: float) -> None:
                super(__class__, self).__init__(x=x, y=y)
                self.bulge: float = bulge

            def writeTo(self, writer: PyFontoBeneWriter) -> bool:
                writer.putSegmentArc(x=self.x, y=self.y, bulge=self.bulge)
                return True

        def writeTo(self, writer: PyFontoBeneWriter) -> bool:
            index: int = 0
            for segment in self.segments:
                if index:
                    writer.putSegmentDelimiter()
                segment.writeTo(writer)
                index += 1
            writer.putCRLF()
            return True

        @staticmethod
        def createFrom(reader: PyFontoBeneReader) -> 'PyFontoBeneGlyph.GlyphItemPolyline':
            segments: List['PyFontoBeneGlyph.GlyphItemPolyline.Segment'] = list()

            segment_texts = reader.line_text.split(";")
            # print(segment_texts)
            for segment_text in segment_texts:
                coord_texts = segment_text.split(",")
                if len(coord_texts) == 2:
                    x = float(coord_texts[0])
                    y = float(coord_texts[1])
                    line = __class__.SegmentLine(x=x, y=y)
                    segments.append(line)
                elif len(coord_texts) == 3:
                    x = float(coord_texts[0])
                    y = float(coord_texts[1])
                    bulge = float(coord_texts[2])
                    arc = __class__.SegmentArc(x=x, y=y, bulge=bulge)
                    segments.append(arc)
            return __class__(segments=segments)

    def __init__(self, *, code: int, items: List['PyFontoBeneGlyph.GlyphItem']) -> None:
        self.code: int = code
        self.items: List['PyFontoBeneGlyph.GlyphItem'] = items

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

        items: List[__class__.GlyphItem] = list()
        while reader.readLine():
            if reader.line_text.strip() == "":
                break
            if reader.line_text[0] == "@":
                reference = __class__.GlyphItemReference.createFrom(reader)
                if reference is not None:
                    items.append(reference)
            elif reader.line_text[0] == "~":
                spacing = __class__.GlyphItemSpacing.createFrom(reader)
                if spacing is not None:
                    items.append(spacing)
            else:
                polyline = __class__.GlyphItemPolyline.createFrom(reader)
                if polyline is not None:
                    items.append(polyline)

        return __class__(code=code, items=items)


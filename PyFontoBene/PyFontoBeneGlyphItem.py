from typing import List
from abc import abstractmethod
from PyFontoBeneReader import PyFontoBeneReader
from PyFontoBeneWriter import PyFontoBeneWriter


class PyFontoBeneGlyphItem:
    def __init__(self):
        pass

    @abstractmethod
    def writeTo(self, writer: PyFontoBeneWriter) -> bool:
        raise NotImplementedError


class PyFontoBeneGlyphItemReference(PyFontoBeneGlyphItem):
    def __init__(self, *, code: int) -> None:
        super(__class__, self).__init__()
        self.code = code

    def writeTo(self, writer: PyFontoBeneWriter) -> bool:
        writer.putGlyphItemReference(self.code)
        return True

    @staticmethod
    def createFrom(reader: PyFontoBeneReader) -> 'PyFontoBeneGlyphItemReference':
        code = reader.parseGlyphItemReference()
        return __class__(code=code)


class PyFontoBeneGlyphItemSpacing(PyFontoBeneGlyphItem):
    def __init__(self, *, gap: float) -> None:
        super(__class__, self).__init__()
        self.gap = gap

    def writeTo(self, writer: PyFontoBeneWriter) -> bool:
        writer.putGlyphItemSpacing(self.gap)
        return True

    @staticmethod
    def createFrom(reader: PyFontoBeneReader) -> 'PyFontoBeneGlyphItemSpacing':
        gap = reader.parseGlyphItemSpacing()
        return __class__(gap=gap)


class PyFontoBeneGlyphItemPolyline(PyFontoBeneGlyphItem):
    def __init__(self, *, segments: List['PyFontoBeneGlyphItemPolyline.Segment']) -> None:
        super(__class__, self).__init__()
        self.segments: List['PyFontoBeneGlyphItemPolyline.Segment'] = segments

    class Segment:
        def __init__(self, *, x: float, y: float) -> None:
            self.x: float = x
            self.y: float = y

        @abstractmethod
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
    def createFrom(reader: PyFontoBeneReader) -> 'PyFontoBeneGlyphItemPolyline':
        segments: List['PyFontoBeneGlyphItemPolyline.Segment'] = list()

        segment_texts = reader.line_text.split(";")
        # print(segment_texts)
        for segment_text in segment_texts:
            coord_texts = segment_text.split(",")
            if len(coord_texts) == 2:
                x = float(coord_texts[0])
                y = float(coord_texts[1])
                line = PyFontoBeneGlyphItemPolyline.SegmentLine(x=x, y=y)
                segments.append(line)
            elif len(coord_texts) == 3:
                x = float(coord_texts[0])
                y = float(coord_texts[1])
                bulge = float(coord_texts[2])
                arc = PyFontoBeneGlyphItemPolyline.SegmentArc(x=x, y=y, bulge=bulge)
                segments.append(arc)
        return __class__(segments=segments)

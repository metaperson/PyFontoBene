from tkinter import Canvas, Label, Button
from PyFontoBeneGeometry import *
from PyFontoBeneFont import PyFontoBeneFont
from PyFontoBeneGlyph import PyFontoBeneGlyph
from PyFontoBeneGlyphItem import *


class PyFontoBeneTk:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.font_canvas = Canvas(master)
        self.font_canvas.pack()

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def drawText(self, font: PyFontoBeneFont
                 , x: float, y: float, ratio_x: float, ratio_y: float
                 , text: str):
        self.font_canvas.create_line(x - ratio_x, y, x + ratio_x, y)
        self.font_canvas.create_line(x, y - ratio_y, x, y + ratio_y)

        x1, y1, x2, y2 = font.getStringBoxSpan(text)
        self.font_canvas.create_rectangle(x + (x1 * ratio_x)
                                          , y - (y1 * ratio_y)
                                          , x + (x2 * ratio_x)
                                          , y - (y2 * ratio_y))

        glyphs = font.stringToGylphList(text)
        cursor: float = x
        for glyph in glyphs:
            if glyph is not None:
                x1, y1, x2, y2 = font.getGlyphBoxSpan(glyph)
                self.font_canvas.create_rectangle(cursor + (x1 * ratio_x)
                                                  , y - (y1 * ratio_y)
                                                  , cursor + (x2 * ratio_x)
                                                  , y - (y2 * ratio_y))

                cursor_advance = self.drawGlyph(font=font
                                                , x=cursor, y=y, ratio_x=ratio_x, ratio_y=ratio_y, glyph=glyph)
                cursor += cursor_advance
            cursor += font.letter_spacing * ratio_x

    def drawGlyph(self, font: PyFontoBeneFont
                  , x: float, y: float, ratio_x: float, ratio_y: float
                  , glyph: PyFontoBeneGlyph) -> float:
        # self.font_canvas.create_line(0, 0, 100, 100)
        cursor_advance: float = 0.0
        for item in glyph.items:
            item_type = type(item)
            if item_type is PyFontoBeneGlyphItemPolyline:
                polyline: PyFontoBeneGlyphItemPolyline = item
                points: tuple = tuple()
                for segment in polyline.segments:
                    cx = segment.x * ratio_x
                    if cursor_advance < cx:
                        cursor_advance = cx
                    px = x + cx
                    py = y - segment.y * ratio_y
                    points = points + (px, py)
                #print(points)
                self.font_canvas.create_line(points)
            elif item_type is PyFontoBeneGlyphItemSpacing:
                spacing: PyFontoBeneGlyphItemSpacing = item
                cx = spacing.gap * ratio_x
                if cursor_advance < cx:
                    cursor_advance = cx
            elif item_type is PyFontoBeneGlyphItemReference:
                reference: PyFontoBeneGlyphItemReference = item
                ref_glyph = font.findGylph(reference.code)
                if ref_glyph is not None:
                    cx = self.drawGlyph(font=font, x=x, y=y, ratio_x=ratio_x, ratio_y=ratio_y, glyph=ref_glyph)
                    if cursor_advance < cx:
                        cursor_advance = cx
        return cursor_advance








    def greet(self):
        print("Greetings!")


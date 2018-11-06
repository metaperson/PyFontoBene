def FontoBeneTest():
    from PyFontoBeneFont import PyFontoBeneFont
    from tkinter import Tk, Canvas, Button

    # read and parse the font file.
    font = PyFontoBeneFont.createFromFile("newstroke.bene")

    # store font file again for checking parsing the font collectly.
    font.writeToFile("newstroke.bene.bak")

    # create test tk dialog.
    root = Tk()
    root.title("FontoBene Drawing Test")

    # pack a canvas to drawing font texts.
    font_canvas = Canvas(root, width=1300, height=800)
    font_canvas.pack()

    # pack the close button.
    close_button = Button(root, text="Close", command=root.quit)
    close_button.pack()

    # drawing test for one code character.
    font.drawCode(font_canvas, x=10, y=30, ratio_x=3, ratio_y=3, char_code=ord("@"))

    # drawing test for text string.
    font.drawText(font_canvas, x=50, y=30, ratio_x=2, ratio_y=2, text="Hello World!!!")

    # drawing test for glyph in the font.
    font.drawText(font_canvas, x=300, y=30, ratio_x=2, ratio_y=2, text="count of glyph : %d" % len(font.glyphs))
    col: int = 0
    row: int = 0
    for glyph in font.glyphs:
        font.drawGlyph(font_canvas, x=col * 25 + 10, y=row * 25 + 70, ratio_x=2, ratio_y=2, glyph=glyph)
        if col < 50:
            col += 1
        else:
            col = 0
            row += 1
    root.mainloop()


if __name__ == "__main__":
    import os
    import sys

    current_path = os.path.dirname(__file__)
    # sys.path.append(current_path + "\Libs")
    # print(sys.path)
    FontoBeneTest()
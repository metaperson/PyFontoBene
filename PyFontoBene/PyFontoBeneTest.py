def FontText():
    from PIL import ImageFont, ImageDraw
    #draw = ImageDraw.Draw("ff.png")
    # use a bitmap font
    #font = ImageFont.load("arial.pil")
    #draw.text((10, 10), "hello", font=font)
    # use a truetype font
    font = ImageFont.truetype("arial.ttf", 15)
    #draw.text((10, 25), "world", font=font)
    print(font.getsize("123123123"))

def FontoBeneTest():
    from PyFontoBeneFont import PyFontoBeneFont
    from PyFontoBeneTk import PyFontoBeneTk
    from tkinter import Tk
    font = PyFontoBeneFont.createFromFile(".\\Libs\\newstroke.bene")
    font.writeToFile(".\\Libs\\newstroke.bene.bak")
    font.letter_spacing = 4.28

    root = Tk()
    #text_string = "HHHHHHHHHH"
    text_string = "IIIIIIIIII"
    my_gui = PyFontoBeneTk(root)
    my_gui.drawText(font=font, x=20, y=150, ratio_x=5, ratio_y=5, text=text_string)
    # args = (10, 10, 10, 20, 20, 20, 20, 30)
    # my_gui.font_canvas.create_line(*args)
    root.mainloop()


if __name__ == "__main__":
    import os
    import sys

    current_path = os.path.dirname(__file__)
    sys.path.append(current_path + "\Libs")
    # print(sys.path)

    # FontText()
    FontoBeneTest()
#from PIL import Image
#import Image, ImageDraw
import os

WIDTH = 512
LEFT_MARGIN = 30
SAFE_WIDTH = WIDTH - LEFT_MARGIN
#im = Image.new("RGB", (WIDTH, 512), "white")
#darw = ImageDraw.Draw(im)

data = {
        "koe1": [(10.2, 1), (12.3, 0), (20.5, 1), (50, 0), (60, 1)],
        "koe2": [(15.2, 1), (17.3, 0), (20.5, 1), (30, 0), (59, 1)],
        }

def draw_line_with_margin(sx, ex, y):
    sx += LEFT_MARGIN
    print "(" + str(sx) + "," + str(y) + ")x(" + str(ex) + "," + str(y) + ")"
    #draw.line((sx, 10, ex, 10), fill=128)

def draw_function(name, values, y):
    # use a truetype font
    font_size = 15
    #font = ImageFont.truetype("arial.ttf", 15)
    #draw.text((5, y + font_size/2), "world", font=font)
    print name + "(5, " + str(y + font_size/2) + ")"

    sx = 0
    ex = SAFE_WIDTH
    start = 1
    for i in values:
        if start == 1:
            if i[1]:
                sx = i[0]
                ex = WIDTH
            else:
                sx = i[0]
                ex = i[0]
            start = 0
            continue
        else:
            if i[1]:
                sx = i[0]
            else:
                ex = i[0]
            draw_line_with_margin(sx, ex, y)
            start = 1
    if start == 0:
        #draw.line((sx, 10, ex, 10), fill=128)
        print "(" + str(sx) + "," + str(y) + ")x(" + str(ex) + "," + str(y) + ")"
        

def main():
    y = 10
    for key, values in data.items():
        draw_function(key, values, y)
        y += 20

    #im.save(sys.stdout, "PNG")

if __name__ == "__main__":
    main()


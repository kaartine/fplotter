#from PIL import Image
import Image, ImageDraw, ImageFont
import os, sys
import re

if len(sys.argv) != 3:
    print 'usage: fplotter <trace_file.txt> <output_file.png> \n'
    sys.exit(1)

WIDTH = 512
LEFT_MARGIN = 30
SAFE_WIDTH = WIDTH - LEFT_MARGIN
PERF_TRACE = '(.*)(perf)(.*)'
im = 0
draw = 0

data = {
        "koe1": [(10.2, 1), (12.3, 0), (20.5, 1), (50, 0), (60, 1)],
        "koe2": [(15.2, 1), (17.3, 0), (20.5, 1), (30, 0), (59, 1)],
        }

def draw_line_with_margin(sx, ex, y):
    sx += LEFT_MARGIN
    ex += LEFT_MARGIN
    print "(" + str(sx) + "," + str(y) + ")x(" + str(ex) + "," + str(y) + ")"
    draw.line((sx, y, ex, y), fill=128)

def draw_function(name, values, y):
    # use a truetype font
    font_size = 15
    #font = ImageFont.truetype("Helvetica.ttf", 15)
    #font = ImageFont.load("Helvetica.ttf")
    #draw.text((5, y + font_size/2), name, font=font)
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
        draw_line_with_margin(sx, ex, y)
        print "(" + str(sx) + "," + str(y) + ")x(" + str(ex) + "," + str(y) + ")"

def parse_file(file_name):
    global WIDTH
    for line in open(file_name):
        if re.match(PERF_TRACE, line):
            words = line.split(' ')
            i = 0
            for word in words:
                if re.match('[0-9]*.[0-9]*:', word):
                    break
                i += 1
            time = float(words[i].split(':')[0])
            print time
            if WIDTH < time:
                WIDTH = int(time) + 10
            f = words[i+1].split('_')
            fname = f[1]
            print fname
            on = int(f[2][0])
            print on

            if not data.has_key(fname):
                data[fname] = []
            data[fname].append( (time, on) )
            print data

def main(in_file, out_file):
    global im
    global draw
    parse_file(in_file)
    y = 10
    im = Image.new("RGB", (WIDTH, 512), "white")
    draw = ImageDraw.Draw(im)

    for key, values in data.items():
        draw_function(key, values, y)
        y += 20

    f = open(out_file, 'w+')
    im.save(f, "PNG")
    f.close
    print "Width " + str(WIDTH)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))


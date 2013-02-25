#from PIL import Image
#import Image, ImageDraw, ImageFont
import os, sys
import re
from svg import Scene, Text, Line

if len(sys.argv) != 3:
    print 'usage: fplotter <trace_file.txt> <output_file.png> \n'
    sys.exit(1)

LEFT_MARGIN = 200
RIGHT_MARGIN = 100
WIDTH = 512
HEIGHT = 512
TRACE_SEPARATOR = 40
SAFE_WIDTH = WIDTH - RIGHT_MARGIN - LEFT_MARGIN
PERF_TRACE = '(.*)(perf)(.*)'
im = 0
draw = 0
scene = 0

data = {
        #"koe1": [(10.2, 1), (12.3, 0), (20.5, 1), (50, 0), (60, 1)],
        #"koe2": [(15.2, 1), (17.3, 0), (20.5, 1), (30, 0), (59, 1)],
        }

def draw_line_with_margin(sx, ex, y, updown, time):
    if ex == -1 or sx == -1:
        print ex
        print sx
        sys.exit(0)
    sx += LEFT_MARGIN
    ex += LEFT_MARGIN
    print "(" + str(sx) + "," + str(y) + ")x(" + str(ex) + "," + str(y) + ") time: " + str(time)
    #draw.line((sx, y, ex, y), fill=128)
    #draw.line((sx, y+1, ex, y+1), fill=128)
    #draw.line((sx, y-1, ex, y-1), fill=128)
    scene.add(Line((sx, y),(ex, y)))

    #draw.line((ex, y - TRACE_SEPARATOR/2-10, ex, y+TRACE_SEPARATOR/2-10), fill=100)
    scene.add(Line((ex, y - TRACE_SEPARATOR/4), (ex, y+TRACE_SEPARATOR/4) ))
    #font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/arial.ttf", 8)
    if updown:
        y += -8
    else: 
        y += 8
    #draw.text((ex+1, y), str(time)[0:8], font=font)
    scene.add(Text((ex, y), str(time)[0:10] + "ms", 10))

def draw_function(name, values, y):
    # use a truetype font
    font_size = 10
    #font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/arial.ttf", font_size)
    #draw.text((5, y - font_size/2), name, font=font)
    scene.add(Text((5, y - font_size/2), name, font_size))
    print name + "(5, " + str(y + font_size/2) + ")"

    #print values
    i = 0
    time_diff = 0
    updown = True
    sx = -1
    ex = -1
    init = 0
    time_diff = 0.0
    last_on = 0
    orig_ts = 0
    orig_te = 0
    clear = 0
    while i < len(values):
        time_s = values[i][0]
        if i == 0 or clear:
            orig_ts = values[i][2]
            orig_te = 0.0
        time_e = WIDTH
        on_s = values[i][1]
        on_e = 0
        sx = time_s
        ex = WIDTH

        if i+1 < len(values):
            on_e = values[i+1][1]
            if on_e == 0:
                time_e = values[i+1][0]
                orig_te = values[i+1][2]
                ex = time_e

            if on_s == 1 and on_e == 0:
                time_diff = orig_te - orig_ts
                clear = 1
            i += 1
        i += 1

        if sx > ex:
            print "ERROR start time > end time"
            print sx
            print ex
            sys.exit()


        time_diff = time_diff * 1000
        draw_line_with_margin(sx, ex, y, updown, time_diff)
        updown = not updown

        #draw.line((sx, 10, ex, 10), fill=128)
        #draw_line_with_margin(sx, ex, y)
        #print "(" + str(sx) + "," + str(y) + ")x(" + str(ex) + "," + str(y) + ")"

def parse_file(file_name):
    global WIDTH
    min_time = 9999999.0
    for line in open(file_name):
        if re.match(PERF_TRACE, line):
            words = line.split(' ')
            i = 0
            for word in words:
                if re.match('[0-9]*.[0-9]*:', word):
                    break
                i += 1
            time_orig = float(words[i].split(':')[0])
            time = time_orig * 1000.0
            if min_time > time:
                min_time = time
                print "min_time " + str(min_time)
            #time = int((time - min_time) * 100.0)
            time -= min_time
            #time *= 1000
            print "time: " + str(time) + " time_orig: " + str(time_orig)

            if WIDTH < time + RIGHT_MARGIN:
                WIDTH = time + RIGHT_MARGIN
                print "update widht: " + str(WIDTH)

            f = words[i+2].split('_')
            fname = f[1]
            if len(f) > 3:
                fname = "_".join(f[1:len(f)-1])

            on = int(f[len(f)-1][0])
            print on

            print fname
            if not data.has_key(fname):
                data[fname] = []
            diff = time_orig
            data[fname].append( (time, on, diff) )

    print data

def main(in_file, out_file):
    #global im
    #global draw
    global scene
    parse_file(in_file)
    y = 20
    #im = Image.new("RGB", (WIDTH, HEIGHT), "black")
    #draw = ImageDraw.Draw(im)
    scene = Scene('fplot', HEIGHT, WIDTH)

    for key, values in data.items():
        draw_function(key, values, y)
        y += TRACE_SEPARATOR

    #f = open(out_file, 'w+')
    #im.save(f, "PNG")
    #f.close
    #print "Width " + str(WIDTH)
    scene.write_svg()
    #scene.display()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))


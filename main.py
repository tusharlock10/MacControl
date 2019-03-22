import osascript as AS
import os
from fire import Fire
from tj import color_text as ct

error = None
warn = None


def clr(num, warn=None):
    color="BLUE"
    if warn:
        color="GREEN"
    return ct(str(num), text_color=color, bold=True)


def get_num(num):
    global error, warn
    n = num
    try:
        num = float(num)
    except ValueError:
        error = "Enter only a number (+ve number, can be a decimal also)\nYou entered - %s" % clr(num)
        return None

    if num < 0:
        error = "Enter only a +ve integer or decimal number\nYou entered - %s" % clr(num)
        return None
    if 0.0 <= num <= 1.0:
        pass
    elif 0.0 <= num <= 100.0:
        num = num/100
    else:
        num = 1.0
        warn = "Number should only be between 0-1 or 0-100\nYou entered - %s , so I took it as 1" % clr(n,1)
    return num


def vol(vol):
    AS.osascript("set volume output volume %s" % vol)


def keyboard(num):
    n = get_num(num)
    if n:
        os.system("./kb %s" % n)


def brightness(num=None):
    if num:
        n = get_num(num)
        if n:
            if n<0.06:
                n=0.000001
                choice = input('This will turn off the display, are you sure (Y/N): ').lower()
                if choice not in ['y','yes']:
                    print('Aborting...')
                    return None
            os.system("./db %s" % n)
    
    else:
        os.system("./db")
        print()

def backlight(num=None):
    brightness(num)
    print()




if __name__ == '__main__':
    Fire()
    if error:
        print(ct(" * ERROR * ", text_color="RED",
                 background_color="WHITE", bold=True)+" | "+error)

    elif warn:
        print(ct(" * WARNING * ", text_color="YELLOW",
                 background_color="GREEN", bold=True)+" | "+warn)

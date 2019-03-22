import osascript as AS
import os
from fire import Fire
from tj import color_text as ct
import subprocess

error = None
warn = None


def clr(num, warn=None):
    color = "BLUE"
    if warn:
        color = "GREEN"
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
        error = "Enter only a +ve integer or decimal number\nYou entered - %s" % clr(
            num)
        return None
    if 0.0 <= num <= 1.0:
        pass
    elif 0.0 <= num <= 100.0:
        num = num/100
    else:
        num = 1.0
        warn = "Number should only be between 0-1 or 0-100\nYou entered - %s , so I took it as 1" % clr(
            n, 1)
    return num


def volume(arg='output', vol=None):
    global error, warn
    arg=arg.lower()
    if arg in ['mute', 'muted', 'unmute']:
        vol=1


    if vol:
        vol = get_num(vol)
        if 0.0 < vol < 1.0:
            vol = round(vol*100, None)

        
        if arg in ['s','speaker','speakers','output','o']:
            arg='output volume %s' % vol
        elif arg in ['i', 'mic','microphone','mics','microphones', 'input', 'i']:
            arg='input volume %s' % vol
        elif arg in ['a', 'alert','notify', 'notification']:
            arg='alert volume %s' % vol
        elif arg in ['mute', 'muted']:
            arg="output muted true"
        elif arg in ['unmute']:
            arg="output muted false"
        else:
            arg='output volume %s' % vol
            warn="Enter available options to control volume are\n * speaker\n * mic\n * alert\n\
mute or unmute\neg. control volume mute\neg. control volume mic 20"

        cmd = "osascript -e 'set volume %s'" % arg
        os.system(cmd)
        print(ct('SPEAKER VOLUME is now set to %s' %
                 vol, text_color='OLIVE', bold=1))

    else:
        cmd = "osascript -e 'get volume settings'"
        process = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        output = process.stdout.decode().strip('\n').split(', ')
        o = [i.split(':')[1] for i in output]

        x = ''
        if o[3] == 'true':
            x = ' but speakers are ' + \
                ct('* MUTED *', text_color='GREEN', bold=1)

        print(ct('SPEAKER VOLUME | %s' %
                 o[0]+' %', text_color='OLIVE', bold=1)+x)
        print(ct('  MIC VOLUME   | %s' %
                 o[1]+' %', text_color='YELLOW', bold=1))
        print(ct(' ALERT VOLUME  | %s' % o[2]+' %', text_color='BLUE', bold=1))


def keyboard(num):
    n = get_num(num)
    if n:
        os.system("./kb %s" % n)


def brightness(num=None):
    if num:
        n = get_num(num)
        if n:
            if n < 0.06:
                n = 0.000001
                choice = input(
                    'This will turn off the display, are you sure (Y/N): ').lower()
                if choice not in ['y', 'yes']:
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

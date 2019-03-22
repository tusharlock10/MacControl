import osascript as AS
import os
from fire import Fire
from tj import color_text

error = None


def vol(vol):
    AS.osascript("set volume output volume %s" % vol)


def keyboard(num):
    try:
        float(num)
    except ValueError:
        error
    if 0 <= float(num) <= 1:

    os.system("./db %s" % num)


if __name__ == '__main__':
    Fire()

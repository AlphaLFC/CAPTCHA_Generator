# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 17:41:55 2016

@author: alpha
"""

import random
import string
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from listutils import flattern


default_fontpath = '/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf'


def randRGBcolor():
    R = random.randrange(256)
    noR = 255 - R
    if noR == 0:
        G = 0
        B = 0
    else:
        G = random.randrange(noR)
        B = 255 - G
    return (R, G, B)


def randFONTcolor():
    return tuple(random.sample(range(0, 64, 4), 3))


def bgImg(mode='RGBA', size=(30, 30),
          color=(255, 255, 255), randcolor=True, transparent=255,
          draw_points=True, npoints='auto', point_color='rand',
          draw_lines=True, nlines='auto',
          line_color='rand', line_width=2,
          fill_images=False, fill_image_path='',
          BLUR=True, EDGE_ENHANCE=False, filter_rand=True):
    u'''创建背景图片!
    '''
    def randbgcolor():
        if mode == 'RGBA':
            return tuple(random.sample(range(191, 256, 4), 3) + [transparent])
        elif mode == 'RGB':
            return tuple(random.sample(range(191, 256, 4), 3))

    def randpointcolor():
        return tuple(random.sample(range(0, 256, 4), 3))

    if randcolor:
        color = randbgcolor()
    else:
        color = tuple(list(color) + [transparent])
    image = Image.new(mode=mode, size=size, color=color)
    draw = ImageDraw.Draw(image)
    if draw_points:
        if npoints == 'auto':
            npoints = long(round(size[0]/5.0) * round(size[1]/5.0))
        else:
            assert type(npoints) in [int, long], 'Watch input!'
        for _ in xrange(random.randint(0, npoints)):
            xpos = random.randrange(size[0])
            ypos = random.randrange(size[1])
            position = [(i, j) for i in range(xpos-random.randint(0, 1),
                                              xpos+random.randint(0, 2))
                        for j in range(ypos-random.randint(0, 1),
                                       ypos+random.randint(0, 2))
                        if 0 <= i < size[0] and 0 <= j <= size[1]]
            if point_color == 'rand':
                draw.point(position, fill=randpointcolor())
            else:
                assert type(point_color) == tuple and len(point_color) == 3
                draw.point(position, fill=point_color)
    if draw_lines:
        if nlines == 'auto':
            nlines = long(round(max(size)/10.0))
        else:
            assert type(nlines) in [int, long], 'Watch input!'
        for _ in range(random.randint(0, nlines)):
            if random.sample([True, False], 1)[0]:
                if random.sample([True, False], 1)[0]:
                    begin = (0, random.randrange(size[1]))
                    end = (size[0]-1, random.randrange(size[1]))
                else:
                    begin = (random.randrange(size[0]), 0)
                    end = (random.randrange(size[0]), size[1]-1)
            else:
                begin = (random.randrange(size[0]), random.randrange(size[1]))
                end = (random.randrange(size[0]), random.randrange(size[1]))
            if line_color == 'rand':
                draw.line([begin, end], fill=randRGBcolor(),
                          width=random.randint(1, line_width))
            else:
                assert type(line_color) == tuple and len(line_color) == 3
                draw.line([begin, end], fill=line_color,
                          width=random.randint(1, line_width))
    if fill_images:
        print fill_image_path
        print 'Currently not functional!'
    if BLUR:
        if filter_rand:
            if random.sample([True, False], 1)[0]:
                image = image.filter(ImageFilter.BLUR)
        else:
            image = image.filter(ImageFilter.BLUR)
    if EDGE_ENHANCE:
        if filter_rand:
            if random.sample([True, False], 1)[0]:
                image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        else:
            image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return image


def charImg(text='T', mode='RGBA', size=(28, 28),
            bgcolor=(255, 255, 255), randbgcolor=True, transparent='auto',
            fontpath=default_fontpath, fontsize='auto',
            fontcolor=(0, 0, 0), randfontcolor=True,
            rotate='rand', QUAD=True,
            BLUR=False, EDGE_ENHANCE=True, filter_rand=True):
    if transparent == 'auto':
        if random.sample([True, False], 1)[0]:
            transparent = random.randint(0, 255)
        else:
            transparent = 0

    def randBGcolor():
        if mode == 'RGBA':
            return tuple(random.sample(range(0, 256, 4), 3) + [transparent])
        elif mode == 'RGB':
            return tuple(random.sample(range(0, 256, 4), 3))

    if randbgcolor:
        bgcolor = randBGcolor()
    else:
        bgcolor = tuple(list(bgcolor) + [transparent])
    image = Image.new(mode=mode, size=size, color=bgcolor)
    draw = ImageDraw.Draw(image)
    if fontsize == 'auto':
        fontsize = max(size)
    font = ImageFont.truetype(fontpath, fontsize)
    new_fontsize = fontsize
    width, height = font.getsize(text)
    posw = (size[0]-width)/2.0
    posh = (size[1]-height)/2.0
    textpos = (posw, posh)
    if height > size[1]:
        while True:
            new_fontsize -= 1
            font = ImageFont.truetype(fontpath, new_fontsize)
            width, height = font.getsize(text)
            if height <= size[1]:
                break
    if randfontcolor:
        fontcolor = randRGBcolor()
    draw.text(textpos, text, font=font, fill=fontcolor)
    if rotate == 'rand':
        image = image.rotate(random.randint(-30, 30), expand=1)
        image = image.resize(size)
    else:
        assert type(rotate) in [int, long]
        image = image.rotate(rotate, expand=1)
        image = image.resize(size)
    if QUAD:
        xt = -size[0]/4
        yt = -size[1]/4
        poses = {'pos0': [(0, 0),
                          (random.randint(xt, 0), random.randint(yt, 0))],
                 'pos1': [(0, size[1]-1),
                          (random.randint(xt, 0),
                           size[1]-1-random.randint(yt, 0))],
                 'pos2': [(size[0]-1, size[1]-1),
                          (size[0]-1-random.randint(xt, 0),
                           size[1]-1-random.randint(yt, 0))],
                 'pos3': [(size[0]-1, 0),
                          (size[0]-1-random.randint(xt, 0),
                           random.randint(yt, 0))]}
        randposes = random.sample(['pos0', 'pos1', 'pos2', 'pos3'],
                                  random.randint(0, 2))
        fixposes = [pos for pos in poses if pos not in randposes]
        for pos in randposes:
            poses[pos] = poses[pos][1]
        for pos in fixposes:
            poses[pos] = poses[pos][0]
        data = tuple(flattern([poses['pos0'], poses['pos1'],
                               poses['pos2'], poses['pos3']]))
        image = image.transform(size, Image.QUAD, data)
    if BLUR:
        if filter_rand:
            if random.sample([True, False], 1)[0]:
                image = image.filter(ImageFilter.BLUR)
        else:
            image = image.filter(ImageFilter.BLUR)
    if EDGE_ENHANCE:
        if filter_rand:
            if random.sample([True, False], 1)[0]:
                image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        else:
            image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return image


def charGenerator(size=(28, 28), fontpath=default_fontpath, text='A',
                  savepath='./train2', fname='0.png'):
    bgimg = bgImg(size=size, line_width=2, BLUR=False,
                  draw_points=True, draw_lines=False)
    charimg = charImg(size=size, text=text)
    bgimg.paste(charimg, (0, 0), charimg)
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    if not os.path.exists(savepath+'/'+text):
        os.mkdir(savepath+'/'+text)
    bgimg.save(savepath+'/'+text+'/'+fname)


def codeGenerator():
    pass


def make_classification_train_data():
    fonts = ['c0419bt_.pfb',
             'c0582bt_.pfb',
             'c0583bt_.pfb',
             'c0611bt_.pfb',
             'c0632bt_.pfb',
             'c0633bt_.pfb',
             'c0648bt_.pfb',
             'c0649bt_.pfb']
    font_path = '/usr/share/fonts/X11/Type1/'
    count = 0
    source = string.digits + string.letters
    for i in range(100):
        fname = '%04d' % count + '.png'
        for text in source:
            charGenerator(text=text, fname=fname, size=(60, 60),
                          fontpath=font_path+random.sample(fonts, 1)[0])
        count += 1
        if count % 100 == 0:
            print 'Generated ' + '%d' % (count*62) + ' training images.'

if __name__ == '__main__':
    make_classification_train_data()

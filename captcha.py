# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 17:41:55 2016

@author: alpha
"""

from __future__ import division
import random
import string
import os
import fortranformat as ff
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# from utils.arrutils import resize
from utils.listutils import flattern


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
          draw_points=True, npoints='auto', point_color='rand', psize=2,
          draw_lines=True, nlines='auto',
          line_color='rand', line_width=2,
          fill_images=False, fill_image_path='',
          SMOOTH=True, EDGE_ENHANCE=False, filter_rand=True):
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
            npoints = long(round(size[0]/5.0) * round(size[1]/5.0) / psize**2)
        else:
            assert type(npoints) in [int, long], 'Watch input!'
        for _ in xrange(random.randint(0, npoints)):
            xpos = random.randrange(size[0])
            ypos = random.randrange(size[1])
            position = [(i, j) for i in range(xpos-random.randint(0, psize),
                                              xpos+random.randint(0, psize))
                        for j in range(ypos-random.randint(0, psize),
                                       ypos+random.randint(0, psize))
                        if 0 <= i < size[0] and 0 <= j <= size[1]]
            if point_color == 'rand':
                draw.point(position, fill=randpointcolor())
            else:
                assert type(point_color) == tuple and len(point_color) == 3
                draw.point(position, fill=point_color)
    if draw_lines:
        if nlines == 'auto':
            # nlines = long(round(max(size)/10.0))
            nlines = 5
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
    if SMOOTH:
        if filter_rand:
            if random.sample([True, False], 1)[0]:
                image = image.filter(ImageFilter.SMOOTH)
        else:
            image = image.filter(ImageFilter.SMOOTH)
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
            rotate='rand', QUAD=True, quadposes='rand',
            SMOOTH=False, EDGE_ENHANCE=True, filter_rand=True):
    if transparent == 'auto':
        if random.sample([True, False], 1)[0]:
            transparent = random.randint(0, 255)
        else:
            transparent = 0
    global TRANSPARENT
    TRANSPARENT = transparent

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
        rotate = random.randint(-30, 30)
        global ROTATE
        ROTATE = rotate
        image = image.rotate(rotate, expand=1)
        image = image.resize(size)
    else:
        assert type(rotate) in [int, long]
        image = image.rotate(rotate, expand=1)
        image = image.resize(size)
    if QUAD:
        if quadposes == 'rand':
            xt = -size[0]//4
            yt = -size[1]//4
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
            global POSES
            POSES = poses
            data = tuple(flattern([poses['pos0'], poses['pos1'],
                                   poses['pos2'], poses['pos3']]))
            image = image.transform(size, Image.QUAD, data)
        else:
            poses = quadposes
            data = tuple(flattern([poses['pos0'], poses['pos1'],
                                   poses['pos2'], poses['pos3']]))
            image = image.transform(size, Image.QUAD, data)
    if SMOOTH:
        if filter_rand:
            if random.sample([True, False], 1)[0]:
                image = image.filter(ImageFilter.SMOOTH)
        else:
            image = image.filter(ImageFilter.SMOOTH)
    if EDGE_ENHANCE:
        if filter_rand:
            if random.sample([True, False], 1)[0]:
                image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        else:
            image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return image


def charGenerator(size=(28, 28), fontpath=default_fontpath, text='A',
                  savepath='./train2', fname='0.png'):
    bgimg = bgImg(size=size, line_width=2, SMOOTH=False,
                  draw_points=True, draw_lines=False)
    charimg = charImg(size=size, text=text, fontpath=fontpath, rotate=0)
    bgimg.paste(charimg, (0, 0), charimg)
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    if not os.path.exists(savepath+'/'+text):
        os.mkdir(savepath+'/'+text)
    bgimg.save(savepath+'/'+text+'/'+fname)


def codeGenerator(text='TEST', bgsize=(200, 60), charsize='auto',
                  w_sep=0, transparent='auto', draw_box=False,
                  fname='test', line_width=2):
    bgimg = bgImg(size=bgsize, draw_points=True, psize=3,
                  line_width=line_width,
                  draw_lines=True, SMOOTH=True)
    # generate code
    text_lst = list(text)
    text_num = len(text)
    if charsize == 'auto':
        charsize = tuple([int(bgsize[1]*0.9)]*2)
    else:
        assert type(charsize) is tuple and len(charsize) == 2, 'watch input!'
    w_out = (bgsize[0] - text_num*charsize[0] - (text_num-1)*w_sep) / 2
    if w_out < 0:
        print 'Warning! Char edge out of box!'
    labels = []
    bboxes = []
    fourpoints = []
    charimgs = []
    for i, char in enumerate(text_lst):
        posw_i = int(w_out + i*(charsize[0]+w_sep))
        posh_i = int((bgsize[1] - charsize[1]) / 2)
        charimg = charImg(size=charsize, text=char, transparent=transparent,
                          EDGE_ENHANCE=True, SMOOTH=True)
        # compute char edge
        global ROTATE, POSES, TRANSPARENT
        tmp_transparent = TRANSPARENT
        bboximg = charImg(size=charsize, text=char, transparent=0,
                          fontcolor=(255, 255, 255),
                          EDGE_ENHANCE=False, SMOOTH=False,
                          rotate=ROTATE, quadposes=POSES)
        bbox = bboximg.getbbox()
        bbox = [posw_i+bbox[0], posh_i+bbox[1],
                posw_i+bbox[2], posh_i+bbox[3]]
        fourpoint = [(bbox[0], bbox[1]),
                     (bbox[2], bbox[1]),
                     (bbox[2], bbox[3]),
                     (bbox[0], bbox[3])]
        fourpoints.append(fourpoint)
        bboxes.append(bbox)
        label = bbox + [char]
        labels.append(label)
        charimgs.append((charimg, posw_i, posh_i, tmp_transparent))
    charimgs = sorted(charimgs, key=lambda x: x[3], reverse=True)
    for charimg in charimgs:
        bgimg.paste(charimg[0], (charimg[1], charimg[2]), charimg[0])
    if draw_box:
        draw = ImageDraw.Draw(bgimg)
        for element in fourpoints:
            draw.polygon(element, outline=(255, 0, 0))
        pass
#    bgimg.save('test.jpg')
    bgimg.mode = 'RGB'
    bgimg.save(fname+'.png')
    label_file = open(fname+'.txt', 'w')
    for label in labels:
        out_format = ff.FortranRecordWriter('(4(I5, 1X), A4)')
        out_string = out_format.write(label)
        print>>label_file, out_string
    label_file.close()


def rand_text(number=5):  # 用来随机生成一个字符串
    source = list(string.letters + string.digits)
    text = ''.join(random.sample(source, number))
    return text


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
    numbers = 100
    for i in range(numbers):
        fname = '%04d' % count + '.jpg'
        for text in source:
            charGenerator(text=text, fname=fname, size=(60, 60),
                          fontpath=font_path+random.sample(fonts, 1)[0])
        count += 1
        if count % 10 == 0:
            print 'Generated ' + '%5d' % (count*62) + ' training images.'
        if count == numbers:
            print 'Done!'


def make_captcha_data():
    path = './captcha'
    if not os.path.exists(path):
        os.mkdir(path)
    for i in xrange(100):
        fname = path + '/' + '%04d' % (i+1)
        text = rand_text(number=4)
        codeGenerator(text=text, w_sep=-5, bgsize=(100, 30), fname=fname)


if __name__ == '__main__':
    # Image.fromarray(imresize)
    # make_classification_train_data()
    make_captcha_data()

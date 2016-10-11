# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 11:03:33 2016

Utils for list or tuple processing.

@author: alpha
"""


def charlist(in_list):
    '''Convert a list of strings to a list of seperate chars.

    Example:
        in_list = ['', 'abc', 'd']\n
        out_list = charlist(in_list)\n
        out_list -> ['', 'a', 'b', 'c', 'd']
    '''
    out_list = []
    for i in in_list:
        assert type(i) in [str, unicode]
        if i == '':
            out_list.append(i)
        else:
            out_list += list(i)
    return out_list


def flattern(in_list):
    '''Flattern a list[tuple] of list[tuple] objects to
    a list of non-list or non-tuple elements.

    Example:
        in_list = [1, [2, [3, 4]]]\n
        out_list = flattern(in_list)\n
        out_list -> [1, 2, 3, 4]
    '''
    out_list = []
    for i in in_list:
        if type(i) in [list, tuple]:
            out_list += flattern(i)
        else:
            out_list.append(i)
    return out_list


def shrinkstrlist(in_list):
    '''Shrink a list of str sequence to
    a list of strings seperated by empty str in the previous sequence.

    Example:
        in_list = ['', 'a', 'b', 'c', '', 'd']\n
        out_list = shrinkstrlist(in_list)\n
        out_list -> ['abc', 'd']
    '''
    tmp_list = []
    for i in in_list:
        if i == '':
            tmp_list.append(' ')
        else:
            tmp_list.append(i)
    outstr = ''.join(tmp_list)
    out_list = outstr.strip().split()
    return out_list

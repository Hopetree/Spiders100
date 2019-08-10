# -*- coding:utf-8 -*-
# Author: https://github.com/Hopetree
# Date: 2019/8/10

'''
剪切音频的工具
'''

import os
from pydub import AudioSegment


def cut_mp3(dirname):
    for each in os.listdir(dirname):
        _name, _type = os.path.splitext(each)
        filename = os.path.join(dirname, each)
        newdir = os.path.join(dirname, 'new')
        if not os.path.exists(newdir):
            os.makedirs(newdir)
        newname = os.path.join(newdir, each)
        if _type == '.mp3':
            mp3 = AudioSegment.from_mp3(filename)
            new_mp3 = mp3[9 * 1000:]
            new_mp3.export(newname, format='mp3')
            print('{} cut done'.format(each))


if __name__ == '__main__':
    DIRNAME = r'C:\Users\HP\Downloads\load'
    cut_mp3(DIRNAME)

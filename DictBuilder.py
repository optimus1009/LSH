# -*-coding:utf8-*-
'''
Created on Tue Aug 22 15:51:20 2017

@author: lin
根据分词结果文件或目录，生成以词频降序排列的特征词典
词典格式如下：ID + 特征词 + 词频
'''
from collections import defaultdict
import os
import sys


class WordDictBuilder:
    def __init__(self, ori_path='', filelist=[], tokenlist=[]):
        self.word_dict = defaultdict(int)
        if ori_path != '' and os.path.exists(ori_path):
            with open(ori_path) as ins:
                for line in ins.readlines():
                    #<word:tf>  (词组：词频)
                    self.word_dict[line.split('\t')[1]] = int(line.split('\t')[2])
        self.filelist = filelist
        self.tokenlist = tokenlist

    def run(self):
        for filepath in self.filelist:
            self._updateDict(filepath)
        self._updateDictByTokenList()
        return self

    def _updateDict(self, filepath):
        with open(filepath, 'r') as ins:
            for line in ins.readlines():
                for word in line.split('\t')[1].rstrip().split():
                    self.word_dict[word] += 1
    # _updateDict主要用于构建一个词典，而_updateDictByTokenList用于添加额外自定义的token，
    def _updateDictByTokenList(self):
        for token in self.tokenlist:
            if isinstance(token, unicode):
                token = token.encode('utf8')
            self.word_dict[token] += 1

    def save(self, filepath):
        l = [(value, key) for key, value in self.word_dict.items()]
        l = sorted(l, reverse=True)
        result_lines = []
        for idx, (value, key) in enumerate(l):
            #os.linesep: 字符串给出当前平台使用的行终止符。例如，Windows使用'\r\n'，Linux使用'\n'而Mac使用'\r'
            result_lines.append('%s\t%s\t%s%s' % (idx, key, value, os.linesep))
        with open(filepath, 'w') as outs:
            #注意write和writelines 区别，writelines不会在每一行末尾加入换行符，参数为一个可迭代的字符串元素序列
            outs.writelines(result_lines)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage:\tWordDictBuilder.py <input_folder/file> <output_file>"
        exit(-1)
    if not os.path.isfile(sys.argv[1]):
        #os.sep 可以取代操作系统特定的路径分割符
        filelist = [sys.argv[1] + os.sep + f for f in os.listdir(sys.argv[1])]
    else:
        filelist = [sys.argv[1]]
    builder = WordDictBuilder(filelist=filelist)
    builder.run()
    builder.save(sys.argv[2])

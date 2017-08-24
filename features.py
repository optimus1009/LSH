#-*-coding:utf8-*-
'''
Created on Tue Aug 22 16:03:26 2017

@author: lin
根据分词结果和特征词典，生成特征向量文件
以行为单位生成各文档的特征向量：id1:nonzero-tf id2:nonzero-tf 
'''
import os,sys
class FeatureBuilder:
    def __init__(self, word_dict):
        self.word_dict = word_dict
    
    def compute(self, token_list):
        #长度为word_dic的全0向量
        feature = [0]*len(self.word_dict) #word_dict--> (word:index)
        for token in token_list:
            feature[self.word_dict[token]] += 1
        #将特征长度（等于字典长度）转化为非0字典长度，过滤0值
        feature_nonzero = [(idx,value) for idx, value in enumerate(feature) if value > 0]
        return feature_nonzero

    def _add_word(self, word):
        if not word in self.word_dict:
            self.word_dict[word] = len(self.word_dict)

    def update_words(self, word_list=[]):
        for word in word_list:
            self._add_word(word)

class FeatureBuilderUpdate(FeatureBuilder):
    def _add_word(self, word):
        self.word_dict.add_one(word)


def feature_single(inputfile, outputfile):
    print inputfile,outputfile
    result_lines = []
    with open(inputfile, 'r') as ins:
        for lineidx, line in enumerate(ins.readlines()):
            feature = fb.compute([token.decode('utf8') for token in line.strip().split()])
            l = []
            for idx,f in feature:
                if f > 1e-6:
                    l.append('%s:%s' %(idx,f))
            result_lines.append(' '.join(l) + os.linesep)
            print 'Finished\r', lineidx,
    with open(outputfile, 'w') as outs:
        outs.writelines(result_lines)
    print 'Wrote to ', outputfile

if __name__=="__main__":
    if len(sys.argv) < 5:
        print "Usage:\tfeature.py -s/-m <word_dict_path> <tokens_file/tokens_folder> <feature_file/feature_folder>"
        exit(-1)
    word_dict = {}
    with open(sys.argv[2], 'r') as ins:
        for line in ins.readlines():
            l = line.split()
            word_dict[l[1].decode('utf8')] = int(l[0])  #建立 word:tf 的字典
    fb = FeatureBuilder(word_dict)
    print 'Loaded', len(word_dict), 'words'
    if sys.argv[1] == '-s':
        feature_single(sys.argv[3], sys.argv[4])
    elif sys.argv[1] == '-m':
        for inputfile in os.listdir(sys.argv[3]):
            feature_single(os.path.join(sys.argv[3],inputfile), os.path.join(sys.argv[4],inputfile.replace('.token','.feat')))

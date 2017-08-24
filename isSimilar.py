# -*-coding:utf8-*-
'''
Created on Tue Aug 22 16:59:40 2017

@author: lin
'''
from __future__ import division
import sys
from simhash_imp import SimhashBuilder, hamming_distance
from tokens import JiebaTokenizer
from features import FeatureBuilder
from Utils import norm_vector_nonzero, cosine_distance_nonzero


class DocFeatLoader:
    def __init__(self, simhash_builder, feat_nonzero):
        self.feat_vec = feat_nonzero
        self.feat_vec = norm_vector_nonzero(self.feat_vec)
        self.fingerprint = simhash_builder.sim_hash_nonzero(self.feat_vec)
        
if __name__ == "__main__":
    if len(sys.argv) < 7:
        print "Usage:\tisSimilar.py <doc1> <doc2> <stopword_path> <word_dict> <-c/-s> <threshold>"
        exit(-1)
    doc_path_1, doc_path_2, stopword_path, word_dict, mode, threshold = sys.argv[1:]
    print 'Arguments get success:', sys.argv[1:]
    with open(doc_path_1) as ins:
        doc_data_1 = ins.read().decode('utf8')
        print 'Loaded', doc_path_1
    with open(doc_path_2) as ins:
        doc_data_2 = ins.read().decode('utf8')
        print 'Loaded', doc_path_2

    # 初始化分词器,主要是加载停用词
    jt = JiebaTokenizer(stopword_path, 'c')

    # 分词 tokens返回分词后的数组
    doc_token_1 = jt.tokens(doc_data_1)
    doc_token_2 = jt.tokens(doc_data_2)
    
    print 'Loading word dict...'
    # 加载字典
    word_list = []
    with open(word_dict, 'r') as ins:
        for line in ins.readlines():
            word_list.append(line.split()[1])
            
    # Build unicode string word dict
    word_dict = {}
    for idx, ascword in enumerate(word_list):
        word_dict[ascword.decode('utf8')] = idx
    # Build nonzero-feature
    fb = FeatureBuilder(word_dict)
    doc_feat_1 = fb.compute(doc_token_1) # return feature_nonzero得到一个非0 长度的向量 ，元素为(idx,value)且 value > 0
    doc_feat_2 = fb.compute(doc_token_2)

    #使得字典中的每个值都有一个hash值，
    smb = SimhashBuilder(word_list)

    doc_fl_1 = DocFeatLoader(smb, doc_feat_1)
    doc_fl_2 = DocFeatLoader(smb, doc_feat_2)

    if mode == '-c':
        print 'Matching by VSM + cosine distance'
        dist = cosine_distance_nonzero(doc_fl_1.feat_vec, doc_fl_2.feat_vec, norm=False)
        if dist > float(threshold):
            print 'Matching Result:\t<True:%s>' % dist
        else:
            print 'Matching Result:\t<False:%s>' % dist
    elif mode == '-s':
        print 'Matching by Simhash + hamming distance'
        dist = hamming_distance(doc_fl_1.fingerprint, doc_fl_2.fingerprint)
        bin_doc_1 = list(bin(doc_fl_1.fingerprint))
        bin_doc_2 = list(bin(doc_fl_2.fingerprint))
        bin_zip = zip(bin_doc_1,bin_doc_2)
        cnt = 0 
        for elem in bin_zip:
            if elem[0] == elem[1]:
                cnt += 1
        prob = cnt/len(bin_zip)
        if dist < float(threshold):
            print('doc_1 simhash code: %(f1)s \ndoc_2 simhash code: %(f2)s') % {'f1':bin(doc_fl_1.fingerprint),'f2':bin(doc_fl_2.fingerprint)}
            print 'Matching Result: True:%(dist)s , Similarity: %(sim)s' % {'dist':dist,'sim':prob}
        else:
            print('doc_1 simhash code: %(f1)s \ndoc_2 simhash code: %(f2)s') % {'f1':bin(doc_fl_1.fingerprint),'f2':bin(doc_fl_2.fingerprint)}
            print 'Matching Result: False:%(dist)s , Similarity: %(sim)s' % {'dist':dist,'sim':prob}

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:42:37 2017
@author: lin
"""

from __future__ import division
import sys
from simhash_imp import SimhashBuilder, hamming_distance
from tokens import JiebaTokenizer
from features import FeatureBuilder
from Utils import norm_vector_nonzero, cosine_distance_nonzero
import time

class DocFeatLoader:
    def __init__(self, simhash_builder, feat_nonzero):
        self.feat_vec = feat_nonzero
        self.feat_vec = norm_vector_nonzero(self.feat_vec)
        self.fingerprint = simhash_builder.sim_hash_nonzero(self.feat_vec)
        
if __name__ == "__main__":
    doc_1_noise,doc_path_1, doc_path_2, stopword_path, word_dict, mode, threshold = ('../text-similarity/data/doc_1.data',\
                                                                                    '../text-similarity/data/doc_1.clear',\
                                                                                    '../text-similarity/data/doc_2.data',\
                                                                                    '../text-similarity/data/stopwords.txt',\
                                                                                    '../text-similarity/data/word.dict',\
                                                                                    '-s',15)
    print 'Arguments get success:', sys.argv[1:]
    #原始query文档
    with open(doc_1_noise) as noise_file:
        doc_noise_file = noise_file.read().decode('utf8')
    #去噪后的query文档
    with open(doc_path_1) as ins:
        doc_data_1 = ins.read().decode('utf8')
    print 'Loaded', doc_path_1
    # 初始化分词器,主要是加载停用词
    jt = JiebaTokenizer(stopword_path, 'c')

    # 分词 tokens返回分词后的数组
    doc_token_1 = jt.tokens(doc_data_1)    
    print 'Loading word dict...'
    # 加载字典并构建词典
    word_list = []
    with open(word_dict, 'r') as ins:
        for line in ins.readlines():
            word_list.append(line.split()[1])
    word_dict = {}
    for idx, ascword in enumerate(word_list):
        word_dict[ascword.decode('utf8')] = idx
    # 构建非0特征向量
    fb = FeatureBuilder(word_dict)
    doc_feat_1 = fb.compute(doc_token_1) # return feature_nonzero得到一个非0 长度的向量 ，元素为(idx,value)且 value > 0
    #使得字典中的每个值都有一个hash值，
    smb = SimhashBuilder(word_list)
    doc_fl_1 = DocFeatLoader(smb, doc_feat_1)
    #测试文件,用于调研算法
    out_file = open('/home/lin.xiong/text-similarity/data/out.file','w')
    #fp_set = set()
    fp_arr = []
    with open('/home/lin.xiong/text-similarity/data/clear_test.fingerprint','r') as fp:
        for line in fp:
            fp_arr.append(long(line))
    comment = []
    with open('/home/lin.xiong/text-similarity/data/test.data','r') as comment_file:
        for line in comment_file:
            comment.append(line)
    fp_comment_tup = zip(fp_arr,comment)
    fp_comment_dict = dict(fp_comment_tup)
    if mode == '-s':
        print 'Matching by Simhash + hamming distance'
#----------------------------------------------------------------------
        tmp_dic = {}
        start_millis = int(round(time.time()*1000))
        for fp in fp_arr:
            dist = hamming_distance(doc_fl_1.fingerprint, fp)
            tmp_dic[fp] = dist
        end_millis = int(round(time.time()*1000))
        print end_millis - start_millis
#------------------------------------------------------------------------
        dict_sorted= sorted(tmp_dic.items(), key=lambda d:d[1])
        concat = 0 
        for fp_dist_tup in dict_sorted:
            if concat <= 99:
                bin_doc_1 = list(bin(doc_fl_1.fingerprint))
                print len(bin_doc_1),
                bin_doc_2 = list(bin(fp_dist_tup[0]))
                print len(bin_doc_2),
                bin_zip = zip(bin_doc_1,bin_doc_2)
                cnt = 0 
                for bin1_bin2_tup in bin_zip:
                    if bin1_bin2_tup[0] == bin1_bin2_tup[1]:
                        cnt += 1
                sim = cnt/len(bin_zip)
                prob = (128 - fp_dist_tup[1])/128
                if fp_dist_tup[1] < float(threshold):
                    print 'query: ',doc_noise_file,
                    print 'comment:',fp_comment_dict[fp_dist_tup[0]],
                    print('doc_1 simhash code: %(f1)s \ndoc_2 simhash code: %(f2)s ') % {'f1':bin(doc_fl_1.fingerprint),'f2':bin(fp_dist_tup[0])}
                    print 'Matching Result: True:%(dist)s , Similarity: %(sim)s\n' % {'dist':fp_dist_tup[1],'sim':prob}
                    out_file.write(doc_noise_file.strip().encode('utf-8') + '\t' + fp_comment_dict[fp_dist_tup[0]].strip() + '\t' + str(fp_dist_tup[1]) + '\t' + str(prob) + '\n')
                else:
                    print 'query: ',doc_noise_file,
                    print 'comment:',fp_comment_dict[fp_dist_tup[0]],
                    print('doc_1 simhash code: %(f1)s \ndoc_2 simhash code: %(f2)s') % {'f1':bin(doc_fl_1.fingerprint),'f2':bin(fp_dist_tup[0])}
                    print 'Matching Result: False:%(dist)s , Similarity: %(sim)s' % {'dist':fp_dist_tup[1],'sim':prob}
                    out_file.write(doc_noise_file.strip().encode('utf-8') + '\t' + fp_comment_dict[fp_dist_tup[0]].strip() + '\t' + str(fp_dist_tup[1]) + '\t' + str(prob) + '\n')
                concat += 1
    else:
        print 'please select model -s'
    out_file.close()

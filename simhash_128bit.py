# -*- coding: utf-8 -*-

import re
from hashlib import md5
import sys
import os
class Token:

    def __init__(self, hash_list, weight):
        self.hash_list = hash_list
        self.weight = weight

def md5Hash(token):
    #h = bin(int(md5(token).hexdigest(), 16)) # 128位hash码
    h = bin(int(md5(token).hexdigest()[8:-8], 16)) #64位hash码
    return h[2:]

def hash_threshold(token_dict, fp_len):
    """
    迭代所有的分词，并且每个hashcode乘上权重
    """
    sum_hash = [0] * fp_len
    for _, token in token_dict.iteritems():
        sum_hash = [ x + token.weight * y for x, y in zip(sum_hash, token.hash_list)]

    # 二值化
    for i, ft in enumerate(sum_hash):
        if ft > 0:
            sum_hash[i] = 1
        else:
            sum_hash[i] = 0
    return sum_hash

def binconv(fp, fp_len):
    """
    转换
    input  : 1001...1
    output : [1,-1,-1, 1, ... , 1]
    """
    vec = [1] * fp_len
    for indx, b in enumerate(fp):
        if b == '0':
            vec[indx] = -1
    return vec


def calc_weights(terms, fp_len):
    """
    统计每一个分词的权重，这里用分词在文档里面的tf作为权重，
    :param tokens: A list of all the tokens (words) within the document
    :fp_len: simhash的长度
    return: Token([-1,1,-1,1,..,-1], 5)
    """
    term_dict = {}
    for term in terms:
        # get weights
        if term not in term_dict:
            fp_hash = md5Hash(term).zfill(fp_len)
            fp_hash_list = binconv(fp_hash, fp_len)
            token = Token(fp_hash_list, 0)
            term_dict[term] = token
        term_dict[term].weight += 1
    return term_dict

def simhash(doc, fp_len=64):
    """
    :param doc: The document we want to generate the Simhash value
    :fp_len: simhash的长度，一般为 64，128,这里可以随时更改，但是要保持与md5Hash一致，
    :return :'0000100001110'
    """
    #tokens = tokenize(doc)
    token_dict = calc_weights(doc, fp_len)
    fp_hash_list = hash_threshold(token_dict, fp_len)
    fp_hast_str =  ''.join(str(v) for v in fp_hash_list)
    return fp_hast_str


if __name__ == '__main__':
    post_id = []
    simhashcode = []
    with open('../lsh_data/test_clear.token','r') as token:
        for line in token:
            pid = line.split('\t')[0]
            post_id.append(pid.strip())
            doc = line.split('\t')[1]
            binary_hash = simhash(doc)
            simhashcode.append(pid + '\t' + str(binary_hash) + os.linesep)
    with open('../lsh_data/test_hash_code_file','w') as hash_code_file:
        hash_code_file.writelines(simhashcode)

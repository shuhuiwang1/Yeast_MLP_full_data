#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 10:00:11 2022

@author: wangshuhui
"""

from csv import reader
from torch import tensor

def get_all_gene(gene_int_file):
  tmp = []
  with open(gene_int_file) as input_f:
    for line in reader(input_f, delimiter=' ', quotechar='"'):
      name_1, name_2 = line[:2]
      tmp += [[name_1, name_2]] 
    gen_1_all = list(set([el[0] for el in tmp]))
    gen_2_all = list(set([el[1] for el in tmp]))
  return gen_1_all, gen_2_all 

def read_gene_batch(gene_int_file, gen_1_all, gen_2_all, bsize=12):
    """From 6 x 10^6 pairs of gene interactions; go_vector dictionary
    """
    # batch = zeros((bsize, 2*414))
    pair_id = 0
    tmp_real = []
    gene_data = []

    with open(gene_int_file) as input_f:
        for pair_l in reader(input_f, delimiter=' ', quotechar='"'):
            try:
              name_1, name_2 = pair_l[:2]
            except:
              print(pair_l[:2])
            
            gene_data += [[gen_1_all.index(name_1), gen_2_all.index(name_2)]] 

            
            tmp_real += [float(pair_l[-1])]
            pair_id += 1

            if pair_id == bsize:
                # yield tensor(batch), tensor(tmp_real)
                yield tensor(gene_data), tensor(tmp_real)
                # batch = zeros((bsize, 2*414))
                pair_id = 0
                tmp_real = []
                gene_data = [] 
                
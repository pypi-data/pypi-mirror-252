# -*- coding:utf-8 -*-
# Author:  zhousf-a
# Date:    2024-01-24
# Description:
def jaccard_similar():
    Nu = {'A', 'C', 'D'}
    Nv = {'A', 'E','C', 'D'}
    # Nv = {'A', 'B', 'D', 'E'}
    similarity = len(Nu & Nv) / len(Nu | Nv)
    print(similarity)

jaccard_similar()
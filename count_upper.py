#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 18:01:34 2021

"""


def COUNT_UPPER(text):
	if text != '':
		c_up=sum(1 for c in text if c.isupper())
		sum_letter=sum(1 for c in text)
		rep=c_up/sum_letter
		if (rep < (10*sum_letter)/100):
			score=1
		else:
			score=0
	else:
		score = 0
		rep = 0

	return(rep, score)
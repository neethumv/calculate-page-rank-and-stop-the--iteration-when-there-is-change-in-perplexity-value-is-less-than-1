
import sys
import math
import operator
from collections import OrderedDict

#P is the set of all pages; |P| = N
# S is the set of sink nodes, i.e., pages that have no out links
# M(p) is the set (without duplicates) of pages that link to page p
# L(q) is the number of out-links (without duplicates) from page q
# d is the PageRank damping/teleportation factor; use d = 0.85 as is typical

P = set();
M = dict();
d = 0.85;
L = dict();
S = list();
#declaring necessary list or dictionary to be used in the program
perplexity = list()
PR = dict();
page_rank = dict()
key_value = dict()
perplexityList = list()
perplexFile = open('PerplexityFile.txt', 'w')
#main method which takes the input file as argument
def main(filename):
	#writing the top 50 pages along with its page rank values 
	top50PRFile = file('top50PageRank.txt', 'wt')
	#writing the top 50 page along with its in-link count
	top50inlinkFile = file('top50inlinks.txt', 'wt')
	#this method creates the M, L, P, S from the input file
	extractGraph(filename)
	#this method calculates the page-rank and write the perplexity value when the perplexity converges
	calpagerank()
	#this method return a list of top 50 pages by page-rank along with their page-rank values
	top50PRlist = top50PR()
	#this method return a list of top 50 pages by in-link count along with their in-link count
	top50inlinklist = top50inlinks()
	#writing the top 50 pages by page-rank in a file
	for item in top50PRlist:
		top50PRFile.write(str(item) + '\n')
	#writing the top 50 pages by in-link count in a file
	for doc in top50inlinklist:
		top50inlinkFile.write(str(doc) + '\n')
	
	print 'done reading the input file'
#this method takes the input file and creates the necessary lists, sets and dictionary i.e (P,M,L,S) 
#to calculate the page rank 	
def extractGraph(filename):
	infile = open(filename)
	print 'computing M and P '
	for line in infile:
		line = line.rstrip();
		x = line.split(' ');
		p = x[0];
		#add the pages to set P
		P.add(p);
		setlines = set(x[1:])
		#creating M dictionary with pages as key and its in-link pages as it value
		if p in M:
			M[p] = M[p].union(setlines)
		else:
			M[p] = setlines
	#create a dictionary with pages as key and the number of each in-link as their values
	for key in M:
		key_value[key] = len(M[key])
	infile.close()	
	#initialising the L list with 0	
	for i in P:
		L[i] = 0;
	
	print 'computing L list: please wait'
	#computing and updating the L list with the number of out-link
	for values in M.values():
		for value in values:
			L[value] += 1
	print 'computing S list: please wait'
	#computing the S list which holds the sink node
	for p in P:
		if (L[p] == 0):
			if(p not in S):
				S.append(p)

#this method calculates the perplexity value
def calcperplexity():
	entropy = 0
	for p in P:
		entropy -= (PR[p] * math.log(PR[p],2));
	perplexity = math.pow(2, entropy)
	return perplexity
#this method find whether the change in perplexity is less than 1 and stops the computation further	
def calcconvergence(iteration):
	perplexity_value = calcperplexity()
	perplexity.append(perplexity_value)
	#calculate perplexity for at least 4 iteration
	if(len(perplexity)>4):
		#returns true when the change in perplexity is less than 1
		if(((perplexity[iteration-3] - perplexity[iteration-2]) <1) and ((perplexity[iteration-2] - perplexity[iteration-1]) <1) and ((perplexity[iteration-1] - perplexity[iteration]) <1)):
			print iteration+1, calcperplexity()
			perplexFile.write('perplexity after {} iteration:'.format(iteration+1) + str(' ') + str(calcperplexity()).ljust(40) + '\n')
			return False
		else:
			return True
	else:
		return True

#this methods calculates the page rank
def calpagerank():
	
	iter = 0 
	newPR = dict()
	N = len(P)
	
	for p in P:
		#initial value
		PR[p] = 1.0/N
	
	#this loop converges until the change in perplexity is less than 1
	while calcconvergence(iter):
		#print 'Calculating perplexity and stops until the change in perplexity is less than 1'
		print iter+1, calcperplexity()
		perplexFile.write('perplexity after {} iteration:'.format(iter+1) + str(' ') + str(calcperplexity()).ljust(40) + '\n')
		sinkPR = 0
		for p in S:
			#calculate total sink PR
			sinkPR += PR[p]
		for p in P:
			#teleportation
			newPR[p] = (1-d)/N;
			#spread remaining sink PR evenly
			newPR[p] += d*sinkPR/N
			#pages pointing to p
			for q in M[p]:
				#add share of page-rank from in-links
				newPR[p] += d*PR[q]/L[q] 
	
		for p in P:
			PR[p] = newPR[p]
		iter += 1 
	perplexFile.close()	

 	
#this method sort the pages by top 50 page-rank values
def top50PR():
	print 'sorting top 50 pages by their page rank values'
	top50PR = []
	SortedPR = sorted(PR.iteritems(), key=operator.itemgetter(1), reverse=True)
	for i in range(50):
		top50PR.append(SortedPR[i])
		#print SortedPR[i]
	return top50PR

#this method sort the page by top 50 in-link count	
def top50inlinks():
	print 'sorting top 50 pages by their inlink count'
	top50inlink = []
	sortedinlinks = sorted(key_value.iteritems(), key=operator.itemgetter(1), reverse=True)
	for i in range(50):
		top50inlink.append(sortedinlinks[i])
		#print sortedinlinks[i]
	return top50inlink

#Main program:
if __name__ == '__main__':
	main(sys.argv[1])
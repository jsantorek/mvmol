#placehlder file - scruipt supposed to make bash scripts for kraken
import os

dname = "_ccsd.dal" #can later be replaced with search for method
inputdir = os.getcwd() + '/output'
print(inputdir)
sh = open(inputdir + '/_test.sh', 'w')
sh.write('#!/bin/sh\n')
sh.write('\n')
c_mol = 0
for fname in os.listdir(inputdir):
	if fname.endswith(".mol"):
		#print(os.path.join("/mydir", file))
		c_mol += 1
		sh.write('/pbs_home/hjaajensen/progs/gitDalton/build_apsg/dalton -dal '+dname+' -mol '+fname+'\n')
print('Process ended successfully.\n'+str(c_mol)+' mol files recognised.')
sh.close();
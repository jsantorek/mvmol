# Simple script extracting usable lines from given txt input file, making data verificaion easier.

from mvmol_defs import *

c_test = 0
i_f = open('input/geometries_all.txt', 'r')
o_f = open('input/geometries.txt', 'w')

for l in i_f:
	if l =='\n':
		continue;
	if l[:4] == 'name':
		c_test += 1
		o_f.write('\n\n'+l+'\n')
		continue;
	ls = l.split()

	# check if line has usable data
	if len(ls) == 1 or len(ls) == 4 or len(ls) == 5:
		o_f.write(l)

print('Process ended successfully.\n'+str(c_test)+' tests.')

o_f.close()
i_f.close()
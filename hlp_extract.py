# Simple script extracting energy values from dalton out files to txt file to easily plot and verify it.
# Only works for ccsd method currently.

scaling_factors = [0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15]
molecule_names = ["C2H4-F2"]
method_names = ['SCF', 'MP2', 'CCSD', 'CCSD(T)']
all_energies = []
dal_prefix = "_ccsd_"
directory = "output/"

start_energies = '             ! Final results from the Coupled Cluster energy program !\n'
end_energies = ' *******************************************************************************\n'

def ReadEnergies(inf):
	local_energies = []
	while True:
		line = inf.readline()
		if line == "\n":
			continue;
		if line == end_energies or line == '' or line == 'eof\n':
			break;
		ldata = line.split()
		if len(ldata) != 4 or ldata[0] != 'Total':
			continue;
		local_energies.append(ldata[3])
	all_energies.append(local_energies)
	return;

def WriteEnergies(ouf, mol):
	ouf.write(mol + '\nscales\n')
	for sf in scaling_factors:
		ouf.write(str(sf) + '\n')
	ouf.write('\nSCF\n')
	for e in all_energies:
		ouf.write(e[0] + '\n')
	ouf.write('\nMP2\n')
	for e in all_energies:
		ouf.write(e[1] + '\n')
	ouf.write('\nCCSD\n')
	for e in all_energies:
		ouf.write(e[2] + '\n')
	ouf.write('\nCCSD(T)\n')
	for e in all_energies:
		ouf.write(str(e[3]) + '\n')
	return;

def main():
	for mol in molecule_names:
		ouf = open(directory + mol + ".txt", 'w');
		all_energies.clear()
		for sf in scaling_factors:
			inf = open(directory + dal_prefix + mol + "-" + str(sf) + ".out", 'r')
			while True:
				line = inf.readline()
				if line == '' or line == 'eof\n':
					break;
				if line == start_energies:
					ReadEnergies(inf)
					break;
			inf.close()
		WriteEnergies(ouf, mol)
		ouf.close()		
	return;

if __name__ == "__main__":
	main()
#!/usr/bin/python
import math
from mvmol_defs import *
from mvmol_settings import *

mmers = []
initpos = []
mname = []

def ReadTestData(ifile):
   mname.clear()
   mname.append('')
   mmers.clear()
   mmers.append(Molecule())
   while True:
      line = ifile.readline()
      if line == '' or line == 'eof\n':
         return False;
      if line == file_test_separator:
         mmers[-1].update()
         return True;
      if line == file_monomer_separator:
         mmers[-1].update()
         mmers.append(Molecule())
         continue;
      ldata = line.split('=')
      if len(ldata) == file_keywordline_l:
         if ldata[0] == file_keyword_name:
            mname[0] = ldata[1][:-1]
      ldata = line.split()
      if len(ldata) == 4 or len(ldata) == 5:
         adata = [0, '', Vector(0, 0, 0)]
         adata[mmers[-1].mass_i] = int(ldata[file_mass_i])
         adata[mmers[-1].tag_i] = ldata[file_tag_i]
         adata[mmers[-1].pos_i] = Vector(
            float(ldata[file_xpos_i])*correction_factor, float(ldata[file_ypos_i])*correction_factor,
               float(ldata[file_zpos_i])*correction_factor )
         mmers[-1].Atoms.append(adata)
   return False;

def PrepareTestData():
   if len(mmers) < 2:
      print('Insufficient amount of groups for '+mname[0])
      return False;
   for mer in mmers:
      initpos.append(mer.CenterOfMass)
   return True;

def WriteTestData(filename):
   atoms = []
   temp = 0
   cnt = 0
   for mer in mmers:
      atoms.extend(mer.Atoms)
   atoms.sort(key=lambda x: x[Molecule.mass_i])
   f = open(o_prefix + filename, 'w')
   f.write(o_header1)
   f.write(o_header2)
   f.write(o_header3)
   f.write(o_header4)
   f.write('Atomtypes={at} Charge=0 Nosymmetry Cartesian\n'.format(
      at=len(set(a[Molecule.mass_i] for a in atoms)) ))

   for atom in atoms:
      if temp != atom[Molecule.mass_i]:
         cnt = 0
         temp = atom[Molecule.mass_i]
         if temp < 10:
            f.write('        {am}.    {n}\n'.format(
               am=temp, n=len([a for a in atoms if a[Molecule.mass_i] == temp]) ))
         else:
            f.write('       {am}.    {n}\n'.format(
               am=temp, n=len([a for a in atoms if a[Molecule.mass_i] == temp]) ))
      f.write('{t}    {x:.9f}    {y:.9f}    {z:.9f}\n'.format(t=GetSymbol(atom[Molecule.mass_i])+str(cnt+1),
         x=atom[Molecule.pos_i].x, y=atom[Molecule.pos_i].y, z=atom[Molecule.pos_i].z) )
      cnt += 1
   f.close()
   return;

def GetSymbol(mass):
   if mass == 1:
      return 'H';
   if mass == 2:
      return 'He';
   if mass == 6:
      return 'C';
   if mass == 7:
      return 'N';
   if mass == 8:
      return 'O';
   if mass == 9:
      return 'F';
   if mass == 10:
      return 'Ne';
   if mass == 16:
      return 'S';
   if mass == 17:
      return 'Cl';
   if mass == 18:
      return 'Ne';
   print('Unrecognised atom of mass: '+ str(mass))
   return 'u';

def main():
   f = open(i_file, 'r')
   c_group = 0
   while ReadTestData(f):
      if not PrepareTestData():
         continue;
      c_group += 1
      for sf in scaling_factors:
         for mer, ipos in zip(mmers, initpos):
            mer.place(ipos*sf)
         WriteTestData(mname[0]+'_'+str(sf)+'.mol')
   f.close()
   print('Process ended successfully.\n'+str(c_group)+' group(s), each in ' + str(len(scaling_factors)) + ' variations.')
   return;

if __name__ == "__main__":
   main()
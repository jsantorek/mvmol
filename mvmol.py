#!/usr/bin/python
import math
# input file:
# 1. No header, must start with 1st test
i_file = 'geometries.txt'
sh_file = '_ccsd.sh'
scaling_factors = [1.0]
# Headers to be written in all generated output files
o_header1 = 'BASIS\n'
o_header2 = 'aug-cc-pVDZ\n'
o_header3 = '\n'
o_header4 = '\n'
# Path and name for all output files
output_prefix = '_ccsd2/'


# Section for input file properties
file_keywordline_l = 2 # length of elements in line with keyword
file_keyword_name = 'name'
file_mass_i = 0   # index of mass of atom in a line of input
file_tag_i = 1    # index of tag for atom in a line of input
file_xpos_i = -3   # index of x position of atom in a line of input
file_ypos_i = -2   # index of y position of atom in a line of input
file_zpos_i = -1   # index of z position of atom in a line of input
file_test_separator = '*********************************************************\n'
file_monomer_separator = '---\n'
correction_factor = 1.889726

mmers = []
separs = []
mname = []

class Vector:
   def __init__(self, x=0, y=0, z=0):
      self.x = x
      self.y = y
      self.z = z
   def __add__(self,other):
      return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
   def __sub__(self,other):
      return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
   def __mul__(self,other):
        return Vector(self.x*other, self.y*other, self.z*other)
   def __truediv__(self,other):
        return Vector(self.x/other, self.y/other, self.z/other)
   def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)
   def __str__(self):
        return str(self.x) + ',' + str(self.y) + ',' + str(self.z)

class Molecule:
   tag_i = 0
   mass_i = 1
   pos_i = 2

   def __init__(self):
      self.Atoms = []
      self.CenterOfMass = Vector(0, 0, 0)

   def update(self):
      if len(self.Atoms) == 0:
         print('Errorous, empty atom group!');
         return;
      TempVector = Vector(0, 0, 0)
      TotalMass = 0.0
      for atom in self.Atoms:
         TotalMass += atom[Molecule.mass_i]
         TempVector += Vector(atom[Molecule.mass_i]*atom[Molecule.pos_i].x, 
            atom[Molecule.mass_i]*atom[Molecule.pos_i].y, atom[Molecule.mass_i]*atom[Molecule.pos_i].z)
      self.CenterOfMass = Vector(TempVector.x/TotalMass, TempVector.y/TotalMass, TempVector.z/TotalMass)

   def move(self, mvector):
      self.CenterOfMass += mvector
      for atom in self.Atoms:
         atom[Molecule.pos_i] += mvector

   def place(self, pvector):
      dvector = pvector - self.CenterOfMass
      self.move(dvector)

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
         adata[mmers[-1].tag_i] = ldata[file_tag_i] # better tags here
         adata[mmers[-1].pos_i] = Vector(
            float(ldata[file_xpos_i])*correction_factor, float(ldata[file_ypos_i])*correction_factor,
               float(ldata[file_zpos_i])*correction_factor )
         mmers[-1].Atoms.append(adata)
   return False;

def PrepareTestData():
   if len(mmers) < 2:
      print('Insufficient amount of groups for '+mname[0])
      return False;
   refpos = -mmers[0].CenterOfMass;
   prnt = math.sqrt((refpos.x*refpos.x) + (refpos.y*refpos.y) + (refpos.z * refpos.z))
   print(prnt)
   for mer in mmers:
      mer.move(refpos)
   for mer in mmers:
      separs.append(mer.CenterOfMass)
   return True;

def WriteTestData(filename):
   atoms = []
   temp = 0
   cnt = 0
   for mer in mmers:
      atoms.extend(mer.Atoms)
   atoms.sort(key=lambda x: x[Molecule.mass_i])
   f = open(output_prefix + filename, 'w')
   f.write(o_header1)
   f.write(o_header2)
   f.write(o_header3)
   f.write(o_header4)
   f.write('Atomtypes={at} Charge=0 Nosymmetry Cartesian\n'.format(
      at=len(set(a[Molecule.mass_i] for a in atoms)) )) # counts unique masses of atoms

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
   return '';

def main():
   f = open(i_file, 'r')
   sh = open(output_prefix + sh_file, 'w')
   sh.write('#!/bin/sh\n')
   while ReadTestData(f):
      if not PrepareTestData():
         continue;
      sh.write('\n')
      for sf in scaling_factors:
         for mer, sep in zip(mmers[1:], separs[1:]):
            mer.place(sep*sf)
         tname = mname[0]+'_'+str(sf)+'.mol'
         WriteTestData(tname)
         sh.write(
            '/pbs_home/hjaajensen/progs/gitDalton/build_apsg/dalton -dal _ccsd.dal -mol '+tname+'\n'
            )
   sh.close();
   f.close()
   return;

if __name__ == "__main__":
   main()
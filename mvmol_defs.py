

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

#correction_factor = 1.889726 
correction_factor = 1

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

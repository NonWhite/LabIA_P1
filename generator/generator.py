from random import randint
import sys

class Generator :
	def __init__( self ) :
		self.clearValues()

	def clearValues( self ) :
		self.setValues()
	
	def setValues( self , num_atoms = 0 , num_clausulas = 0 , num_literais = 0 ) :
		self.N = num_atoms
		self.M = num_clausulas
		self.K = num_literais
		self.currentClauses = {}
		self.data = []
		self.maxcode = 1000000007
		self.top = 0
	
	def mod( self , a ) : return ( a % self.maxcode + self.maxcode ) % self.maxcode
	def add( self , a , b ) : return self.mod( self.mod( a ) + self.mod( b ) )
	def mult( self , a , b ) : return self.mod( self.mod( a ) * self.mod( b ) )

	def hashcode( self , clause ) :
		base = self.N * 2
		hashing = 0
		for c in clause : hashing = self.add( self.mult( hashing , base ) , self.add( c , self.N ) )
		#print 'clause = %s' % clause
		#print 'hash = %s' % hashing
		return hashing

	def addClause( self , clause ) :
		self.currentClauses[ self.hashcode( clause ) ] = True

	def generateClause( self ) :
		clause = []
		ishard = randint( 0 , 1 )
		weight = ( self.M * self.M if ishard == 1 else randint( 1 , self.M ) )
		self.top = max( self.top , weight )
		while True :
			clause = []
			currentLiterals = {}
			for p in range( self.K ) :
				while True :
					sign = randint( 0 , 1 )
					atom = randint( 1 , self.N )
					atom = ( 1 if sign == 0 else -1 ) * atom
					if atom in currentLiterals : continue
					else : break
				currentLiterals[ atom ] = True
				clause.append( atom )
			if self.hashcode( clause ) in self.currentClauses : continue
			else : break
		self.addClause( clause )
		clause.insert( 0 , weight )
		return clause
	
	# num_atoms: N , num_clauses: M , num_literals: K
	def generateAleatoryData( self , num_atoms , num_clauses , num_literals ) :
		self.setValues( num_atoms , num_clauses , num_literals )
		for i in range( num_clauses ) :
			clause = self.generateClause()
			self.data.append( clause )
	
	def saveData( self , name = None ) :
		if name == None : name = 'maxsat_%ssat_%sat_%scl.wcnf' % ( self.K , self.N , self.M )
		f = open( name , 'w' )
		f.write( 'p wcnf %s %s %s\n' % ( self.N , self.M , self.top ) )
		for clause in self.data :
			for at in clause : f.write( '%s ' % at )
			f.write( '0\n' )

if __name__ == "__main__" :
	if len( sys.argv ) < 5 :
		print "usage: %s NUM_ATOMS NUM_CLAUSES NUM_LITERALS OUTPUT_FILE" % sys.argv[ 0 ]
		sys.exit( 2 )
	else :
		num_atoms = int( sys.argv[ 1 ] )
		num_clauses = int( sys.argv[ 2 ] )
		num_literals = int( sys.argv[ 3 ] )
		output = sys.argv[ 4 ]
		g = Generator()
		g.generateAleatoryData( num_atoms , num_clauses , num_literals )
		g.saveData( output )
		sys.exit( 0 )

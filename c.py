import sys
import os
import utils
import time
from functools import partial
from multiprocessing.dummy import Pool
from subprocess import call
from subprocess import Popen
from daemon import Daemon

class Turing( Daemon ) :
	# Parametros de configuracion generales del demonio
	config = {
		'max_process_in': 50 ,
		'max_process_out': 5 ,
		'location' : os.environ[ 'P1_HOME' ] ,
		'dirs': [ 'data/max2sat_100at/' ] * 80 ,
		'num_literals' : 2 ,
		'atoms' : [ 100 ] ,
		'rel_mn' : utils.frange( 0.1 , 8.0 , 0.1 ) ,
		'files_per_conf' : 100 ,
		'call_generator' : 'python generator/generator.py' ,
		'call_maxsatsolver' : 'sh maxsatsolver.sh' ,
		'maxsatsolver_timeout' : 1800
	}
	
	def initialize( self ) :
		self.atoms = Turing.config[ 'atoms' ]
		self.clauses_rel = Turing.config[ 'rel_mn' ]
		self.dirs = Turing.config[ 'dirs' ]
		self.iters = Turing.config[ 'files_per_conf' ]
		self.K = Turing.config[ 'num_literals' ]
		self.process = self.inFiles = []

	def generateInFiles( self ) :
		start_time = time.time()
		self.inFiles = []
		for i in range( len( self.atoms ) ) :
			N = self.atoms[ i ]
			for j in range( len( self.clauses_rel ) ) :
				rel = self.clauses_rel[ j ]
				M = int( N * rel )
				direc = self.dirs[ j ]
				for it in range( 1 , self.iters + 1 ) :
					num = ( "00%s" % it if it < 10 else ( "0%s" % it if it < 100 else "%s" % it ) )
					m = ( "00%s" % M if M < 10 else ( "0%s" % M if M < 100 else "%s" % M ) )
					infile = direc + "in/%scl_%s.wcnf" % ( m , num )
					self.inFiles.append( { 'infile': infile , 'N': N , 'M': M , 'K': self.K } )
		files = list( self.inFiles )
		self.process = []
		while len( files ) > 0 or len( self.process ) > 0 :
			for f in files :
				if len( self.process ) >= Turing.config[ 'max_process_in' ] : continue
				files.remove( f )
				if os.path.isfile( f[ 'infile' ] ) : continue
				params = Turing.config[ 'call_generator' ].split()
				params.append( str( f[ 'N' ] ) )
				params.append( str( f[ 'M' ] ) )
				params.append( str( f[ 'K' ] ) )
				params.append( f[ 'infile' ] )
				self.process.append( Popen( params ) )
				
			for proc in self.process :
				retcode = proc.poll()
				if retcode is not None :
					self.process.remove( proc )
		print "T. de generacion: %s segundos" % ( time.time() - start_time )
		time.sleep( 5 )
	
	def processInFiles( self ) :
		start_time = time.time()
		self.process = []
		home = Turing.config[ 'location' ]
		while len( self.inFiles ) > 0 or len( self.process ) > 0 :
			for f in self.inFiles :
				if len( self.process ) >= Turing.config[ 'max_process_out' ] : continue
				params = Turing.config[ 'call_maxsatsolver' ].split()
				params.append( '--timeout=%s' % Turing.config[ 'maxsatsolver_timeout' ] )
				params.append( home + "/" + f[ 'infile' ] )
				outname = home + "/" + f[ 'infile' ].replace( 'in' , 'out' ).replace( 'wcnf' , 'txt' )
				self.inFiles.remove( f )
				if os.path.isfile( outname ) : continue
				outfile = open( outname , 'w' )
				self.process.append( Popen( params , stdout = outfile ) )

			for proc in self.process :
				retcode = proc.poll()
				if retcode is not None :
					self.process.remove( proc )
		print "T. de maxsatsolver: %s segundos" % ( time.time() - start_time )

	def run( self ) :
		self.initialize()
		self.generateInFiles()
		self.processInFiles()

if __name__ == "__main__" :
	turing = Turing( 'b.pid' )
	if( len( sys.argv ) == 2 ) :
		if( sys.argv[ 1 ] == 'start' ) : turing.start()
		elif( sys.argv[ 1 ] == 'stop' ) : turing.stop()
		elif( sys.argv[ 1 ] == 'restart' ) : turing.restart()
		else :
			print "Unknown command"
			sys.exit( 2 )
		sys.exit( 0 )
	else :
		print "usage: %s start|stop|restart" % sys.argv[ 0 ]
		sys.exit( 2 )

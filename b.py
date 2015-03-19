import sys
import os
import utils
from functools import partial
from multiprocessing.dummy import Pool
from subprocess import call
from subprocess import Popen
from daemon import Daemon

class Turing( Daemon ) :
	# Parametros de configuracion generales del demonio
	config = {
		'max_process': 50 ,
		'dirs': [ 'data/max3sat_100at/' ] * 80 ,
		'num_literals' : 3 ,
		'atoms' : [ 100 ] ,
		'rel_mn' : utils.frange( 0.1 , 8.0 , 0.1 ) ,
		'files_per_conf' : 100 ,
		'call_generator' : 'python generator/generator.py' ,
		'call_maxsatsolver' : './toysat'
	}
	
	def initialize( self ) :
		self.atoms = Turing.config[ 'atoms' ]
		self.clauses_rel = Turing.config[ 'rel_mn' ]
		self.dirs = Turing.config[ 'dirs' ]
		self.iters = Turing.config[ 'files_per_conf' ]
		self.K = Turing.config[ 'num_literals' ]
		self.process = self.inFiles = []

	def getInFiles( self ) :
		info = utils.getAllFromPath( self.location )
		files = info[ 1 ]
		for f in files :
			ext = os.path.splitext( f )[ 1 ]
			if( ext in self.extensions ) :
				self.initializeArchivo( f , ext )

	def generateInFiles( self ) :
		# TODO: Agregar timer de duracion de generacion de datos
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
					#print "N = %s , M = %s , FILE = %s" % ( N , M , infile )
		files = self.inFiles
		self.process = []
		while len( files ) > 0 :
			for f in files :
				if len( self.process ) >= Turing.config[ 'max_process' ] : continue
				params = Turing.config[ 'call_generator' ].split()
				params.append( str( f[ 'N' ] ) )
				params.append( str( f[ 'M' ] ) )
				params.append( str( f[ 'K' ] ) )
				params.append( f[ 'infile' ] )
				self.process.append( Popen( params ) )
				files.remove( f )
				
			for proc in self.process :
				retcode = proc.poll()
				if retcode is not None :
					self.process.remove( proc )
	
	def processInFiles( self ) :
		# TODO: Agregar timer de duracion de procesado de datos
		self.process = []
		while len( self.inFiles ) > 0 :
			for f in self.inFiles :
				if len( self.process ) >= Turing.config[ 'max_process' ] : continue
				params = Turing.config[ 'call_maxsatsolver' ].split()
				# TODO: agregar llamada a proceso
				self.inFiles.remove( f )

			for proc in self.process :
				retcode = proc.poll()
				if retcode is not None :
					self.process.remove( proc )

	def run( self ) :
		self.initialize()
		#self.generateInFiles()
		self.processInFiles()
		#while True :
			#files = self.inFiles
			#for f in files :
				#if( len( self.process ) >= Turing.config[ 'max_process' ] ) : continue
				#params = etapa[ 'nombreproceso' ].split()
				#params.append( f[ 'nombrearchivo' ] )
				#self.data.append( { 'archivo': f , 'etapa' : etapa } )
				#self.process.append( Popen( params ) )


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
import sys
import os
import utils
import time
from daemon import Daemon

class Turing( Daemon ) :
	# Parametros de configuracion generales del demonio
	config = {
		'location' : os.environ[ 'P1_HOME' ] + '/data' ,
		'out_dir' : 'out' ,
		'stats_dir' : 'stats' ,
		'parameters' : { '#vars': 'atoms' , '#constraints' : 'clauses' , 'total CPU time' : 'time' , 's ' : 'status' }
	}
	
	def initialize( self ) :
		return 'init'

	def parse( self , line , filt ) :
		line = line.replace( '\n' , '' )
		line = line.replace( 'M F' , 'M_F' )
		line = line.rpartition( ' ' )[ -1 ]
		return line

	def extractDataFromFile( self , path ) :
		parameters = Turing.config[ 'parameters' ]
		filters = parameters.keys()
		data = { 'location' : path.replace( Turing.config[ 'location' ] , '' ) }
		lines = open( path , 'r' ).readlines()
		for l in lines :
			for filt in filters :
				if l.find( filt ) < 0 : continue
				data[ parameters[ filt ] ] = self.parse( l , filt )
		if data[ 'status' ][ 0 ] != 'U' and  data[ 'status' ][ 0 ] != 'O' : print data # only for verification
		return data

	def filterFiles( self ) :
		start_time = time.time()
		home = Turing.config[ 'location' ]
		dirs = os.walk( home ).next()[ 1 ]
		for d in dirs :
			dpath = home + '/' + d
			subdirs = os.walk( dpath ).next()[ 1 ]
			for sub in subdirs :
				if sub != Turing.config[ 'out_dir' ] : continue
				spath = dpath + '/' + sub
				files = os.walk( spath ).next()[ 2 ]
				contador = 0
				stats = {}
				for f in files :
					fpath = spath + '/' + f
					data = self.extractDataFromFile( fpath )
					key = ( data[ 'atoms' ] , data[ 'clauses' ] )
					if not key in stats : stats[ key ] = []
					data.pop( 'atoms' , None )
					data.pop( 'clauses' , None )
					stats[ key ].append( data )
					# TODO: Create a file with stats per key
					contador += 1
				print "Cant. archivos en %s: %s" % ( spath , contador )
		print "T. de stats: %s segundos" % ( time.time() - start_time )
		#print "%s archivos eliminados" % contador

	def run( self ) :
		self.initialize()
		self.filterFiles()

if __name__ == "__main__" :
	turing = Turing( 'stats.pid' )
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

import sys
import os
import utils
import time
from daemon import Daemon

class Turing( Daemon ) :
	# Parametros de configuracion generales del demonio
	config = {
		'location' : os.environ[ 'P1_HOME' ] + '/data' ,
		'subdirs' : [ 'out' ] ,
		'filters' : [ 'TIMEOUT' ]
	}
	
	def initialize( self ) :
		return 'init'

	def filterFiles( self ) :
		start_time = time.time()
		home = Turing.config[ 'location' ]
		dirs = os.walk( home ).next()[ 1 ]
		filters = Turing.config[ 'filters' ]
		contador = 0
		for d in dirs :
			dpath = home + '/' + d
			subdirs = os.walk( dpath ).next()[ 1 ]
			for sub in subdirs :
				if not sub in Turing.config[ 'subdirs' ] : continue
				spath = dpath + '/' + sub
				print spath
				files = os.walk( spath ).next()[ 2 ]
				for f in files :
					fpath = spath + '/' + f
					test = open( fpath ).read()
					for filt in filters :
						if test.find( filt ) < 0 : continue
						print "Eliminando %s" % fpath
						os.remove( fpath )
						contador += 1
		print "T. de cleaner: %s segundos" % ( time.time() - start_time )
		print "%s archivos eliminados" % contador

	def run( self ) :
		self.initialize()
		self.filterFiles()

if __name__ == "__main__" :
	turing = Turing( 'cleaner.pid' )
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

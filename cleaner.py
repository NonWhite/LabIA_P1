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
		'good_filters' : [ 'UNSATIS' , 'OPTIMUM' ] , # At least one of this
		'bad_filters' : [ 'TIMEOUT' ] # No one of this
	}
	
	def initialize( self ) :
		return 'init'

	def isOk( self , path ) :
		have_bad = have_good = False
		good_f = Turing.config[ 'good_filters' ]
		bad_f = Turing.config[ 'bad_filters' ]
		with open( path ) as f :
			for line in f :
				if have_bad : break
				if have_good : break
				for filt in bad_f :
					if line.find( filt ) < 0 : continue
					have_bad = True
					break
				for filt in good_f :
					if line.find( filt ) < 0 : continue
					have_good = True
					break
		return have_good and not have_bad

	def filterFiles( self ) :
		start_time = time.time()
		home = Turing.config[ 'location' ]
		dirs = os.walk( home ).next()[ 1 ]
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
					if not self.isOk( fpath ) :
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

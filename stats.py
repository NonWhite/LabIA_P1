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

	def saveStats( self , path , stats ) :
		f = open( path + '/stats.txt' , 'w' )
		staticIdField = ( 1 if path.find( 'mn' ) < 0 else 0 )
		staticField = [ "Atoms" , "Clauses" ]
		lst_stats = []
		for key in stats :
			lst = stats[ key ]
			countFiles = 0.0
			totalFiles = ( 100.0 if staticIdField == 1 else 10.0 )
			optimumFiles = 0.0
			totalTime = 0.0
			for prop in lst :
				if prop[ 'status' ].find( 'OPTIMUM' ) >= 0 : optimumFiles += 1
				countFiles += 1
				totalTime += float( prop[ 'time' ][ :-1 ] )
			# ( clauses or atoms , opt_files , total_files , percentage , time )
			lst_stats.append( ( int( key[ staticIdField ] ) , optimumFiles , totalFiles , 100.0 * ( optimumFiles / totalFiles ) , ( totalTime / countFiles ) ) )
		lst_stats = sorted( lst_stats , key = lambda st : st[ 0 ] )
		for x in lst_stats :
			f.write( "%s: %s\n" % ( staticField[ staticIdField ] , x[ 0 ] ) )
			f.write( "Optimum: %s\n" % x[ 1 ] )
			f.write( "Total: %s\n" % x[ 2 ] )
			f.write( "Percentage: %s\n" % x[ 3 ] )
			f.write( "Time: %s\n" % x[ 4 ] )
			f.write( "\n" )

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
					#data.pop( 'atoms' , None )
					#data.pop( 'clauses' , None )
					#print data
					stats[ key ].append( data )
					# TODO: Create a file with stats per key
					contador += 1
				print "Cant. archivos en %s: %s" % ( spath , contador )
			self.saveStats( dpath , stats )
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

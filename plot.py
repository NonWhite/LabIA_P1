import sys
import os
import utils
import time
import matplotlib.pyplot as plt
from daemon import Daemon

class Turing( Daemon ) :
	# Parametros de configuracion generales del demonio
	config = {
		'location' : os.environ[ 'P1_HOME' ] + '/data' ,
		'stats_filename' : 'stats.txt' ,
	}
	
	def initialize( self ) :
		return 'init'

	def doAndSavePlot( self , stats , filename , directory ) :
		if directory.find( 'mn' ) < 0 :
			x = [ cl[ 'Clauses' ] for cl in stats ]
			x.insert( 0 , 0 )
			y1 = [ cl[ 'Time' ] for cl in stats ]
			y1.insert( 0 , 0 )
			y2 = [ float( cl[ 'Percentage' ] ) for cl in stats ]
			y2.insert( 0 , 100.0 )

			fig , ax1 = plt.subplots()

			ax2 = ax1.twinx()
			ax1.plot( x , y1 , 'b-' )
			ax2.plot( x , y2 , 'r-' )

			ax1.set_xlabel('Numero de clasulas (M)')
			ax1.set_ylabel('Tempo (segundos)', color='blue')
			ax2.set_ylabel('Percentagem (%)', color='red')

			plt.savefig( directory + "/" + filename )
		else :
			x = [ cl[ 'Atoms' ] for cl in stats ]
			x.insert( 0 , 0 )
			y = [ cl[ 'Time' ] for cl in stats ]
			y.insert( 0 , 0 )

			plt.xlabel( 'Numero de atomos (N)' )
			plt.ylabel( 'Tempo (segundos)' )

			plt.plot( x , y , 'b-' )
			plt.savefig( directory + "/" + filename )
		plt.clf()
		return 'init'

	def extractStats( self , dpath ) :
		filename = Turing.config[ 'stats_filename' ]
		lst_lines = open( dpath + "/" + filename , 'r' ).readlines()
		lst_stats = []
		for i in range( 0 , len( lst_lines ) , 6 ) :
			stats = {}
			for j in range( 5 ) :
				line = lst_lines[ i + j ].strip()
				( field , value ) = line.split( ': ' )
				stats[ field ] = value
			lst_stats.append( stats )
		return lst_stats
				

	def plotStats( self ) :
		start_time = time.time()
		home = Turing.config[ 'location' ]
		dirs = os.walk( home ).next()[ 1 ]
		for d in dirs :
			dpath = home + '/' + d
			stats = self.extractStats( dpath )
			self.doAndSavePlot( stats , 'plot.pdf' , dpath )
		print "T. de stats: %s segundos" % ( time.time() - start_time )

	def run( self ) :
		self.initialize()
		self.plotStats()

if __name__ == "__main__" :
	turing = Turing( 'plot.pid' )
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

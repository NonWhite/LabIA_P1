import pip
import MySQLdb as mysql
import sys
import os
import shutil
import itertools
import time
import datetime
from mybd import MyBD
from functools import partial
from multiprocessing.dummy import Pool
from subprocess import call
from subprocess import Popen

sys.path.insert( 0 , '../' )
from daemon import Daemon
import utils

class Turing( Daemon ) :
	# Parametros de configuracion generales del demonio
	config = {
		'max_process': 50
		'home': os.environ[ "IME_HOME" ]
	}
	
	def initialize( self ) :
		self.location = Turing.config[ 'home' ]
		self.process = []

	# Retorna los archivos que aun no terminan de procesarse (todas las etapas)
	def initializeArchivo( self , fileName , extension ) :
		return 'gg'
		#newName = utils.generateName( fileName )
		#os.makedirs( newName )
		#os.rename( fileName , newName + extension )
		#shutil.move( newName + extension , newName )
		#reg = { 'nombrearchivo' : newName + '/' + newName + extension ,
		#			'estado' : 0 } 
		#self.bd.insert( 'archivo' , reg )

	def getInFiles( self ) :
		info = utils.getAllFromPath( self.location )
		files = info[ 1 ]
		for f in files :
			ext = os.path.splitext( f )[ 1 ]
			if( ext in self.extensions ) :
				self.initializeArchivo( f , ext )

	def run( self ) :
		self.initialize()
		while True :
			files = self.getInFiles()
			for f in files :
				if( len( self.process ) >= Turing.config[ 'max_process' ] ) : continue
				params = 
				#params = etapa[ 'nombreproceso' ].split()
				#params.append( f[ 'nombrearchivo' ] )
				#self.data.append( { 'archivo': f , 'etapa' : etapa } )
				self.process.append( Popen( params ) )

			for proc in self.process :
				retcode = proc.poll()
				pos = self.process.index( proc )
				if retcode is not None :
					data = self.data[ pos ]
					self.process.remove( proc )
					#self.data.remove( data )

if __name__ == "__main__" :
	turing = Turing( 'turing.pid' )
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

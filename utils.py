def frange( start , end , increment ) :
	data = []
	pos = start
	while pos <= end :
		data.append( int( round( pos , 2 ) * 100.0 ) / 100.0 )
		pos += increment
	return data

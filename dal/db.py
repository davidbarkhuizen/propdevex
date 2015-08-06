import psycopg2

def db_connection_factory(host, database, user, password):

	def generate():

		connection = psycopg2.connect(
			host=host, 
			database=database, 
			user=user, 
			password=password
			)

		def fetchone(sql):
			cursor = connection.cursor()
			cursor.execute(sql)          
			return cursor.fetchone()

		def fetchall(sql):
			cursor = connection.cursor()
			cursor.execute(sql)          
			return cursor.fetchall()

		def execute(sql):
			cursor = connection.cursor()
			cursor.execute(sql)          
			connection.commit()

		def close():
			if connection is not None:
				connection.close()

		class Connection(object):
			
			def fetchone(self, sql):
				return fetchone(sql)
			def fetchall(self, sql):
				return fetchall(sql)
			def execute(self, sql):
				return execute(sql)
			def close(self):
				close()

		return Connection()

	return generate
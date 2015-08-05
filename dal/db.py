import psycopg2

def connection_factory(host, database, user, password):

	def generate():

		connection = psycopg2.connect(
			host=cls.host, 
			database=cls.database, 
			user=cls.user, 
			password=cls.password
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

		def exit():
			if connection is not None:
				connection.close()

		class Connection(object):
			
			def fetchone(self, sql):
				fetchone(sql)
			def fetchall(self, sql):
				fetchall(sql)
			def execute(self, sql):
				execute(sql)
			def close(self):
				close(sql)

		return connxn

	return generate
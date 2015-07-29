from dbconnection import DBConnection

class Site(object):

	@classmethod
	def truncate(cls):
		db = DBConnection.get_connection()
		db.execute('truncate table site;')
		db.terminate()

	@classmethod
	def get_ids_of_sites_needing_to_be_updated(cls):

		sql = 'select id from site where updated = false;'
		db_connxn = DBConnection.get_connection()
		ids = [row[0] for row in db_connxn.fetchall(sql)]		
		db_connxn.terminate()
		return ids

	@classmethod
	def 

		ftp_host 				= models.CharField(max_length=1024, unique=True, null=False)
	ftp_port 				= models.IntegerField(null=False)
	ftp_user 				= models.CharField(max_length=1024, unique=True, null=False)
	ftp_password			= models.CharField(max_length=1024, unique=True, null=False)
	ftp_account				= models.CharField(max_length=1024, unique=True, null=False)
	ftp_secure				= models.BooleanField(default=False, null=False)

	@classmethod
	def increment_activation_token_distribution_try_count_for_email(cls, email):

		sql = '''
		update "user"
		set activation_token_distribution_try_count = activation_token_distribution_try_count + 1
		where email = '{0}'
		;'''.format(str(email))

		db_connxn = DBConnection.get_connection()
		print(sql)	
		db_connxn.execute(sql)
		db_connxn.close()

	@classmethod
	def set_activation_token_distributed_for_email(cls, email):

		sql = '''
		update "user"
		set activation_token_distributed = now()
		where (email = '{0}') 
		;'''.format(email)

		db_connxn = DBConnection.get_connection()
		db_connxn.execute(sql)
		db_connxn.close()

	@classmethod
	def select_emailuuid_for_undistributed(cls, max_retry_count = 3):

		sql = '''
		select email, uuid 
		from "user"
		where
			(
			(activation_token_distributed is null)
			and
			(activation_token_distribution_try_count < {0})
			)
		;'''.format(str(max_retry_count))

		db_connxn = DBConnection.get_connection()

		data = []
		rows = db_connxn.fetchall(sql)
		for row in rows:
			
			email = row[0]
			uuid = row[1]

			datum =  { 'uuid' : uuid, 'email' : email }
			data.append(datum)

		return data
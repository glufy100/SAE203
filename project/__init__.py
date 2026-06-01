try:
	# If PyMySQL is installed, make it act as MySQLdb for Django
	import pymysql
	pymysql.install_as_MySQLdb()
except Exception:
	# No PyMySQL available or failed to initialize; continue silently
	pass



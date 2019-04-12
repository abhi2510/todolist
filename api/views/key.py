import hashlib
class Key:
	def __init__(self):
		self.secretkey = 'VNr4286XmUkKGt9D'

	def encrypt_data(self,data):
		data = str(data)+self.secretkey
		hashdata = hashlib.sha256(data.encode('utf-8')).hexdigest()
		return hashdata[0:30]

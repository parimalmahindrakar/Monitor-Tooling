from pexpect import pxssh
import pexpect
import os
import json
import ssl
import pymysql
import re



class MonitorToolManage2():
	sender, passwordGmail = "nightfury4653@gmail.com", "Ambition@gmail18"
	subjectForRam = "About Used Ram."
	context = ssl.create_default_context()
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))

	def __init__(self, ip, host, password,  uniqueNum):
		self.hsh = uniqueNum
		self.ip = ip
		self.host = host
		self.password = password
		self.obj = pxssh.pxssh()
		self.f = open(f"{MonitorToolManage2.BASE_DIR}/%s.txt" % self.hsh, "w")
		self.loginHost()
		self.sendRequiredPythonFile()
		self.executionDeletionSentFile()
		self.closeConnections()
		self.mysqlConnectionsStart()

	def loginHost(self):
		self.obj.login(self.ip, self.host, self.password)

	def sendRequiredPythonFile(self):
		tempChannel = pexpect.spawn(
			f'scp {MonitorToolManage2.BASE_DIR}/destination2.py {self.host}@{self.ip}:/home/{self.host}/Desktop')
		tempChannel.expect('assword:')
		tempChannel.sendline(self.password)
		tempChannel.expect(pexpect.EOF)

	def executionDeletionSentFile(self):
		self.obj.sendline(f"python3 /home/{self.host}/Desktop/destination2.py")
		self.obj.prompt()
		self.to_write = self.obj.before.decode()
		self.obj.sendline(f"rm -rf /home/{self.host}/Desktop/destination2.py")

	def closeConnections(self):
		self.obj.logout()
		self.obj.close()
		self.f.write(self.to_write)

	def mysqlConnectionsStart(self):
		self.con = pymysql.connect(host="localhost", user="root", password="")
		self.cursor = self.con.cursor()
		self.cursor.execute("use RAM")

	def mysqlConnectionsEnd(self):
		self.cursor.close()
		self.con.close()

	def func1(self, Tuple):
		count = 0
		for i in Tuple:
			if i[1] > self.threshPercent:
				count += 1
		if count == len(Tuple) and count == self.cnt:
			print("Count is overloaded")

	def storeInfo(self):
		self.f = open("./%s.txt" % self.hsh, "r")
		file_ = open('machineInfo%s.txt' % self.hsh, 'w')
		for line in self.f:
			data1 = re.search("^{", line)
			if data1 != None:
				file_.write(line)
		self.f.close()

	def sendRAMmail(self, cnt, threshPercent):
		self.f = open("%s.txt" % self.hsh, "r")
		self.cnt = cnt
		self.threshPercent = threshPercent
		# print(self.f.read())
		dataList = []
		for line in self.f:
			data1 = re.search("^{", line)
			if data1 != None:
				dataList.append(line)
		self.allDct = {}
		for i in range(len(dataList)):
			self.allDct['dict_%s' % i] = json.loads(dataList[i])

		try:
			self.query = "create table statusRAM%s(id INT NOT NULL AUTO_INCREMENT,RAMval integer (15),primary key (id));" % self.hsh
			self.cursor.execute(self.query)
			self.con.commit()
		except:
			pass

		RAM_PERCENT = self.allDct['dict_0'].get('virtualMemoryPercent')
		print(RAM_PERCENT)
		self.query = "insert into statusRAM%s(RAMval) values(%d);" % (
			self.hsh, RAM_PERCENT)
		self.cursor.execute(self.query)
		self.con.commit()
		self.cursor.execute("select * from statusRAM%s" % self.hsh)
		self.con.commit()
		data = self.cursor.fetchall()
		print(data)
		self.func1(data)
		if len(data) == self.cnt:
			lastID = data[-1][0]
			removeID = lastID-(self.cnt-1)
			self.query = "delete from statusRAM%s where id=%d" % (self.hsh, removeID)
			self.cursor.execute(self.query)
			self.con.commit()
		file = "%s.txt" % self.hsh
		# os.system(f"rm -rf {file}")


# a = MonitorToolManage2('127.0.0.1', 'light', 'l', 'parimalm4653@gmail.com', 6)
# a.storeInfo()
# a.sendRAMmail(5, 35)
# self,cnt,threshPercent


##################################
#  dict_1 is for virtual memory
#  dict_2 is for disk usage
#  dict_3 is for battery percent
#  dict_4 is for user recognition

# *****************************
#  virtual memory contains attributes like,
#  'cpuCountLogical','virtualMemoryTotal', 'virtualMemoryAvailable',
#  'virtualMemoryPercent''virtualMemoryUsed', 'virtualMemoryFree'
# *****************************

# *****************************
#  disk usage contains attributes like,
# 'diskUsageTotal','diskUsageUsed', 'diskUsageFree', 'diskUsagePercent'
# *****************************

# *****************************
#  battery percent contains attributes like,
# 'batteryPercent', 'isPowerPluged'
# *****************************

# *****************************
# username contains attributes like,
# 'username'
# *****************************
# self.allDct['dict_1'].get('virtualMemoryPercent')

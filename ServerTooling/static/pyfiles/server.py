from pexpect import pxssh
import pexpect
import os
import pymysql
import textwrap


class MonitorToolManage():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, ip, host, password, command_, num):

        self.ip = ip
        self.host = host
        self.password = password
        self.command_ = command_
        self.obj = pxssh.pxssh()
        self.num = num
        self.loginHost()
        self.writeToFile()
        self.sendRequiredPythonFile()
        self.executionDeletionSentFile()
        self.closeConnections()
        self.mysqlConnectionsStart()
        self.deleteAllFiles()

    def loginHost(self):
        self.obj.login(self.ip, self.host, self.password)

    def writeToFile(self):
        a = f'''
		import subprocess
		command_ = "{self.command_}"
		a = subprocess.run(command_,shell=True,capture_output=True)
		print(a.stdout.decode())'''
        text_without_Indentation = textwrap.dedent(a)
        with open(f"{MonitorToolManage.BASE_DIR}/destination.py", "w") as f:
            f.write(text_without_Indentation)

    def sendRequiredPythonFile(self):
        tempChannel = pexpect.spawn(
            f'scp {MonitorToolManage.BASE_DIR}/destination.py {self.host}@{self.ip}:/home/{self.host}/Desktop')
        tempChannel.expect('assword:')
        tempChannel.sendline(self.password)
        tempChannel.expect(pexpect.EOF)

    def executionDeletionSentFile(self):
        self.obj.sendline(f"python3 /home/{self.host}/Desktop/destination.py")
        self.obj.prompt()
        self.to_write = self.obj.before.decode()
        self.obj.sendline(f"rm -rf /home/{self.host}/Desktop/destination.py")

    def closeConnections(self):
        self.obj.logout()
        self.obj.close()

    def mysqlConnectionsStart(self):
        self.con = pymysql.connect(host="localhost", user="root", password="")
        self.cursor = self.con.cursor()
        self.cursor.execute("use RAM")

    def mysqlConnectionsEnd(self):
        self.cursor.close()
        self.con.close()

    def deleteAllFiles(self):
        os.system('rm -rf destination.py')

    def getCommandInfo(self) :
        return self.to_write


# self, ip, host, password,command_,num

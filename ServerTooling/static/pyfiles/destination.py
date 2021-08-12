
import subprocess
command_ = "ls"
a = subprocess.run(command_,shell=True,capture_output=True)
print(a.stdout.decode())
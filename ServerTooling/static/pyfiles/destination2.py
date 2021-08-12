import subprocess
import os
import json
import datetime

try:
	import psutil
except ImportError as e:
	try:
		os.system("pip3 install psutil")
		os.system("python3 destination.py")
	except:
		try:
			os.system("pip install psutil")
			os.system("python3 destination.py")
		except:
			os.system("sudo apt-get install python3-pip")
			os.system("python3 destination.py")



cpuCountLogical = psutil.cpu_count()
cpuCountNotLogical = psutil.cpu_count(logical=False)

virtualMemory = psutil.virtual_memory()
diskUsage = psutil.disk_usage('/')

batteryPercent = psutil.sensors_battery()
usersSystem = psutil.users()

virtulaMemDictionary = {
    "cpuCountLogical": cpuCountLogical,
				"virtualMemoryTotal": virtualMemory.total,
				'virtualMemoryAvailable': virtualMemory.available,
				'virtualMemoryPercent': virtualMemory.percent,
				'virtualMemoryUsed': virtualMemory.used,
				'virtualMemoryFree': virtualMemory.free
}

diskUsageDictionary = {
    "diskUsageTotal": diskUsage.total,
				"diskUsageUsed": diskUsage.used,
				"diskUsageFree": diskUsage.free,
				"diskUsagePercent": diskUsage.percent
}

batteryPercentDictionary = {
    "batteryPercent": batteryPercent.percent,
				"isPowerPluged": batteryPercent.power_plugged
}

usersSystemDictionary = {
    "username": usersSystem[0].name
}


print(json.dumps(virtulaMemDictionary))
print(json.dumps(diskUsageDictionary))
print(json.dumps(batteryPercentDictionary))
print(json.dumps(usersSystemDictionary))

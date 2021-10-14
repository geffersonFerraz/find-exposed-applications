import datetime
import os
import requests
import json
import nmap3 #pip3 install python3-nmap

# UTIL VARS
vVPN = True
now = datetime.datetime.now()
nmap = nmap3.NmapHostDiscovery()


try:
    r = requests.get("http://peoplesoft.local.intranet:8000/")
except:
    vVPN = False

modeInput = 'r' if os.path.exists("input.txt") else 'a+'
inputFile = open("input.txt", modeInput)
outputFile = open("output.txt", "a+")

dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
if vVPN:
    header = "\r\n\r\n" + dt_string +" - VPN: CONECTADA\r\n"
else:
    header = "\r\n\r\n" + dt_string + " - VPN: DESCONECTADA\r\n"

outputFile.writelines(header)

num_lines = sum(1 for line in open('input.txt'))
now_line = 0
for line in inputFile.readlines():
    now_line = now_line + 1
    firstLine = "\r\n\r\n - "
    secondLine = "\r\n - "
    thirdLine = "\r\n = "
    httpDomain = line.split('/', 1)[0][0:].strip()
    httpUrl = "http://" + line.strip()
    httpsUrl = "https://" + line.strip()
    print(str(now_line) + " of " + str(num_lines) +" - "+ httpDomain)

    try:
        firstLine = firstLine + httpUrl + " -> "
        r = requests.get(httpUrl, allow_redirects=False)
        firstLine = firstLine + str(r.status_code)
        if (r.status_code == 301):
            r = requests.get(httpUrl, allow_redirects=True)
            firstLine = firstLine + " = "
            data = json.dumps(r.json())
            firstLine = firstLine + data
        else:
            if (r.status_code == 301):
                r = requests.get(httpUrl, allow_redirects=True)
                firstLine = firstLine + " = "
                firstLine = firstLine + str(r.content)
            else:
                firstLine = firstLine + " = "
                data = json.dumps(r.json())
                firstLine = firstLine + data
    except:
        firstLine = firstLine + " ERR"


    try:
        secondLine = secondLine + httpsUrl + " -> "
        r = requests.get(httpsUrl, allow_redirects=False)
        secondLine = secondLine + str(r.status_code)
        if (r.status_code == 301):
            r = requests.get(httpsUrl, allow_redirects=True)
            secondLine = secondLine + " = "
            secondLine = secondLine + str(r.content)
        else:
            secondLine = secondLine + " = "
            data = json.dumps(r.json())
            secondLine = secondLine + data
    except:
        secondLine = secondLine + " ERR"

    thirdLine = thirdLine + "Exposed ports: "
    vPassou = False
    results = nmap.nmap_portscan_only(httpDomain)
    for entry in results:
        if (not entry == "stats" and not entry == "runtime"):
            for subEntry in results[entry]['ports']:
                if not(vPassou):
                    thirdLine = thirdLine + subEntry['portid']
                    vPassou = True
                else:
                    thirdLine = thirdLine + ", " + subEntry['portid']
            break    
    outputFile.write(firstLine)
    outputFile.write(secondLine)
    outputFile.write(thirdLine)
    outputFile.write("\r\n")

    outputFile.flush()
inputFile.close()
outputFile.close()

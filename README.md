# find-exposed-applications
Script to find exposed applications to world

You can test inside a VPN and outside that network.


0 - At line 14, you can use a local intranet url to check if the VPN is connected.

1 - Instal nmap: pip3 install python3-nmap

![image](https://user-images.githubusercontent.com/13826728/137327734-d8e586bb-c219-4ca1-a97a-a25e3eb7ec7f.png)

2 - Create a file input.txt with the urls you need test, like:
xptoAAA.com
xptoBBB.com/v1/health
xptoCCC.com.br/v1

3 - python3 main.py

4 = A new file was created, with some like this:
```
 - http://jackpot.xpto.com.br/v1/health -> 403 =  ERR
 - https://jackpot.xpto.com.br/v1/health -> 403 =  ERR
 = Exposed ports: 80, 443, 8008, 8080, 8443

 - http://another-url.com.br/v1/uatu/health/ping -> 301 = {"status": "pong"}
 - https://aanother-url.com.br/v1/uatu/health/ping -> 200 = {"status": "pong"}
 = Exposed ports: 80, 443, 8080, 12265, 15004, 20005, 27352, 28201, 44501, 49152, 49163, 57294, 64680

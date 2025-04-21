@echo off echo Opening ports 31400 - 31409 in Windows Firewall for Pi Network Node...

REM Open TCP ports 31400 - 31409 netsh advfirewall firewall add rule ^ name="Open Ports 31400-31409 (TCP) for Pi Network Node" ^ dir=in action=allow protocol=TCP localport=31400-31409

REM Open UDP ports 31400 - 31409 netsh advfirewall firewall add rule ^ name="Open Ports 31400-31409 (UDP) for Pi Network Node" ^ dir=in action=allow protocol=UDP localport=31400-31409

echo Ports 31400-31409 have been opened on TCP and UDP. echo You can now run the Pi Node in a Docker container with these ports exposed. pause
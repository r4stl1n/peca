import os
import logging
from pyftpdlib.log import logger
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from optparse import OptionParser


class PecaServer:

    def __init__(self, bindaddress, bindport, username, password, datafolder):
        self.bindaddress = bindaddress
        self.bindport = bindport
        self.username = username
        self.password = password
        self.datafolder = datafolder
        self.authorizer = None
        self.handler = None
        self.server = None

    def check_data_folder(self):
        if os.path.isdir(self.datafolder) is False:
            os.makedirs(self.datafolder)

    def config_server(self):
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_user(self.username, self.password, self.datafolder, perm='elradfmwM')
        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer
        self.handler.banner = "PECA Server"
        self.server = FTPServer((self.bindaddress, self.bindport), self.handler)

        # set a limit for connections
        self.server.max_cons = 1000
        self.server.max_cons_per_ip = 1000

    def run(self):
        self.check_data_folder()
        self.config_server()
        self.server.serve_forever()


def print_banner():
    banner = """
          ____  _______________     _____
         / __ \/ ____/ ____/   |   / ___/
        / /_/ / __/ / /   / /| |   \__ \\
       / ____/ /___/ /___/ ___ |_ ___/ /
      /_/   /_____/\____/_/  |_(_)____/
    Post Exploitation Collection Agent Server
    """
    print banner


def main():
    print_banner()

    parser = OptionParser()
    parser.add_option("--ip", dest="bindip", help="Ftp Server BIND Addres [default: %default]", default="")
    parser.add_option("--port", dest="bindport", help="FTP Server BIND Port [default: %default]", default="21")
    parser.add_option("--user", dest="ftpuser", help="FTP Server User [default: %default]", default="pecauser")
    parser.add_option("--password", dest="ftppass", help="FTP Server Password [default: %default]", default="pecapass")
    parser.add_option("--datafolder", dest="datafolder", help="FTP Server datafolder location [default: %default]", default="data")
    (options, args) = parser.parse_args()

    pecaserver = PecaServer(options.bindip, options.bindport, options.ftpuser, options.ftppass, options.datafolder)
    pecaserver.run()

if __name__ == '__main__':
    main()
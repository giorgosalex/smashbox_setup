import sys, os, shutil

def install_and_import(pkg):
    import importlib, site
    
    os.system(sys.executable + " -m easy_install " + pkg)

    reload(site)
    importlib.import_module(pkg)
    globals()[pkg] = importlib.import_module(pkg)



install_and_import('wget')

shutil.rmtree("C:\\smashbox-master")

wget.download("https://github.com/cernbox/smashbox/archive/master.zip")
    
import zipfile
with zipfile.ZipFile("smashbox-master.zip", 'r') as zip_ref:
    zip_ref.extractall("C:\\")

os.remove("smashbox-master.zip")

from sys import platform
import os, ctypes, sys
import wget
import zipfile

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def unzip():
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()

url = "https://chromedriver.storage.googleapis.com/2.31/chromedriver_win32.zip"

if platform == 'linux' or platform == 'linux2':
    print "Linux detected"

elif platform == 'win32':
    print "Windows detected"
    chrome = os.path.isdir("C:\Program Files (x86)\Google\Chrome\Application")
    if chrome == True:
        print "Chrome detected"
        if is_admin():
            output = "C:\Program Files (x86)\Google\Chrome\Application"
            wget.download(url, out=output)
            path_to_zip_file = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver_win32.zip"
            directory_to_extract_to = "C:\Program Files (x86)\Google\Chrome\Application"
            unzip()
        else:
            ctypes.windll.shell32.ShellExecuteW(None, u"runas", u"python", u"install.py", None, 1)
    else:
        print "Chrome not detected"
        
elif platform == 'darwin':
    print 'Mac not supported in this version.'
import subprocess
import os

def is_openSUSE_tumbleweed():
    cmd = "awk -F= '$1==\"ID\" { print $2 ;}' /etc/os-release"

    try:
        os = subprocess.getoutput(cmd).strip('\"').split("-")[1]
    except:
        raise Exception

    return True if os == 'tumbleweed' else False


def get_installed_version():
    cmd = "awk -F= '$1==\"VERSION_ID\" { print $2 ;}' /etc/os-release"
    
    if is_openSUSE_tumbleweed():
        try:
            version = subprocess.getoutput(cmd).strip('\"')
            return version
        except:
            raise Exception
    
    return None
   


def get_latest_released_version(builds):
    builds.sort(key=lambda item:item['Date'], reverse=True)

    for build in builds:
        if build["Published"] == 'Yes':
            return build["Build"][-8:]


def add_installed_flag_on_table(builds_data, version):
    builds = []
    for build in builds_data:
        if build["Build"][-8:] == version:
            build.update({"S": "i"})

        
        builds.append(build)
    
    return builds


def is_upgradable(current,latest):
    if is_openSUSE_tumbleweed():
        return current < latest
    
    return False


def launch_upgrade():
    os.system("sudo zypper dup")
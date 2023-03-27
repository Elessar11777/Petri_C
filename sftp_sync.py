import os
import paramiko
import configparser
import stat

def read_config():
    config = configparser.ConfigParser()
    config.read('./images/configs/config.ini')
    return config

config = read_config()


# Set up your SFTP credentials
host = config.get('SFTP', 'hostname')
username = config.get('SFTP', 'username')
password = config.get('SFTP', 'password')
# load the host keys from the known_hosts file
host_keys = paramiko.hostkeys.HostKeys()
host_keys.load('./known_hosts')



def recursive_check_local(local_dir="./image_test/"):
    local_files = set()
    dir_set = set()
    def recurse(dir):
        file_set = set(os.listdir(dir))
        for set_element in file_set:
            element_path = os.path.join(dir, set_element).replace("\\", "/")
            if os.path.isdir(element_path):
                dir_set.add(element_path)
                recurse(element_path)
            else:
                local_files.add(element_path)

    recurse(local_dir)

    return local_files, dir_set

def recursive_check_remote(sftp, remote_dir="/srv/filehosting/image_test/"):
    remote_files = set()
    dir_set = set()

    def recurse(dir):
        file_set = set(sftp.listdir(dir))
        for set_element in file_set:
            element_path = os.path.join(dir, set_element).replace("\\", "/")
            fileattr = sftp.lstat(element_path)
            if stat.S_ISDIR(fileattr.st_mode):
                dir_set.add(element_path)
                recurse(element_path)
            else:
                remote_files.add(element_path)

    recurse(remote_dir)
    return remote_files, dir_set


def find_missings(sftp):
    loc, loc_dir = recursive_check_local()
    rem, rem_dir = recursive_check_remote(sftp)
    new_rem = {x.replace("/srv/filehosting", ".") for x in rem}
    new_rem_dir = {x.replace("/srv/filehosting", ".") for x in rem_dir}
    mis_files = loc - new_rem
    mis_dirs = loc_dir - new_rem_dir

    abs_rem_files = {os.path.join("/srv/filehosting/", x[2:]) for x in mis_files}
    abs_rem_dir = {os.path.join("/srv/filehosting/", x[2:]) for x in mis_dirs}
    abs_rem_dir = sorted(abs_rem_dir, key=len)
    print(f"Files in remote to sync {abs_rem_files}")
    print(f"Dirs in remote to sync {abs_rem_dir}")
    return abs_rem_dir, abs_rem_files

def sync_files(sftp, index):
    dirs, files = index
    for dir in dirs:
        print(f"Creating folder {dir}")
        sftp.mkdir(dir)
    for file in files:
        print(f"Creating file {file}")
        # print(file.replace("/srv/filehosting", "."))
        sftp.put(file.replace("/srv/filehosting", "."), file)
if __name__ == "__main__":
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    sftp = ssh.open_sftp()


    index = find_missings(sftp)
    sync_files(sftp, index)

    sftp.close()
    ssh.close()
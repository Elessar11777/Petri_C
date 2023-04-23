import pysftp
import subprocess


HOSTNAME = "194.186.150.222"
USERNAME = "user"
PASSWORD = "1qaz!QAZ"
cnopts = pysftp.CnOpts(knownhosts='known_hosts')
SERVER_DIRECTORY = "/srv/filehosting/"


def file_sending():
    with pysftp.Connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts) as sftp:
        #sftp.execute("sudo su")
        #sftp.execute("1qaz!QAZ")
        sftp.put(localpath=f"./images/configs/settings.json", remotepath=f"/srv/filehosting/images_new")
        return

file_sending()



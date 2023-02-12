import pysftp
import subprocess


def sftp_connection():
    HOSTNAME = "194.186.150.221"
    USERNAME = "user"
    PASSWORD = "1qaz!QAZ"
    cnopts = pysftp.CnOpts(knownhosts='known_hosts')
    SERVER_DIRECTORY = "/srv/filehosting/"


def file_sending(local_path, remote_path):
    with pysftp.Connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts) as sftp:
        #sftp.execute("sudo su")
        #sftp.execute("1qaz!QAZ")
        sftp.put(localpath=f"{local_path}", remotepath=f"/srv/filehosting/images_new/{remote_path}")
        return





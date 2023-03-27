# import pysftp
# import subprocess
#
# HOSTNAME = "194.186.150.221"
# USERNAME = "user"
# PASSWORD = "1qaz!QAZ"
# cnopts = pysftp.CnOpts(knownhosts='known_hosts')
# SERVER_DIRECTORY = "/srv/filehosting/images/gracia-test"
# SEARCH_TERM = "Pr"

if __name__ == '__main__':
    with pysftp.Connection(HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts) as sftp:
        sftp.cwd(SERVER_DIRECTORY)
        file_list = sftp.listdir()
        counter = 0
        for i in file_list:
            sftp.cwd(SERVER_DIRECTORY + "/" + i)
            cur_dir = sftp.listdir()
            for a in cur_dir:
                if "EC" in a or "ec" in a or "Ec" in a:
                    print(a)
                    counter += 1
        print(int(counter/2))
        #search_format = 'grep -rl "{}" {}/*'.format(SEARCH_TERM, SERVER_DIRECTORY)
        #print(search_format)
        #output = sftp.execute(search_format)
        # num_files = len(output)
        # print(output)
        # print("Number of files containing at least one string from the list: ", num_files)
import os
import shutil
import time
from distutils.dir_util import copy_tree
import datetime
import csv

def write_file(file,action,source,replica):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    filenames = [[date,action,file,source,replica]]
    if os.path.exists('Sync data.csv'):
        with open('Sync data.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(filenames)
    else:
        print('The "Sync data.csv" file was created')
        with open('Sync data.csv', 'w', newline='') as f:
            columns = ['date','Action', 'file / dir','Source','Replica']
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(filenames)


# sync file from source folder to replica folder. Time_loop = minute interval to sync
def sync_file(source,replica,time_loop):
    while True:
        files_surces = os.listdir(source)
        for i in files_surces:
            full_files=os.path.join(source,i)
            if os.path.isfile(full_files):
                shutil.copyfile(full_files,replica+i)
                print('file "'+i+ '" sync in replica folder')
                write_file(i,'copy','from '+source,'to '+replica)
            try:
                if os.path.isdir(full_files):
                    shutil.copytree(source+i,replica+i)
                    print('dir "'+i+ '" sync in replica folder')
                    write_file(i,'copy','from '+source,'to '+replica)
            except:
                copy_tree(source+i,replica+i)
                print('file "'+i+ '" sync in replica folder')
                write_file(i,'copy','from '+source,'to '+replica)

        # remove file from dir replica if are not in source
        files_replica = os.listdir(replica)
        files_surces = os.listdir(source)
        for i in files_replica:
            full_filesR = os.path.join(replica, i)
            try:
                if i not in files_surces:
                    os.remove(replica + i)
                    write_file(i,action='detete',source='',replica='from '+replica)
                    print('file "' + i + '" deleted from replica folder')
            except:
                pass
            if os.path.isdir(full_filesR):
                if i not in files_surces:
                    os.rename(replica + i, replica + i + '1')
                    shutil.rmtree(replica + i + '1')
                    write_file(i,action='detete',source='',replica='from '+replica)
                    print('dir "' + i + '" deleted from replica folder')
        time.sleep(time_loop*60)


sync_file('C:\\Users\\Users\\Desktop\\source\\','C:\\Users\\Users\\Desktop\\replica\\',2)







import paramiko

def mv(ssh):
    
    try:
        res=[]
        nas = 'ssh -o PreferredAuthentications=publickey -o PubkeyAuthentication=yes -o passwordAuthentication=no -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa isd@isp.s0'+host+'.wal-mart.com'
        mv='ls -ltr /u/is/data/mv/MV00* |tail -5;pwd;date'
        ls='ls -ltr /u/is/data/mv/linksave/ |tail -5;pwd;'
        arch='ls -ltr /u/is/data/mv/archive/MV00* |tail -3;pwd;date'
        rej='ls -ltr /u/is/data/mv/smv0032_reject/ |tail -3;pwd;'
        ts='ls -ltr /u/is/tlog/TS00* |tail -3;pwd;'
        mb='tail -2 /u/is/tlog/tmp/mbEditor.log'
        stdin, stdout, stderr = ssh.exec_command(nas+';'+mv+';'+ls+';'+arch+';'+rej+';'+ts+';'+mb)
        res.append(stdout.read().decode('utf-8'))

        txt = host+'_isp.txt'
            
        with open(txt, 'w', newline='') as f:
            f.writelines("%s\n" % i for i in res)
            print ("Filecreated")
        
        # return output

        log(ssh)

    except Exception as e:
        print('Error: '+ stderr.read().decode('utf-8'))
        print(e)

def log(ssh):
    
    try:
        res=[]
        nas = 'ssh -o PreferredAuthentications=publickey -o PubkeyAuthentication=yes -o passwordAuthentication=no -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa isd@isp.s0'+host+'.wal-mart.com'
        runcm=nas+'  \'. /u/data/environment; sco_fixfs.pl | grep y | grep \'\'`date +%Y-%m-%d`\'\'|cut -c6-15;\''

        stdin,stdout,stderr=ssh.exec_command(runcm)
        res.append(stdout.read().decode('utf-8'))

        runcm=nas+'  \'. /u/data/environment; dfx_xferpos -l /tmp/POSRESET.LOG -r adxlxacn::d:/log/POSRESET.LOG -m PULL -o| grep -v \'Failed to open\';\''
        stdin,stdout,stderr=ssh.exec_command(runcm)
        res.append(stdout.read().decode('utf-8'))

        runcm=nas+'  \'. /u/data/environment; tail -5 /tmp/POSRESET.LOG | grep 0063 | tail -1 | cut -c1-6;\''
        stdin,stdout,stderr=ssh.exec_command(runcm)
        res.append(stdout.read().decode('utf-8'))

        txt = host+'_log.txt'
            
        with open(txt, 'w', newline='') as f:
            f.writelines("%s\n" % i for i in res)
            print ("Filecreated")
        
        # return output


    except Exception as e:
        print('Error: '+ stderr.read().decode('utf-8'))
        print(e)

def ssh_connect(host):
    try:
        ssh = paramiko.SSHClient()
        uid='vn50to7'
        pw='asdf@2121'
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # ssh.connect(hostname='.wal-mart.com', username=uid, password=pw)
        # ssh.connect(hostname=host,username='',password='')
        ssh.connect(hostname='isp.s0'+host+'.wal-mart.com', username='', password='')
        print(host+' Connection Established')

        mv(ssh)

    except Exception as e:
        print('Host Connection Failed')
        print(e)

if __name__=='__main__':
    host = input("Store: Example: 1000.US:")
    # host = '00000.US'
    ssh_connect(host)
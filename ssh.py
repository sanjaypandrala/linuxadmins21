#!/usr/bin/env python

'''
ssh-keygen  will create generate
~/.ssh/id-rsa is a private key
~/.ssh/id-rsa.pub is public key

ssh-copy-id will add ~/.ssh/id-rsa.pub to ~/.ssh/authorized_keys on the server
set up passphrase to add more security
'''

'''
configure ssh authentication
server1$ ssh-keygen -t dsa
enter passphrase

$ ssh-copy-id server2
enter passphrase

then we will in the
server2$ cat authorized_keys

to avoid entering passphrase all the time we the following on server1

server1$ ssh-agent /bin/bash

server1$ ssh-add
enter passphrase only once

server1$ ssh server2
we need not enter passphrase

Naturally, the "ls -l; echo 'Hello World'" part could be replaced with a bash script stored in a file on the local machine.

echo "ls -l; echo 'Hello World'" | ssh me@myserver /bin/bash

'''
'''
/etc/ssh/sshd_config

default port from 22 2022
ListenAddress may be to specific address
SyslogFacility
PermitRootLogin yes => no
AllowUsers like sanjpa
MaxSessions
PasswordAuthentication to no
GSSAPICleanupCredentials to yes
TCPKeepAlive to yes
ClientAliveInterval to yes
after doing the modification
systemctl restart sshd
systemctl start sshd
if it doesnot work
setenforce 0 # to check if it is selinux issue
systemctl restart sshd
systemctl start sshd

grep AVC /var/log/audit/audit.log # will details
semanage port l | grep 22 # to find the correct context
semanage port -a -t ssh_port_t -p tcp 8991
semanage port l | grep 22 # now will show the new port 8991
systemctl restart sshd # will bring up the new port 8991

'''
'''
tuning ssh clients is by editing
/etc/ssh/sshd_config

'''
'''
ssh tunnels

AMS     AMD     AMS
4444--->SSHD---->110

'''
'''
creating ssh tunnels and this is local port forwarding
ssh -fNL 4444:server.redhatcertification.com:80 root@server2.example.com
elinks https:localhost:4444 # will the server.redhatcertification.com:80 on server2

ssh -fNL 5555:localhost:80 root@server2.example.com
elinks https://localhost:5555  # this will open the page provided by server2

remote port forwarding not common
ssh -R 80:localhost:8080 sander@lab.sandervanvugt.nl

lsof -i -n | grep ssh # to monitor the tunnels currently existing
netstat -tulpen | grep 22 # will show all the ssh tunnels or active sessions

'''
'''

exercise ssh
on server1 set up SSH to forward all traffic on port 2020 to port 80 on www.sandervanvugt.nl
use server2 as an intermediate server and make sure the session runs in background and does not open a console
session to server2
set up SSH key based authentication. make sure to protect the private key with a passphrase
take the appropriate measures to cache the key (so that you'll have to enter it once only)

exp exer ssh
ssh -l 2022:www.sandervanvugt.nl:80 root@server2.example.com
ssh-keygen -t -dsa
ssh-agent /bin/bash
ssh-add

'''
'''
Copy the file "foobar.txt" from a remote host to the local host

$ scp your_username@remotehost.edu:foobar.txt /some/local/directory
Copy the file "foobar.txt" from the local host to a remote host

$ scp foobar.txt your_username@remotehost.edu:/some/remote/directory
Copy the directory "foo" from the local host to a remote host's directory "bar"

$ scp -r foo your_username@remotehost.edu:/some/remote/directory/bar
Copy the file "foobar.txt" from remote host "rh1.edu" to remote host "rh2.edu"

$ scp your_username@rh1.edu:/some/remote/directory/foobar.txt \
your_username@rh2.edu:/some/remote/directory/
Copying the files "foo.txt" and "bar.txt" from the local host to your home directory on the remote host

$ scp foo.txt bar.txt your_username@remotehost.edu:~
Copy the file "foobar.txt" from the local host to a remote host using port 2264

$ scp -P 2264 foobar.txt your_username@remotehost.edu:/some/remote/directory
Copy multiple files from the remote host to your current directory on the local host

$ scp your_username@remotehost.edu:/some/remote/directory/\{a,b,c\} .
$ scp your_username@remotehost.edu:~/\{foo.txt,bar.txt\} .

'''

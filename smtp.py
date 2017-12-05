'''
SMTP outgoing email transmission
POP IMAP receiving mail
mutt/outlook/evolution are mail clients
'''
'''
requirements for email transmission

relaying : mail is sent to an outgoing mail
DNS MX records are used to look up the mail server for the recipient
'''
'''
configuring postfix for mail reception are in the
cd /etc/postfix

ls
# on server201
vim main.cf
inet_interface = all
myorigin = $mydomain  # like user@
relayhost =  192.x.x.x.x # host msg forward to
mydestination =    #which domain it should take care for receiving msgs like redhatcertification.com, sandervanvugt.nl
local_transport = # forward msg to someother
mynetworks =   #
then
systemctl restart postfix
ssh servrer202

on servrer202
postconf -e "relayhost[server201.example.com]"
postconf -e "inet_interface = loopback-only"
postconf -e "mynetworks=127.0.0.0/8" # this is to accept loopback-only
postconf -e "mydestination="
mail -s mailtolisa lisa@server201.example.com < .
exit
server201$ su - lisa
server201$ mail  # there is no mail so troubleshooting

on servrer202
postqueue -p
ping server201.example.com # ping works
vim /etc/postfix/main.cf
inet_protocol = all to ipv4
systemctl restart postfix # on both servers

on server201
grep mydestination /etc/postfix/main.cf
systemctl restart postfix
su - lisa
mail
#################################
Exercise 38.1 Changing Postfix Parameters with postconf
1. On server1, open a root shell and type postconf. You’ll see a long list of all current Postfix settings.
2. Type postconf myorigin. This shows the current value of the myorigin setting.
3. Type postconf mydomain to verify the current value of the mydomain parameter.
4. Enter postconf -e 'myorigin = $mydomain' to change the value of the myorigin parameter.
5. Repeat the command postconf myorigin. Notice that nothing has changed so far.
6. Type postfix check. This checks the contents of the /etc/postfix/main.cf file and alerts if anything is wrong with it (always a good choice before starting to use new configuration).
7. Reload Postfix, using systemctl reload postfix, and repeat step 5. You’ll see that the setting has now been changed.
8. Type postconf -n. This shows all parameters with a parameter that is different from the default.
Exercise 38.2 Configuring a Postfix Null Client Setup
Notice that in this exercise you configure two servers. The tasks that you perform on server1 show how to set up a null client. On server2, you configure a mail server that does accept incoming messages. This goes beyond the RHCE objective, but it is useful to know how to do it so that you can set up a working email configuration. To perform this exercise, you need to use DNS services. You can use the IPA server virtual machine (VM) that is provided at http://www.rhatcert.com for this purpose, or you can build your own IPA server according to the instructions in Appendix D, “Setting Up Identity Management.”
1. Open a root shell on server1.
2. Verify that you can resolve server2 using host server2. The host command should get back with the IP address that server2 is currently using.
3. Type postconf -e 'relayhost=[server2.example.com]' to relay messages to server2.
4. Make sure your server can only relay messages that are sent from this server using postconf -e 'inet_interfaces=loopback-only'.
5. Type postconf mynetworks to verify that only messages originating from the loopback IP address will be accepted.
6. Type postconf -e 'mydestination='. This ensures that Postfix on server1 has no destinations.
7. Disable IPv6, using postconf -e 'inet_protocols = ipv4'.
8. Type postconf -e 'mydomain=example.com' to change the origin of each message that is sent.
9. Type systemctl reload postfix to restart the Postfix server on server1.
10. On server2, use the following commands to enable the server to receive messages that are relayed by server1:
Click here to view code image
postconf -e 'inet_interfaces=all'
postconf -e 'mydestination = example.com,server2.example.com'
postconf -e 'inet_protocols = ipv4'

11. On server2, type firewall-cmd --add-service smtp --permanent followed by firewall-cmd --reload to add the SMTP service to the firewall.
12. On server2, typen systemctl restart postfix to restart the postfix service.
13. On server1, type mail -s test1 root@server2.example.com <. (note that the command ends with a dot)
14. On server2, as root, type mail. You should see the test message that has just been received from the other server.
#####################################
exercise
create an email configuration where server1 is configured as a
relay serer and server2 is configured as  a null client
test its working by creating a user lisa on server1
as any user on server2, send a message to lisa on server1
use mutt to verify it is working correctly

explation to exercise
on server1
    inet_interface = all
    myorigin = example.com
    mydestination= # empty or example.com
    inet_protocols = ipv4
on server2
    postconf -e "relayhost[server1.example.com]"
    postqueue -e "inet_interface=loopback-only"
    postconf -e "mynetworks=127.0.0.0/8[::1]/128"
    postconf -e "mydestination="
    inet_protocols=ipv4
'''
demonstrate it is working by sending mail from server2 to a user on server1
as user on server1, use mutt to see the message coming in
tail -f /var/log/messages
postqueue -p
postqueue -f
'''
'''
command to use are
postconf
postconf inet_interface # will show value for specific paramenters
postconf -e 'myorigin = example.com' # this to edit the value for the paramenters
man 5 postconf
postqueue -p
postqueue -f # will flush the queue
tail -f /var/log/maillog

'''

import Tkinter
import ttk
from PIL import Image, ImageTk
import paramiko,os,time,select
import time, os
#from PIL import Image, ImageTk

print 'Welcome to OVP control panel!'

# create logs & downloads directories in the path of the executable; if it exists, it will delete the content.
root_dir = os.getcwd()
outputs_dir = root_dir + '\outputs'
downloads_dir = root_dir + '\downloads'
if os.path.isdir(outputs_dir) == True:
    contents = [os.path.join(outputs_dir, i) for i in os.listdir(outputs_dir)]
    for i in contents:
        if os.path.isfile(i):
            os.remove(i)
else:
    os.mkdir("outputs")

if os.path.isdir(downloads_dir) == True:
    contents = [os.path.join(downloads_dir, i) for i in os.listdir(downloads_dir)]
    for i in contents:
        if os.path.isfile(i):
            os.remove(i)
else:
    os.mkdir("downloads")

# variables
selenium_host = '10.236.56.131'
private_key=paramiko.RSAKey.from_private_key_file("resources\\selenium_rsakey")
session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

root = Tkinter.Tk()
root.title('OVP* control panel')
image = ImageTk.PhotoImage(file="resources\\background_image.jpg")
root.geometry("%dx%d+%d+%d" % (image.width(), image.height(), 200, 50))
root.resizable(True, True)

ansible_user = "ansible"
ansible_password = "GgansibleX"


# Functions
#validated
def OVC_Portal():
    os.chdir(root_dir)
    try:
        session.connect(selenium_host, port=22, username='centos', pkey=private_key)
        print '\nconnected to the Selenium server.\n Please wait for the test result. This should take up to 10 seconds ... \n'
        ssh_stdin, ssh_stdout, ssh_stderr = session.exec_command('sudo /usr/bin/python /usr/local/nagios/libexec/OVC_Portal_test.py')
        output = ssh_stdout.readlines()
        output = "".join(output)
        while not ssh_stdout.channel.exit_status_ready():
            if ssh_stdout.channel.recv_ready():
                rl, wl, xl = select.select([ssh_stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    #print rl
                    print ssh_stdout.channel.recv(1024)
        out=ssh_stdout.read()

        if txt_OVC_Portal.get() == True:
            os.chdir(outputs_dir)
            f = open('OVC_Portal_output.txt', 'w')
            print >> f, output
            f.close()
            os.system('start notepad.exe ' + 'OVC_Portal_output.txt')
            print "you can find the output into the file " + outputs_dir + '\OVC_Portal_output.txt'
        else:
            print output
    except:
        print '\nCould not connect to the server. Please stop the Cactus connection and try again.'
    else:
        print 'Successfully finished!'
    session.close()
def OVP_Core():
    os.chdir(root_dir)
    try:
        session.connect(selenium_host, port=22, username='centos', pkey=private_key)
        print '\nconnected to the Selenium server.\n Please wait for the test result. This should take up to 10 seconds ... \n'
        ssh_stdin, ssh_stdout, ssh_stderr = session.exec_command(
            'sudo /usr/bin/python /usr/local/nagios/libexec/OVP_test.py')
        output = ssh_stdout.readlines()
        output = "".join(output)
        while not ssh_stdout.channel.exit_status_ready():
            if ssh_stdout.channel.recv_ready():
                rl, wl, xl = select.select([ssh_stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    # print rl
                    print ssh_stdout.channel.recv(1024)
        out = ssh_stdout.read()

        if txt_OVP_Core.get() == True:
            os.chdir(outputs_dir)
            f = open('OVP_Core_output.txt', 'w')
            print >> f, output
            print "you can find the output into the file " + outputs_dir + '\OVP_Core_output.txt'
            f.close()
            os.system('start notepad.exe ' + 'OVP_Core_output.txt')
        else:
            print output
    except:
        print '\nCould not connect to the server. Please stop the Cactus connection and try again.'
    else:
        print 'Successfully finished!'
    session.close()
def OVPA_Portal():
    os.chdir(root_dir)
    try:
        session.connect(selenium_host, port=22, username='centos', pkey=private_key)
        print '\nconnected to the Selenium server.\n Please wait for the test result. This should take up to 3 minutes ... \n'
        ssh_stdin, ssh_stdout, ssh_stderr = session.exec_command('sudo /usr/bin/python /usr/local/nagios/libexec/OVPA_Portal_test.py')
        output = ssh_stdout.readlines()
        output = "".join(output)
        while not ssh_stdout.channel.exit_status_ready():
            if ssh_stdout.channel.recv_ready():
                rl, wl, xl = select.select([ssh_stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print ssh_stdout.channel.recv(1024)
        out=ssh_stdout.read()

        if txt_OVPA_Portal.get() == True:
            os.chdir(outputs_dir)
            f = open('OVPA_Portal.txt', 'w')
            print >> f, output
            print "you can find the output into the file " + outputs_dir + '\OVPA_Portal.txt'
            f.close()
            os.system('start notepad.exe ' + 'OVPA_Portal.txt')
        else:
            print output
    except:
        print '\nCould not connect to the server. Please stop the Cactus connection and try again.'
    else:
        print 'Successfully finished!'
    session.close()
def ssh_command(server, command=''):
    username = ansible_user
    password = ansible_password
    #command = "ls"
    # prerequisites
    #os.chdir(root_dir)

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, username = username, password = password)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.readlines()
        output = "".join(output)
    except:
        print "\nssh KO! Please asure that your Cactus session is active."
    else:
        #print output
        ssh.close()
        return output
def sftp_transfer(server, source_dir, source_file, dest_dir, dest_file):
    username = ansible_user
    password = ansible_password

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=username, password=password)
    ftp_client = ssh.open_sftp()
    ftp_client.get( source_dir + source_file , dest_dir + dest_file )
    ftp_client.close()
def update_dict():
    ovp_hostname_dict_updated = {}
    for elem in ovp_hostname_dict:
        ovp_hostname_dict_updated[elem] = [ovp_hostname_dict[elem][0].get() , ovp_hostname_dict[elem][1]]
    return ovp_hostname_dict_updated

def execute_ovp_command():
    update_dict()
    for elem in update_dict():
        if update_dict()[elem][0] == True:
            print "Start the download from " + elem
            try:
                for file in ssh_command(update_dict()[elem][1], command='ls /data/tracability/logs | grep ' + elem + ' | grep log | grep -v elastic' ).split():
                    print "   downloading " + file.split("/")[-1] + " ..."
                    sftp_transfer(update_dict()[elem][1] , "/data/tracability/logs/", file.split("/")[-1], "downloads/", file.split("/")[-1])
            except:
                print "Could not download from " + elem
                pass
            else:
                print "Finished download from " + elem + "\n"
    print "You can find all the downloaded files in: " + downloads_dir

# not validated
def help():
    print "help section - this is under construction ..."
def clock():
    print "Local time: " + time.ctime()
def print_var_value():
    print var.get()
def popup_showinfo():
    showinfo("Window", "Hello World!")

rows = 0
while rows < 50:
    root.rowconfigure(rows, weight = 1)
    root.columnconfigure(rows, weight=1)
    rows += 1

nb = ttk.Notebook(root)
nb.grid(row = 1, column = 0, columnspan = 48, rowspan = 45, sticky = 'NESW', )

tab_e2e = ttk.Frame(root)
nb.add(tab_e2e,text = "OVP e2e tests")

tab_ovpTools = ttk.Frame(root)
nb.add(tab_ovpTools,text = "OVP* tools")

tab_help = ttk.Frame(root)
nb.add(tab_help,text = " Help ")

# populate OVP e2e tests (tab_e2e)
labelFrame = ttk.LabelFrame(tab_e2e, text = "    OVC portal e-2-e test", width=25)
labelFrame.grid(column = 1, row = 1, padx = 300, pady= 50)
button_OVC_e2e = Tkinter.Button(labelFrame, text=' Submit test ', command = OVC_Portal, width=25, fg="orange")
button_OVC_e2e.grid(column = 0, row = 0, padx = 8, pady= 10)
txt_OVC_Portal = Tkinter.BooleanVar()
checkButton = Tkinter.Checkbutton(labelFrame,text="export to txt", variable=txt_OVC_Portal,)
checkButton.grid(column = 1, row = 0, padx = 8, pady= 10)
txt_OVC_Portal.set(False)

labelFrame = ttk.LabelFrame(tab_e2e, text = "    OVP and OVC e-2-e test", width=25)
labelFrame.grid(column = 1, row = 2, padx = 8, pady= 50)
button_OVC_e2e = Tkinter.Button(labelFrame, text=' Submit test ', command = OVP_Core, width=25, fg="orange")
button_OVC_e2e.grid(column = 0, row = 0, padx = 8, pady= 10)
txt_OVP_Core = Tkinter.BooleanVar()
checkButton = Tkinter.Checkbutton(labelFrame,text="export to txt", variable=txt_OVP_Core,)
checkButton.grid(column = 1, row = 0, padx = 8, pady= 10)
txt_OVP_Core.set(False)

labelFrame = ttk.LabelFrame(tab_e2e, text = "    OVPA portal e-2-e test", width=25, )
labelFrame.grid(column = 1, row = 3, padx = 2, pady= 50)
button_OVC_e2e = Tkinter.Button(labelFrame, text=' Submit test ', command = OVPA_Portal, width=25, fg="orange")
button_OVC_e2e.grid(column = 0, row = 0, padx = 8, pady= 10)
txt_OVPA_Portal = Tkinter.BooleanVar()
checkButton = Tkinter.Checkbutton(labelFrame,text="export to txt", variable=txt_OVPA_Portal,)
checkButton.grid(column = 1, row = 0, padx = 8, pady= 10)
txt_OVPA_Portal.set(False)

# populate OVP* tools (tab_ovpTools)
labelFrame = ttk.LabelFrame(tab_ovpTools, text = "    OVP* logs download", width=25, )
labelFrame.grid(column = 0, row = 1, padx = 10, pady= 0)

check_opopvas11 = Tkinter.BooleanVar()
check_opopvas12 = Tkinter.BooleanVar()
check_opopvas13 = Tkinter.BooleanVar()
check_opopvas14 = Tkinter.BooleanVar()
check_opopvas15 = Tkinter.BooleanVar()
check_opopvas16 = Tkinter.BooleanVar()
check_opopvdc11 = Tkinter.BooleanVar()
check_opopvdnc01 = Tkinter.BooleanVar()
check_opopvdnc02 = Tkinter.BooleanVar()

ovp_hostname_dict = {"opopvas11": [check_opopvas11, "10.108.160.43", 0],
                     "opopvas12": [check_opopvas12, "10.108.160.44", 1],
                     "opopvas13": [check_opopvas13, "10.108.160.45", 2],
                     "opopvas14": [check_opopvas14, "10.108.160.46", 3],
                     "opopvas15": [check_opopvas15, "10.108.160.47", 4],
                     "opopvas16": [check_opopvas16, "10.108.160.48", 5],
                     "opopvdc11": [check_opopvdc11, "10.108.160.49", 6],
                     "opopvdnc01": [check_opopvdnc01, "10.97.167.65", 7],
                     "opopvdnc02": [check_opopvdnc02, "10.97.167.66", 8],
                }

def check_butons_ovpTools():
    row_count = 0
    for elem_number in range(len(ovp_hostname_dict)):
        for elem in ovp_hostname_dict:
            if ovp_hostname_dict[elem][2] == elem_number:
                elem_found = elem
                print elem_found
                checkButton = Tkinter.Checkbutton(labelFrame, text=elem_found, variable=ovp_hostname_dict[elem_found][0])
                checkButton.grid(column=0, row=row_count, padx=6, pady=0)
                row_count += 1
            else:
                pass


button_start_download = Tkinter.Button(labelFrame, text='Start download', command = execute_ovp_command, width=40, fg="orange")
button_start_download.grid(column = 1, row = 0, padx = 8, pady= 0)

#checkButton - just test
var = Tkinter.BooleanVar()
checkButton = Tkinter.Checkbutton(tab_help,text="fac ce text vrea muschii mei", variable=var,)
checkButton.grid(column = 0, row = 0, padx = 8, pady= 10)
var.set(False)

# button - just test
button_confInfo = Tkinter.Button(tab_help, text=' confInfo ', fg="blue", command = print_var_value)
button_confInfo.grid(column = 1, row = 0, padx = 8, pady= 10)

'''
def changeLabel(output):
    theLabel_text.set(output)
    return
'''

# execution
check_butons_ovpTools()
root.mainloop()
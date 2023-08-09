import wmi, subprocess, os, time, re

special_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

version = "0.10"

os.system("cls")

c = wmi.WMI()    
systeminfo = c.Win32_ComputerSystem()[0]
mdl = systeminfo.Model
o_serial = c.Win32_Bios()[0].SerialNumber

def get_model():
    if mdl.find("7440") != -1:
        return "7440"
    elif mdl.find("7450") != -1:
        return "7450"
    elif mdl.find("9030") != -1:
        return "9030"
    elif mdl.find("Unidentified System") != -1:
        return "7450UNK"

mdl = get_model()

if not mdl:
    exit()

if mdl == "7450UNK":
    print("WARNING!!!!! THIS SYSTEM IS PRESUMED TO BE A 7450 IF YOU RUN ANY OF THE FOLLOWING FUNCTIONS AND THIS UNIT ISN'T A 7450 YOU COULD BRICK THE SYSTEM.")
    mdl = "7450"
    
print("AIO Programming Tool {0}".format(version))    
print("Current System Serial: {0}".format(o_serial))
print("Functions available (Ensure Jumper Is Set Before Running Any Functions Below):")
print("1. Serial Reset")
print("2. Longboot (Unit Will Restart)")
print("3. Longboot & Serial Reset (Recommended For Mobo Swaps, Unit Will Restart)")

def get_serial_offset():
    if mdl == "7440":
        return 0x81412
    elif mdl == "9030":
        return 0x4814F
    elif mdl == "7450":
        return 0x899C2

def create_bios(s):
    with open('C:\\TOOLS\\{0}_RES\\BIOS.bin'.format(mdl), 'rb+') as f:
        f.seek(get_serial_offset())
        f.write(s.encode())
        f.close()

def reset_bios():
    with open('C:\\TOOLS\\{0}_RES\\BIOS.bin'.format(mdl), 'rb+') as f:
        f.seek(get_serial_offset())
        f.write(b'\x00\x00\x00\x00\x00\x00\x00')
        f.close()

def get_entered_serial():
    while True:
            serial = input("Please Enter The New Serial: ")
            if serial == o_serial:
                print("Serial Already Set To Specified Serial, Press Any Key To Exit!")
                os.system("pause")
                exit(0)
            if len(serial) <= 7 and serial and serial.find(' ') == -1 and special_regex.search(serial) == None:
                break
            print("Serial Must Be Not Empty, 7 Characters, Have No Special Characters, And Must Have No Spaces. Try Again.")
    return serial

def do_reset(s):
    create_bios(s)
    time.sleep(1.5)

    if mdl == "7440" or mdl == "7450":
        proc = subprocess.run("C:\\FPT\\40\\FPT.exe -BIOS -F C:\\TOOLS\\{0}_RES\\BIOS.bin -P C:\\FPT\\40\\fparts.txt".format(mdl))
    elif mdl == "9030":
        proc = subprocess.run("C:\\FPT\\30\\FPT.exe -BIOS -F C:\\TOOLS\\9030_RES\\BIOS.bin -P C:\\FPT\\30\\fparts.txt")
    
    while proc.returncode != 0:
        print("Process Failed Retrying..")
        time.sleep(1)
        proc = subprocess.run(proc.args)
    
    reset_bios()
        
def serial_reset():
    print('Running Serial Reset For {0} AIO.'.format(mdl))
    serial = get_entered_serial()
    do_reset(serial)

def do_long_boot():
    if mdl == "7440" or mdl == "7450":
        proc = subprocess.run("C:\\FPT\\40\\FPT.exe -ME -F C:\\TOOLS\\{0}_LB\\ME.bin -P C:\\FPT\\40\\fparts.txt".format(mdl))
    elif mdl == "9030":
        proc = subprocess.run("C:\\FPT\\30\\FPT.exe -ME -F C:\\TOOLS\\9030_LB\\ME.bin -P C:\\FPT\\30\\fparts.txt")
        
    while proc.returncode != 0:
        print("Process Failed Retrying..")
        time.sleep(1)
        proc = subprocess.run(proc.args)

    if mdl == "9030":
        proc = subprocess.run("C:\\FPT\\30\\FPT.exe -DESC -F C:\\TOOLS\\9030_LB\\DESC.bin -P C:\\FPT\\30\\fparts.txt")
        while proc.returncode != 0:
            print("Process Failed Retrying..")
            time.sleep(1)
            proc = subprocess.run(proc.args)

    if mdl == "7440" or mdl == "7450":
        subprocess.run("C:\\FPT\\40\\FPT.exe -greset -P C:\\FPT\\40\\fparts.txt")
    elif mdl == "9030":
        subprocess.run("C:\\FPT\\30\\FPT.exe -greset -P C:\\FPT\\30\\fparts.txt")
        

def long_boot():
    print('Running Longboot For {0} AIO.'.format(mdl))
    do_long_boot()
         

selection = "0"

while True:
    selection = input("Enter An Action To Perform (1-3): ")
    if selection == "1" or selection == "2" or selection == "3":
        break
    print("Invalid input! Try again.")

os.system("cls")

if selection == "1":
    serial_reset()
elif selection == "2":
    long_boot()
elif selection == "3":
    serial_reset()
    long_boot()

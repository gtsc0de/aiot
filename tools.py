import wmi, subprocess, os, time

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

print("AIO Programming Tool {0}".format(version))    
print("Current System Serial: {0}".format(o_serial))
print("Functions available (Ensure Jumper Is Set Before Running Any Functions Below):")
print("1. Serial Reset")
print("2. Longboot (Unit Will Restart)")
print("3. Longboot & Serial Reset (Recommended For Mobo Swaps, Unit Will Restart)")

def create_40_bios(s):
    with open('C:\\TOOLS\\7440_RES\\BIOS.bin', 'rb+') as f:
        f.seek(0x81412)
        f.write(s.encode())
        f.close()

def reset_40_bios():
    with open('C:\\TOOLS\\7440_RES\\BIOS.bin', 'rb+') as f:
        f.seek(0x81412)
        f.write(b'\x00\x00\x00\x00\x00\x00\x00')
        f.close()

def create_50_bios(s):
    with open('C:\\TOOLS\\7450_RES\\BIOS.bin', 'rb+') as f:
        f.seek(0x899C2)
        f.write(s.encode())
        f.close()

def reset_50_bios():
    with open('C:\\TOOLS\\7450_RES\\BIOS.bin', 'rb+') as f:
        f.seek(0x899C2)
        f.write(b'\x00\x00\x00\x00\x00\x00\x00')
        f.close()

def create_30_bios(s):
    with open('C:\\TOOLS\\9030_RES\\BIOS.bin', 'rb+') as f:
        f.seek(0x4814F)
        f.write(s.encode())
        f.close()

def reset_30_bios():
    with open('C:\\TOOLS\\9030_RES\\BIOS.bin', 'rb+') as f:
        f.seek(0x4814F)
        f.write(b'\x00\x00\x00\x00\x00\x00\x00')
        f.close()

def serial_reset():
    if mdl == "7450UNK":
        print("This unit was unknown and presumed as being a 7450 If This Is A 7450 AIO Press Any Key To Continue If Not Close This Tool.")
        os.system("pause")
    if mdl == "7450UNK":
        print('Running Serial Reset For 7450 AIO.')
    else:
        print('Running Serial Reset For {0} AIO.'.format(mdl))
    if mdl == "7440":
        while True:
            serial = input("Please Enter The New Serial: ")
            if serial == o_serial:
                print("Serial Already Set To Specified Serial, Press Any Key To Exit!")
                os.system("pause")
                exit(0)
            if len(serial) <= 7 and serial:
                break
            print("Serial Must Be 7 Characters Or Less And Not Empty, Try Again.")
        create_40_bios(serial)
        time.sleep(1)
        subprocess.run("C:\\FPT\\40\\FPT.exe -BIOS -F C:\\TOOLS\\7440_RES\\BIOS.bin -P C:\\FPT\\40\\fparts.txt")
        reset_40_bios()
    elif mdl == "7450" or mdl == "7450UNK":
          while True:
              serial = input("Please Enter The New Serial: ")
              if serial == o_serial:
                print("Serial Already Set To Specified Serial, Press Any Key To Exit!")
                os.system("pause")
                exit(0)
                break
              if len(serial) <= 7 and serial:
                  break
              print("Serial Must Be 7 Characters Or Less And Not Empty, Try Again.")
          create_50_bios(serial)
          time.sleep(1)
          subprocess.run("C:\\FPT\\40\\FPT.exe -BIOS -F C:\\TOOLS\\7450_RES\\BIOS.bin -P C:\\FPT\\40\\fparts.txt")
          reset_50_bios()
    elif mdl == "9030":
          while True:
            serial = input("Please Enter The New Serial: ")
            if serial == o_serial:
                print("Serial Already Set To Specified Serial, Press Any Key To Exit!")
                os.system("pause")
                exit(0)
            if len(serial) <= 7 and serial:
                break
            print("Serial Must Be 7 Characters Or Less And Not Empty, Try Again.")
          create_30_bios(serial)
          time.sleep(1)
          subprocess.run("C:\\FPT\\30\\FPT.exe -BIOS -F C:\\TOOLS\\9030_RES\\BIOS.bin -P C:\\FPT\\30\\fparts.txt")
          reset_30_bios()

def long_boot():
    if mdl == "7450UNK":
        print("This unit was unknown and presumed as being a 7450 If This Is A 7450 AIO Press Any Key To Continue If Not Close This Tool.")
        os.system("pause")
    print('Running Longboot For {0} AIO.'.format(mdl))
    if mdl == "7440":
        subprocess.run("C:\\FPT\\40\\FPT.exe -ME -F C:\\TOOLS\\7440_LB\\ME.bin -P C:\\FPT\\40\\fparts.txt")
        print("Press Any Key To Finish Longboot And Restart If No Red Text Is Present If It's Present Please Close This Tool And Re-Run It.")
        os.system("pause")
        subprocess.run("C:\\FPT\\40\\FPT.exe -greset -P C:\\FPT\\40\\fparts.txt")
    elif mdl == "7450":
        subprocess.run("C:\\FPT\\40\\FPT.exe -ME -F C:\\TOOLS\\7450_LB\\ME.bin -P C:\\FPT\\40\\fparts.txt")
        print("Press Any Key To Finish Longboot And Restart If No Red Text Is Present If It's Present Please Close This Tool And Re-Run It.")
        os.system("pause")
        subprocess.run("C:\\FPT\\40\\FPT.exe -greset -P C:\\FPT\\40\\fparts.txt")
    elif mdl == "9030":
         subprocess.run("C:\\FPT\\30\\FPT.exe -ME -F C:\\TOOLS\\9030_LB\\ME.bin -P C:\\FPT\\30\\fparts.txt")
         subprocess.run("C:\\FPT\\30\\FPT.exe -DESC -F C:\\TOOLS\\9030_LB\\DESC.bin -P C:\\FPT\\30\\fparts.txt")
         print("Press Any Key To Finish Longboot And Restart If No Red Text Is Present If It's Present Please Close This Tool And Re-Run It.")
         os.system("pause")
         subprocess.run("C:\\FPT\\30\\FPT.exe -greset -P C:\\FPT\\30\\fparts.txt")
         

selection = "0"

while True:
    selection = input("Enter An Action To Perform (1-3): ")
    if selection == "1" or selection == "2" or selection == "3":
        break
    print("Invalid input! Try again.")

os.system("cls")

if selection == "1":
    serial_reset()
    print("Press Any Key To Close And If No Red Text Is Shown Above Then Process Was Successful You Can Then Reboot. If Red Text Is Shown Press Enter And Run This Tool Again.")
    os.system("pause")
elif selection == "2":
    long_boot()
elif selection == "3":
    serial_reset()
    print("Press Any Key To Continue To Longboot If No Red Text Is Present If Red Text Is Present Please Close This Tool And Re-Run It.")
    os.system("pause")
    long_boot()

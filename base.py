import sys, subprocess, os.path, time

class AttrMod:
    def __init__(self, choice):
        self.choice = choice
    
    def run(self, file, date):
        if self.choice == 1:
            self.operation = self.spawn_process("CreationTime", file, date)
        elif self.choice == 2:
            self.operation = self.spawn_process("LastWriteTime", file, date)
            if "." not in file:
                print("This option is not effective with directories.")
                return
        else:
            self.operation = self.spawn_process("LastAccessTime", file, date)
            if "." not in file:
                print("This option is not effective with directories.")
                return
            
    def spawn_process(self, operation, file, date):
        self.file = file
        try:
            com = subprocess.run(args=["powershell", "-Command", f'(Get-Item "{file}").{operation}=("{date}")'])

            # Raise exception
            com.check_returncode()

            time.sleep(1)
            self.show_attrs()

        except subprocess.CalledProcessError as e:
            print("Command returned with code %s" %e.returncode)
            
        

    def show_attrs(self):
        if self.choice == 1:
            print("New creation date: %s" %time.ctime(os.path.getctime(self.file)))
        elif self.choice == 2:
            print("New write date for %s: %s" % (self.file, time.ctime(os.path.getmtime(self.file))))
        else:
            print("New access date: %s" %time.ctime(os.path.getatime(self.file)))
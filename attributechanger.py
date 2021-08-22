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
          print(e.returncode)
        

    def show_attrs(self):
        if self.choice == 1:
            print("New creation date: %s" %time.ctime(os.path.getctime(self.file)))
        elif self.choice == 2:
            print("New write date: %s" %time.ctime(os.path.getatime(self.file)))
        else:
            print("New access date: %s" %time.ctime(os.path.getmtime(self.file)))
        

class AttrModGNU(AttrMod):
    def run(self, file, date):
        if self.choice == 1:
            self.operation = self.spawn_process("t", file, date)
        elif self.choice == 2:
            self.operation = self.spawn_process("mt", file, date)
            if "." not in file:
                print("This option is not effective with directories.")
                return
        else:
            self.operation = self.spawn_process("at", file, date)
            if "." not in file:
                print("This option is not effective with directories.")
                return

        
    def spawn_process(self, operation, file, date):
        self.file = file
        try:
            os.system(f"touch -{operation} {date} {file}")
            time.sleep(1)
            self.show_attrs()
        except Exception:
            pass

def program(object_instance, format):

    print("Choose operation")
    print("----------------")
    print("1 - Modify creation date")
    print("2 - Modify last write date")
    print("3 - Modify last access date")

    try:
        choice = int(input("> "))
        if not type(choice) is int or choice > 3 or choice < 1:
            raise ValueError("INPUT OUT OF RANGE")

        instance = object_instance(choice)

        files = str(input("> Exact file path(s): ")).split(" ")
        if not len(files) > 1:
            instance.run(files[0], str(input(f"> Date (format: {format}): ")))
        else:
            for i in files:
                instance.run(i, str(input(f"> Date for file {i} (format: {format}): ")))
    # Exception handling
    except ValueError as err:
        if hasattr(err, 'message'):
            print(err.message)
        else:
            print(err)
        # If error is risen, re-run function 
        init()

def init(os):

    if 3 != 3:
        program(AttrMod, "DD MM YYYY h:m:s")
    else:
        program(object_instance=AttrModGNU, format="YYYYMMDDhhmm")
        
if __name__ == "__main__":
    init(sys.platform)

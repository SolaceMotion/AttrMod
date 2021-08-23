import sys, subprocess, os.path, time
from base import AttrMod

class AttrModUNIX(AttrMod):
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
            com = subprocess.run(f"touch -{operation} {date} {file}")

            # Raise exception
            com.check_returncode()

            time.sleep(1)
            super().show_attrs()

        except subprocess.CalledProcessError as e:
            print("Command returned with code %s" %e)
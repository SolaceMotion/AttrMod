import sys, subprocess, os.path, time
from base import AttrMod
from derived import AttrModUNIX

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
            print()
        # If error is risen, re-run function 
        init(sys.platform)

def init(os):
    if os != "win32":
        program(object_instance=AttrMod, format="DD MM YYYY h:m:s")
    else:
        program(object_instance=AttrModUNIX, format="YYYYMMDDhhmm")
        
if __name__ == "__main__":
    init(sys.platform)

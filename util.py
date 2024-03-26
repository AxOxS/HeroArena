import sys, time

def print_running_text(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    print()
    
def print_running_info(info):
    for line in info.split("\n"):
        print_running_text(line)
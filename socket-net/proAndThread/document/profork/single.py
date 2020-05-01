from time import sleep

def sing():
    for i in range(3):
        print("I am sing %d" %i)
        sleep(1)

def dance():
    for i in range(3):
        print("I am dance %d" %i)
        sleep(1)

if __name__ == '__main__':
    sing()
    dance()

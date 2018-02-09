# coding=utf-8

def create(arg1, arg2):
    print("creating...")

def run():
    import sys
    arg1, arg2 = 1, 2
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
    except:
        pass
    print(arg1, arg2)
    create(arg1, arg2)


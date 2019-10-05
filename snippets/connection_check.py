import ctypes, win32com.client

_objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")

def check_connection():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('Error: The proces is not run with Admin permission.')
        return False
 
    if (_objCpCybos.IsConnect == 0):
        print("Connection error. ")
        return False
 
    return True
 
if __name__ == '__main__':
    if (check_connection()):
        print('connection ok')
    
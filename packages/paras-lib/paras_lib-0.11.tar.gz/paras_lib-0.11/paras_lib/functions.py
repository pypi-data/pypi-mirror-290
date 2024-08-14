import datetime
def print(txt):
    return datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S") + ' | ' + txt
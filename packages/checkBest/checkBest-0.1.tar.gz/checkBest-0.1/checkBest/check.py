import re
import jdatetime

def checkInput(inputs):
    for i in inputs:
        if not i and i != 0:
            return False
    return True


def checkPhone(phone, tp):
    if tp == 'phone':
        if not phone.startswith('09'):
            return False
    if tp == 'line':
        if not phone.startswith('0'):
            return False
    if len(phone) != 11:
        return False
    return True


def checkPassword(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True


def checkEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def checkBirthdayDate(date):
    try:
        date = jdatetime.datetime.strptime(date, '%Y/%m/%d')
        res = True
    except Exception as e:
        print(e.__class__.__name__)
        res = False
    return res


def checkInputInt(temp):
    try:
        number = int(temp)
        return number
    except ValueError:
        print('yes')
        return False

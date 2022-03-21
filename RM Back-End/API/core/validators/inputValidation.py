import re


def validate_signup_input(user_input):
    if user_input['username']:
        if validate_username(user_input['username']):
            if user_input['firstname']:
                if validate_name(user_input['firstname']):
                    if user_input['lastname']:
                        if validate_name(user_input['lastname']):
                            if user_input['email']:
                                if validate_email(user_input['email']):
                                    if user_input['password']:
                                        if validate_password(user_input['password']):
                                            return True
    else:
        return False


def validate_update_input(user_input):
    if user_input['username']:
        if not validate_username(user_input['username']):
            return False
    elif user_input['firstname']:
        if not validate_name(user_input['firstname']):
            return False
    elif user_input['lastname']:
        if validate_name(user_input['lastname']):
            return False
    elif user_input['email']:
        if not validate_email(user_input['email']):
            return False
    elif user_input['password']:
        if not validate_password(user_input['password']):
            return False
    else:
        return True


def validate_username(username):
    regex = "^[a-zA-Z0-9_.-]+$"
    if re.search(regex, username):
        return True
    else:
        return "Invalid username"


def validate_name(name):
    regex = "^[a-zA-Z]+$"
    if re.search(regex, name):
        return True
    else:
        return "invalid Name"


def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        return "Invalid Email"


def validate_password(password):
    if len(password) < 8:
        return "Make sure your password is at lest 8 letters"
    elif re.search('[0-9]', password) is None:
        return "Make sure your password has a number in it"
    elif re.search('[A-Z]', password) is None:
        return "Make sure your password has a capital letter in it"
    else:
        return True

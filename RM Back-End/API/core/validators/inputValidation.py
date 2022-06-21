import re


def validate_signup_input(user_input):
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
    if len(list(user_input.keys()))== 0:
        return True
    if user_input['firstname'] != "":
        validate_name(user_input['firstname'])
    elif user_input['lastname'] != "":
        validate_name(user_input['lastname'])
    elif user_input['email'] != "":
        validate_email(user_input['email'])
    elif user_input['old-password'] != "":
        validate_password(user_input['old-password'])
    elif user_input['password'] != "":
        validate_password(user_input['password'])
    return True


def validate_name(name):
    regex = "^[a-zA-Z]+$"
    if re.search(regex, name):
        return True
    else:
        raise CustomValidationException("invalid Name")


def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        raise CustomValidationException("Invalid Email")


def validate_password(password):
    if len(password) < 8:
        raise CustomValidationException("Password must be at lest 8 characters long!")
    elif re.search('[0-9]', password) is None:
        raise CustomValidationException("Password must has at least one number")
    elif re.search('[A-Za-z]', password) is None:
        raise CustomValidationException("Password must have at least one letter!")
    elif re.search('[A-Z]', password) is None:
        raise CustomValidationException("Password must have at least one capital letter!")
    else:
        return True


class CustomValidationException(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message

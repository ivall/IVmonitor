import bcrypt


def hash_password(password):
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password


def verify_password(password, hashed_password) -> bool:
    password = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    if bcrypt.hashpw(password, hashed_password) == hashed_password:
        return True
    return False
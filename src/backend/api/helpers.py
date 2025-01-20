from db.model import User
from crud import users

def requires_user(AccessToken: str, same_user: User | None = None) -> User | None:
    if not AccessToken:
        print("Unauthorized: No access token in cookie")
        return
    usr = users.get_by_access_token(AccessToken.strip())
    if not usr:
        print("Unauthorized: Access token not found in database")
        return
    return usr


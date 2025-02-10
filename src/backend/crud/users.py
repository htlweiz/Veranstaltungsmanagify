from api.model import SignupSchema
from crud.crud import CRUD, log_db
from db.session import session, Session
from db.model import User
import bcrypt
import uuid


class UserCRUD(CRUD[User]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, User)

    # We don't want to log the password
    def create(self, payload: SignupSchema, user_creating_id=None) -> User:
        # Hash Password
        byte_password = payload.password.encode("utf-8")
        salt = bcrypt.gensalt(8)
        hsh = bcrypt.hashpw(byte_password, salt)

        # Generate random Access Token
        access_token = str(uuid.uuid4())

        user = User(
            email=payload.email,
            password=hsh.decode("utf-8"),
            access_token=access_token,
            username=payload.username,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    @log_db(class_name="User")
    def get_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).first()

    @log_db(class_name="User")
    def get_by_access_token(self, access_token: str) -> User:
        return self.session.query(User).filter_by(access_token=access_token).first()


users = UserCRUD(session)
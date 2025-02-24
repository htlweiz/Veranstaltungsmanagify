import sqlalchemy.exc
from api.model import SignupSchema, UserPatch, UserSchema
from crud.crud import CRUD, log_db
from db.session import session, Session
import sqlalchemy
from fastapi import HTTPException
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
            role_id=payload.role_id,
        )
        try:
            self.session.add(user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

        self.session.refresh(user)
        return user
    
    def patch(self, id, request: UserPatch) -> User:
        user = self.session.query(User).filter_by(user_id=id).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        if request.password is not None:
            byte_password = request.password.encode("utf-8")
            salt = bcrypt.gensalt(8)
            hsh = bcrypt.hashpw(byte_password, salt)

            user.password = hsh.decode("utf-8")
        
        if request.email is not None:
            user.email = request.email
        
        if request.username is not None:
            user.username = request.username
        
        if request.role_id is not None: 
            user.role_id = request.role_id

        try:
            self.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            if "users_username_key" in str(e):
                raise HTTPException(status_code=400, detail="Username already in use")
            if "users_email_key" in str(e):
                raise HTTPException(status_code=400, detail="E-Mail already in use")
        except Exception as e:
            self.session.rollback()
            raise e

        self.session.refresh(user)
        return user
    
    def put(self, id, request):
        return self.patch(id, request)

    @log_db(class_name="User")
    def get_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).first()

    @log_db(class_name="User")
    def get_by_access_token(self, access_token: str) -> User:
        return self.session.query(User).filter_by(access_token=access_token).first()


users = UserCRUD(session)
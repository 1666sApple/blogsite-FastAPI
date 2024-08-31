from passlib.context import CryptContext

pwd = CryptContext(schemes='bcrypt', deprecated='auto')

class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        """Hash the given password using bcrypt."""
        return pwd.hash(password)
        
    @staticmethod
    def verify(hashed_password: str, unhashed_password: str) -> bool:
        """Verify that the unhashed password matches the hashed password."""
        return pwd.verify(unhashed_password, hashed_password)
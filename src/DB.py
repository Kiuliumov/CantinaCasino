from typing import Optional, List
from sqlalchemy import Column, Integer, BigInteger, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()


class User(Base):
    """
    Represents a global Discord user.
    """
    __tablename__ = "users"

    discord_id: int = Column(BigInteger, primary_key=True, unique=True)
    balance: int = Column(Integer, default=0)
    experience: int = Column(Integer, default=0)
    level: int = Column(Integer, default=1)

    def __repr__(self) -> str:
        return (f"<User {self.discord_id} | Balance {self.balance} | "
                f"EXP {self.experience} | Level {self.level}>")


class Database:
    """
    Global database for Discord users with lazy ranking.
    """
    def __init__(self, db_path: str = "cantina.db") -> None:
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def add_user(self, discord_id: int) -> User:
        """
        Adds a new user globally if they don't exist.
        """
        session: Session = self.SessionLocal()
        try:
            user = session.query(User).filter_by(discord_id=discord_id).first()
            if not user:
                user = User(discord_id=discord_id)
                session.add(user)
                session.commit()
                session.refresh(user)
        finally:
            session.close()
        return user

    def get_user(self, discord_id: int) -> Optional[User]:
        """
        Returns the user object if exists, else None.
        """
        session: Session = self.SessionLocal()
        try:
            user = session.query(User).filter_by(discord_id=discord_id).first()
        finally:
            session.close()
        return user

    def update_balance(self, discord_id: int, amount: int) -> None:
        """
        Updates the user's balance.
        """
        session: Session = self.SessionLocal()
        try:
            user = session.query(User).filter_by(discord_id=discord_id).first()
            if user:
                user.balance += amount
                session.commit()
        finally:
            session.close()

    def set_balance(self, discord_id: int, amount: int) -> None:
        """
        Sets the user's balance.
        """
        session: Session = self.SessionLocal()
        try:
            user = session.query(User).filter_by(discord_id=discord_id).first()
            if user:
                user.balance = amount
                session.commit()
        finally:
            session.close()

    def update_experience(self, discord_id: int, exp: int) -> None:
        """
        Adds experience points to a user and auto-levels them.
        """
        session: Session = self.SessionLocal()
        try:
            user = session.query(User).filter_by(discord_id=discord_id).first()
            if user:
                user.experience += exp
                new_level = int((user.experience // 100) ** 0.5) + 1
                if new_level > user.level:
                    user.level = new_level
                session.commit()
        finally:
            session.close()

    def set_experience(self, discord_id: int, exp: int) -> None:
        """
        Sets experience for a user.
        """
        session: Session = self.SessionLocal()
        try:
            user = session.query(User).filter_by(discord_id=discord_id).first()
            if user:
                user.experience = exp
                session.commit()
        finally:
            session.close()

    def top_balance(self, limit: int = 10, offset: int = 0) -> List[User]:
        """
        Returns top users globally by balance with optional offset.
        """
        session: Session = self.SessionLocal()
        try:
            users = session.query(User).order_by(User.balance.desc(), User.discord_id.asc())\
                .offset(offset).limit(limit).all()
        finally:
            session.close()
        return users

    def top_experience(self, limit: int = 10, offset: int = 0) -> List[User]:
        """
        Returns top users globally by experience with optional offset.
        """
        session: Session = self.SessionLocal()
        try:
            users = session.query(User).order_by(User.experience.desc(), User.discord_id.asc())\
                .offset(offset).limit(limit).all()
        finally:
            session.close()
        return users

    def get_balance_rank(self, discord_id: int) -> int:
        """
        Returns the global balance rank of the user (1-based).
        """
        session: Session = self.SessionLocal()
        try:
            user = session.query(User).filter_by(discord_id=discord_id).first()
            if not user:
                return 0
            rank = session.query(User).filter(User.balance > user.balance).count() + 1
            return rank
        finally:
            session.close()

    def get_experience_rank(self, discord_id: int) -> int:
        """
        Returns the global experience rank of the user (1-based).
        """
        session: Session = self.SessionLocal()
        try:
            user = session.query(User).filter_by(discord_id=discord_id).first()
            if not user:
                return 0
            rank = session.query(User).filter(User.experience > user.experience).count() + 1
            return rank
        finally:
            session.close()

    def leaderboard(self, by: str = "balance", limit: int = 10, offset: int = 0) -> List[User]:
        """
        Returns a global leaderboard.
        'by' can be 'balance' or 'experience'.
        Supports limit and offset for pagination.
        """
        if by == "balance":
            return self.top_balance(limit=limit, offset=offset)
        elif by == "experience":
            return self.top_experience(limit=limit, offset=offset)
        else:
            raise ValueError("Leaderboard 'by' must be 'balance' or 'experience'")

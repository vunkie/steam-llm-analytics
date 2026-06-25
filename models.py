from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Games(Base):
    __tablename__ = "games"
    appid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    img_icon_url: Mapped[str]
    playtime_forever: Mapped[int]
    playtime_windows_forever: Mapped[int]
    playtime_linux_forever: Mapped[int]
    playtime_deck_forever: Mapped[int]
    playtime_disconnected: Mapped[int]
    rtime_last_played: Mapped[datetime] = mapped_column(DateTime(timezone=True))

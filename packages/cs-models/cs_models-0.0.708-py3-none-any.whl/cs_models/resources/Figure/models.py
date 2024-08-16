from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Text,
    Boolean,
    ForeignKey,
)

from ...database import Base


class FigureModel(Base):
    __tablename__ = "figures"

    id = Column(Integer, primary_key=True)
    file_id = Column(
        Integer,
        ForeignKey('files.id'),
        nullable=True,
    )
    source_type = Column(String(50), nullable=False)
    source_id = Column(Integer, nullable=False)
    figure_label = Column(String(50), nullable=True)
    figure_caption = Column(Text, nullable=True)
    figure_description = Column(Text, nullable=True)
    figure_link = Column(String(255), nullable=True)
    llm_processed = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

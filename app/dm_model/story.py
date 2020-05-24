from .base import db, Base
import enum
from ..models.fileType import fileType

class Type(enum.Enum):
    IMAGE = "IMAGE"
    VEDIO = "VEDIO"
    TEXT = "TEXT"

class Story(Base):

    user_name = db.Column(db.String(80), unique=False, nullable=False)
    story_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    type_of_story = db.Column(db.Enum(Type),  default=Type.TEXT)
    file_data_location = db.Column(db.String(200))
    latitude = db.Column(db.String(200), unique=False, nullable=True)
    longitude = db.Column(db.String(200), unique=False, nullable=True)


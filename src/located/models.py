from sqlalchemy import Column, Date, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base


class Located(Base):
    __tablename__ = "located"
    __table_args__ = (PrimaryKeyConstraint("Id_Users_adresses", "Id_Code_Postal"),)

    Id_Users_adresses = Column(
        Integer, ForeignKey("Users_adresses.Id_Users_adresses"), nullable=False
    )
    Id_Code_Postal = Column(
        Integer, ForeignKey("code_postal.Id_Code_Postal"), nullable=False
    )
    users_adresses = relationship("Users_adresses", back_populates="locate")
    code_postal = relationship("Code_Postal", back_populates="locate")

from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, String
from database import Base


class Redact(Base):
    __tablename__ = "redact"

    Id_Recipes = Column(Integer, ForeignKey("recipes.Id_Recipes"), primary_key=True)
    Id_Admin = Column(Integer, ForeignKey("admin.Id_Admin"), primary_key=True)

    __table_args__ = (PrimaryKeyConstraint("Id_Recipes", "Id_Admin"),)

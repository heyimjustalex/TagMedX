from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# SQLAlchemy models that map to /DB/setup.sql in MYSQL database


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    e_mail = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String)
    surname = Column(String)
    title = Column(String)
    role = Column(String, nullable=False, default="User")
    description = Column(String)
    experience = Column(String)

    # Define the one-to-many relationship with Membership
    Membership = relationship("Membership", back_populates="User")

    # Define the one-to-many relationship with Examination
    Examination = relationship("Examination", back_populates="User")


class Membership(Base):
    __tablename__ = "Membership"

    id_user = Column(Integer, ForeignKey("User.id"), primary_key=True)
    id_group = Column(Integer, ForeignKey("Group.id"), primary_key=True)

    # Define the many-to-one relationship with User
    User = relationship("User", back_populates="Membership")

    # Define the many-to-one relationship with Group
    Group = relationship("Group", back_populates="Membership")


class Group(Base):
    __tablename__ = "Group"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # Define the one-to-many relationship with Task
    Task = relationship("Task", back_populates="Group")

    # Define the one-to-many relationship with Group
    Membership = relationship("Membership", back_populates="Group")


class Task(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True)
    id_group = Column(Integer, ForeignKey("Group.id"), nullable=False)
    max_samples_for_user = Column(Integer)
    name = Column(String)
    description = Column(String)
    type = Column(String)

    # Define the many-to-one relationship with Group
    Group = relationship("Group", back_populates="Task")

    # Define the one-to-many relationship with Sample
    Sample = relationship("Sample", back_populates="Task")

    # Define the one-to-many relationship with Label
    Label = relationship("Label", back_populates="Task")


class Sample(Base):
    __tablename__ = "Sample"

    id = Column(Integer, primary_key=True)
    id_task = Column(Integer, ForeignKey("Task.id"), nullable=False)
    path = Column(String)
    format = Column(String)

    # Define the many-to-one relationship with Task
    Task = relationship("Task", back_populates="Sample")

    # Define the one-to-many relationship with Examination
    Examination = relationship("Examination", back_populates="Sample")


class Examination(Base):
    __tablename__ = "Examination"

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("User.id"), nullable=False)
    id_sample = Column(Integer, ForeignKey("Sample.id"), nullable=False)
    to_further_verification = Column(Boolean)
    bad_quality = Column(Boolean)

    # Define the many-to-one relationship with User
    User = relationship("User", back_populates="Examination")

    # Define the many-to-one relationship with Sample
    Sample = relationship("Sample", back_populates="Examination")

    # Define the one-to-many relationship with BBox
    BBox = relationship("BBox", back_populates="Examination")


class Label(Base):
    __tablename__ = "Label"

    id = Column(Integer, primary_key=True)
    id_task = Column(Integer, ForeignKey("Task.id"), nullable=False)
    name = Column(String)
    description = Column(String)

    # Define the many-to-one relationship with Task
    Task = relationship("Task", back_populates="Label")

    # Define the one-to-many relationship with BBox
    BBox = relationship("BBox", back_populates="Label")


class BBox(Base):
    __tablename__ = "BBox"

    id = Column(Integer, primary_key=True)
    id_examination = Column(Integer, ForeignKey("Examination.id"), nullable=False)
    id_label = Column(Integer, ForeignKey("Label.id"), nullable=False)
    comment = Column(String)
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)

    # Define the many-to-one relationship with Examination
    Examination = relationship("Examination", back_populates="BBox")

    # Define the many-to-one relationship with Label
    Label = relationship("Label", back_populates="BBox")

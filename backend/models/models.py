from sqlalchemy import ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


# SQLAlchemy models that map to /DB/setup.sql in MYSQL database


class User(Base):
    __tablename__ = "User"

    id = mapped_column(Integer, primary_key=True)
    e_mail = mapped_column(String, nullable=False)
    password_hash = mapped_column(String, nullable=False)
    name = mapped_column(String)
    surname = mapped_column(String)
    title = mapped_column(String)
    
    specialization = mapped_column(String)
    practice_start_year = mapped_column(Integer)

    # Define the one-to-many relationship with Membership
    Membership = relationship("Membership", back_populates="User")

    # Define the one-to-many relationship with Examination
    Examination = relationship("Examination", back_populates="User")


class Membership(Base):
    __tablename__ = "Membership"

    id_user = mapped_column(Integer, ForeignKey("User.id"), primary_key=True)
    id_group = mapped_column(Integer, ForeignKey("Group.id"), primary_key=True)
    role = mapped_column(String, nullable=False, default="User")

    # Define the many-to-one relationship with User
    User = relationship("User", back_populates="Membership")

    # Define the many-to-one relationship with Group
    Group = relationship("Group", back_populates="Membership")


class Group(Base):
    __tablename__ = "Group"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=False)
    connection_string = mapped_column(String)
    # Define the one-to-many relationship with Task
    Task = relationship("Task", back_populates="Group")

    # Define the one-to-many relationship with Group
    Membership = relationship("Membership", back_populates="Group")


class Task(Base):
    __tablename__ = "Task"

    id = mapped_column(Integer, primary_key=True)
    id_group = mapped_column(Integer, ForeignKey("Group.id"), nullable=False)
    max_samples_for_user = mapped_column(Integer)
    name = mapped_column(String)
    description = mapped_column(String)
    type = mapped_column(String)
    

    # Define the many-to-one relationship with Group
    Group = relationship("Group", back_populates="Task")

    # Define the one-to-many relationship with Sample
    Sample = relationship("Sample", back_populates="Task")

    # Define the one-to-many relationship with Label
    Label = relationship("Label", back_populates="Task")


class Sample(Base):
    __tablename__ = "Sample"

    id = mapped_column(Integer, primary_key=True)
    id_task = mapped_column(Integer, ForeignKey("Task.id"), nullable=False)
    path = mapped_column(String)
    format = mapped_column(String)

    # Define the many-to-one relationship with Task
    Task = relationship("Task", back_populates="Sample")

    # Define the one-to-many relationship with Examination
    Examination = relationship("Examination", back_populates="Sample")


class Examination(Base):
    __tablename__ = "Examination"

    id = mapped_column(Integer, primary_key=True)
    id_user = mapped_column(Integer, ForeignKey("User.id"), nullable=False)
    id_sample = mapped_column(Integer, ForeignKey("Sample.id"), nullable=False)
    to_further_verification = mapped_column(Boolean)
    bad_quality = mapped_column(Boolean)

    # Define the many-to-one relationship with User
    User = relationship("User", back_populates="Examination")

    # Define the many-to-one relationship with Sample
    Sample = relationship("Sample", back_populates="Examination")

    # Define the one-to-many relationship with BBox
    BBox = relationship("BBox", back_populates="Examination")


class Label(Base):
    __tablename__ = "Label"

    id = mapped_column(Integer, primary_key=True)
    id_task = mapped_column(Integer, ForeignKey("Task.id"), nullable=False)
    name = mapped_column(String)
    description = mapped_column(String)

    # Define the many-to-one relationship with Task
    Task = relationship("Task", back_populates="Label")

    # Define the one-to-many relationship with BBox
    BBox = relationship("BBox", back_populates="Label")


class BBox(Base):
    __tablename__ = "BBox"

    id = mapped_column(Integer, primary_key=True)
    id_examination = mapped_column(
        Integer, ForeignKey("Examination.id"), nullable=False
    )
    id_label = mapped_column(Integer, ForeignKey("Label.id"), nullable=False)
    comment = mapped_column(String)
    x1 = mapped_column(Float)
    y1 = mapped_column(Float)
    x2 = mapped_column(Float)
    y2 = mapped_column(Float)

    # Define the many-to-one relationship with Examination
    Examination = relationship("Examination", back_populates="BBox")

    # Define the many-to-one relationship with Label
    Label = relationship("Label", back_populates="BBox")

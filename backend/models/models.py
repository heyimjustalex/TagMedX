from sqlalchemy import ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped
from typing import List


class Base(DeclarativeBase):
    pass


# SQLAlchemy models that map to /DB/setup.sql in MYSQL database


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    e_mail: Mapped[str]
    password_hash: Mapped[str]
    name: Mapped[str | None]
    surname: Mapped[str | None]
    title: Mapped[str | None]
    specialization: Mapped[str | None]
    practice_start_year: Mapped[int | None]

    # Define the one-to-many relationship with Membership
    Membership: Mapped[List["Membership"]] = relationship(back_populates="User")

    # Define the one-to-many relationship with Examination
    Examination: Mapped[List["Examination"]] = relationship(back_populates="User")
    
    # Define the one-to-many relationship with Package
    Package: Mapped[List["Package"]] = relationship(back_populates="User")


class Membership(Base):
    __tablename__ = "Membership"

    id_user: Mapped[int] = mapped_column(ForeignKey("User.id"), primary_key=True)
    id_group: Mapped[int] = mapped_column(ForeignKey("Group.id"), primary_key=True)
    role: Mapped[str] = mapped_column(default="User")

    # Define the many-to-one relationship with User
    User: Mapped["User"] = relationship(back_populates="Membership")

    # Define the many-to-one relationship with Group
    Group: Mapped["Group"] = relationship(back_populates="Membership")


class Group(Base):
    __tablename__ = "Group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    connection_string: Mapped[str]
    # Define the one-to-many relationship with Set
    Set: Mapped[List["Set"]] = relationship(back_populates="Group")

    # Define the one-to-many relationship with Group
    Membership: Mapped[List["Membership"]] = relationship(back_populates="Group")


class Set(Base):
    __tablename__ = "Set"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_group: Mapped[int] = mapped_column(ForeignKey("Group.id"))
    max_samples_for_user: Mapped[int | None]
    name: Mapped[str | None]
    description: Mapped[str | None]
    type: Mapped[str | None]

    # Define the many-to-one relationship with Group
    Group: Mapped["Group"] = relationship(back_populates="Set")

    # Define the one-to-many relationship with Package
    Package: Mapped[List["Package"]] = relationship(back_populates="Set")

    # Define the one-to-many relationship with Label
    Label: Mapped[List["Label"]] = relationship(back_populates="Set")


class Sample(Base):
    __tablename__ = "Sample"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_package: Mapped[int] = mapped_column(ForeignKey("Package.id"))
    id_user: Mapped[int | None] = mapped_column(ForeignKey("User.id"))
    path: Mapped[str | None]
    format: Mapped[str | None]

    # Define the many-to-one relationship with Package
    Package: Mapped["Package"] = relationship(back_populates="Sample")

    # Define the one-to-many relationship with Examination
    Examination: Mapped[List["Examination"]] = relationship(back_populates="Sample")

class Package(Base):
    __tablename__ = "Package"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_set: Mapped[int] = mapped_column(ForeignKey("Set.id"))
    id_user: Mapped[int | None] = mapped_column(ForeignKey("User.id"))
    is_ready: Mapped[bool | None]
    # Define the one-to-many relationship with Sample
    Sample: Mapped["Sample"] = relationship(back_populates="Package")
    # Define the many-to-one relationship with Set
    Set: Mapped["Set"] = relationship(back_populates="Package")
     # Define the many-to-one relationship with User
    User: Mapped["User"] = relationship(back_populates="Package")

class Examination(Base):
    __tablename__ = "Examination"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("User.id"))
    id_sample: Mapped[int] = mapped_column(ForeignKey("Sample.id"))
    to_further_verification: Mapped[bool | None]
    bad_quality: Mapped[bool | None]

    # Define the many-to-one relationship with User
    User: Mapped["User"] = relationship(back_populates="Examination")

    # Define the many-to-one relationship with Sample
    Sample: Mapped["Sample"] = relationship(back_populates="Examination")

    # Define the one-to-many relationship with BBox
    BBox: Mapped[List["BBox"]] = relationship(back_populates="Examination")


class Label(Base):
    __tablename__ = "Label"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_set: Mapped[int] = mapped_column(ForeignKey("Set.id"))
    name: Mapped[str | None]
    description: Mapped[str | None]

    # Define the many-to-one relationship with Set
    Set: Mapped["Set"] = relationship(back_populates="Label")

    # Define the one-to-many relationship with BBox
    BBox: Mapped[List["BBox"]] = relationship(back_populates="Label")


class BBox(Base):
    __tablename__ = "BBox"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_examination: Mapped[int] = mapped_column(ForeignKey("Examination.id"))
    id_label: Mapped[int] = mapped_column(ForeignKey("Label.id"))
    comment: Mapped[str | None]
    x1: Mapped[float | None]
    y1: Mapped[float | None]
    x2: Mapped[float | None]
    y2: Mapped[float | None]

    # Define the many-to-one relationship with Examination
    Examination: Mapped["Examination"] = relationship(back_populates="BBox")

    # Define the many-to-one relationship with Label
    Label: Mapped["Label"] = relationship(back_populates="BBox")

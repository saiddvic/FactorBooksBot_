# from sqlalchemy import BigInteger, VARCHAR
# from sqlalchemy.orm import mapped_column, Mapped, relationship
#
# from db import Order
# from db.base import CreateModel


# class User(CreateModel):
#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     first_name: Mapped[str] = mapped_column(VARCHAR(255))
#     username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
#     phone_number: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
#     order: Mapped[list['Order']] = relationship('Order', back_populates='user')


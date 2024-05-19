# from sqlalchemy import BigInteger, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from db import CreateModel, User, Product


# class Order(CreateModel):
#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(User.id, ondelete='CASCADE'))
#     product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Product.id, ondelete='CASCADE'))
#
#     user: Mapped[User] = relationship("User", back_populates="orders")
#     product: Mapped[Product] = relationship("Product", back_populates="orders")

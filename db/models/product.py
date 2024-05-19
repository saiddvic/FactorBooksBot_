from sqlalchemy import BigInteger, VARCHAR, ForeignKey, select
from sqlalchemy.orm import mapped_column, Mapped, relationship


from db.base import CreateModel, db
from db.utils import CustomImageField

class User(CreateModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(255))
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    orders: Mapped[list['Order']] = relationship('Order', back_populates='users')


class Category(CreateModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    products: Mapped[list['Product']] = relationship("Product", back_populates="category")
class Product(CreateModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    price: Mapped[str] = mapped_column(BigInteger, nullable=True)
    photo: Mapped[str] = mapped_column(CustomImageField)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete='CASCADE'))
    category: Mapped[Category] = relationship("Category", back_populates="products")
    orders: Mapped[list['Order']] = relationship("Order", back_populates='products')

    @classmethod
    async def get_products_by_category_id(cls, category_id):
        query = select(cls).where(cls.category_id == category_id)
        return (await db.execute(query)).scalars()


class Order(CreateModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(User.id, ondelete='CASCADE'))
    category_id: Mapped[int] = mapped_column(BigInteger)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Product.id, ondelete='CASCADE'))
    quantity_of_books: Mapped[int] = mapped_column(BigInteger, nullable=True)
    users: Mapped[User] = relationship("User", back_populates="orders")
    products: Mapped[Product] = relationship("Product", back_populates="orders")




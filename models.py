from app import db, session, Base


class Parseritem(Base):
    __tablename__ = 'parseitems'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    usd_price = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)


import json

from sqlalchemy import create_engine, Column, Integer, String, and_, Date, Numeric, UniqueConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.testing import db

# 创建数据库连接
engine = create_engine('mysql+pymysql://root:XBJmysql126%40@192.168.1.22:3306/test_data?charset=utf8mb4')
Base = declarative_base()
Session = sessionmaker(bind=engine)
data_session = Session()


# 店铺
class TmPromotion(Base):
    __tablename__ = 'data_tm_link_promotion'

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, nullable=False)
    promotionId = Column(String(20), nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String(10), nullable=False)
    charge = Column(Numeric(15, 2), nullable=False)
    alipayInshopAmt = Column(Numeric(15, 2), nullable=False)
    click = Column(Integer, nullable=False)
    adPv = Column(Integer, nullable=False)

    @staticmethod
    def upsert(data: list, date, shop_id):
        data_session.query(TmPromotion).filter(and_(TmPromotion.date == date, TmPromotion.shop_id == shop_id,
                                                    TmPromotion.promotionId == data['promotionId'])).delete()
        data_session.add_all(data)
        data_session.commit()


class TmCTB(Base):
    __tablename__ = 'data_tm_link_ctb'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    shop_id = Column(Integer, nullable=False)
    link_id = Column(String(20), nullable=False)

    sales = Column(Numeric(15, 2), nullable=False)
    refund = Column(Numeric(15, 2), nullable=False)
    replenish = Column(Numeric(15, 2), nullable=False)
    replenish_count = Column(Integer, nullable=False)

    @staticmethod
    def upsert(data: list, date, shop_id):
        data_session.query(TmCTB).filter(
            and_(TmCTB.date == date, TmCTB.shop_id == shop_id, TmCTB.link_id == data['link_id'])).delete()
        data_session.add_all(data)
        data_session.commit()


class PddPlatform(Base):
    __tablename__ = 'data_pdd_platform'

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    deal_amount = Column(Numeric(10, 2), nullable=False, comment='成交金额')
    refund_amount = Column(Numeric(10, 2), nullable=False, comment='退款金额')
    dd_search = Column(Numeric(10, 2), nullable=False, comment='多多搜索')
    dd_scene = Column(Numeric(10, 2), nullable=False, comment='多多推广')
    fxt = Column(Numeric(10, 2), nullable=False, comment='方向台')
    qztg = Column(Numeric(10, 2), nullable=False, comment='全站推广')
    bztg = Column(Numeric(10, 2), nullable=False, comment='标准推广')
    sptg = Column(Numeric(10, 2), nullable=False, comment='商品推广')

    __table_args__ = (
        UniqueConstraint("shop_id", "date", name='unique_shop_id_date'),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def upsert(data):
        data_session.query(PddPlatform).filter(and_(PddPlatform.date.in_([i.date for i in data]),
                                                    PddPlatform.shop_id.in_([i.shop_id for i in data]))).delete()
        data_session.add_all(data)
        data_session.commit()


class JdPlatform(Base):
    __tablename__ = 'data_jd_platform'

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    jbkk = Column(Numeric(10, 2), nullable=False, comment='价保扣款')
    htkc = Column(Numeric(10, 2), nullable=False, comment='海投快车')

    __table_args__ = (
        UniqueConstraint("shop_id", "date", name='unique_shop_id_date'),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def upsert(data):
        data_session.query(JdPlatform).filter(and_(JdPlatform.date.in_([i.date for i in data]),
                                                   JdPlatform.shop_id.in_([i.shop_id for i in data]))).delete()
        data_session.add_all(data)
        data_session.commit()

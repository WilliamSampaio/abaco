import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class MovimentacaoEnum(enum.Enum):
    Compra = 1
    Venda = 2
    Bonificacao = 3

    @classmethod
    def names(cls):
        return list(map(lambda c: c.name, cls))


class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)
    password = Column(String(32), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class Negociacoes(Base):
    __tablename__ = 'negociacoes'

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('wallet.id'), nullable=False)
    ticker = Column(String(10), nullable=False)
    movimentacao = Column(Enum(MovimentacaoEnum), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Float(precision=2), nullable=False, default=0.0)
    valor_total = Column(Float(precision=2), nullable=False, default=0.0)
    nota = Column(String(20), nullable=False, default='')
    data_pregao = Column(Date, nullable=False)
    observacao = Column(String(100), nullable=False, default='')
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    def to_dict(self):
        return {
            'id': self.id,
            'wallet_id': self.wallet_id,
            'ticker': self.ticker,
            'movimentacao': self.movimentacao,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'valor_total': self.valor_total,
            'nota': self.nota,
            'data_pregao': self.data_pregao,
            'observacao': self.observacao,
            'created_at': self.created_at,
        }

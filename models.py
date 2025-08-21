from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import create_engine

Base = declarative_base()

class TradingNarrative(Base):
    __tablename__ = 'trading_narrative'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    entry_type = Column(String(50))  # 'scan_results', 'position_update', 'market_analysis', 'strategy_note'
    content = Column(Text)
    meta_data = Column(JSON)  # Store additional structured data
    confidence_score = Column(Float)
    symbols = Column(String(200))  # Comma-separated symbols related to this entry
    source_device = Column(String(50))  # 'desktop', 'android', 'replit'
    created_by = Column(String(100))  # Claude instance identifier
    
class ScanResults(Base):
    __tablename__ = 'scan_results'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    scan_type = Column(String(50))  # 'social_sentiment', 'technical_analysis', 'confluence'
    symbol = Column(String(20))
    confidence_score = Column(Float)
    technical_data = Column(JSON)  # RSI, MACD, etc.
    social_data = Column(JSON)  # LunarCrush data
    confluence_signals = Column(JSON)
    recommendation = Column(String(20))  # 'buy', 'sell', 'hold', 'watch'
    price_target = Column(Float)
    stop_loss = Column(Float)
    reasoning = Column(Text)
    
class Positions(Base):
    __tablename__ = 'positions'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    symbol = Column(String(20))
    action = Column(String(10))  # 'open', 'close', 'update'
    entry_price = Column(Float)
    current_price = Column(Float)
    quantity = Column(Float)
    pnl_usd = Column(Float)
    pnl_percent = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    reasoning = Column(Text)
    status = Column(String(20))  # 'active', 'closed', 'watching'
    exchange = Column(String(20))
    
class TradingContext(Base):
    __tablename__ = 'trading_context'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    context_key = Column(String(100), unique=True)  # 'current_strategy', 'market_outlook', 'risk_profile'
    context_value = Column(Text)
    meta_data = Column(JSON)
    last_updated_by = Column(String(100))
    
# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
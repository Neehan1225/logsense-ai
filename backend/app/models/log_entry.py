from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import datetime
import enum  
Base = declarative_base()

class LogLevel(str, enum.Enum):
    INFO = "INFO"         
    WARNING = "WARNING"  
    ERROR = "ERROR"       
    CRITICAL = "CRITICAL"
    DEBUG = "DEBUG"

class LogEntry(Base):
    
    __tablename__ = "log_entries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    service_name = Column(String(255), nullable=False)
    
    level = Column(Enum(LogLevel), nullable=False, default=LogLevel.INFO)
    
    message = Column(Text, nullable=False)
    
    source_ip = Column(String(45), nullable=True)
    
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    ai_analysis = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<LogEntry(id={self.id}, level={self.level}, service={self.service_name})>"
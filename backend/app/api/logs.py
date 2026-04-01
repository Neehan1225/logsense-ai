from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from pydantic import BaseModel
from typing import Optional, List
import datetime

from app.core.database import get_db
from app.models.log_entry import LogEntry, LogLevel

router = APIRouter(prefix="/logs", tags=["logs"])

class LogCreate(BaseModel):
    service_name: str         
    level: LogLevel           
    message: str               
    source_ip: Optional[str] = None  
    
    class Config:
        
        use_enum_values = True

class LogResponse(BaseModel):
    id: int
    service_name: str
    level: str
    message: str
    source_ip: Optional[str]
    timestamp: datetime.datetime
    ai_analysis: Optional[str]
    
    class Config:
        from_attributes = True

@router.post("/", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
def create_log(
    log_data: LogCreate,     
    db: Session = Depends(get_db) 
):
    """
    Create a new log entry.
    
    This docstring appears in your auto-generated API documentation!
    Send a POST request to /logs/ with JSON body to create a log.
    """
    db_log = LogEntry(**log_data.dict())
    
    db.add(db_log)
    
    db.commit()
    
    db.refresh(db_log)
    
    return db_log

@router.get("/", response_model=List[LogResponse])
def get_logs(

    skip: int = 0,          
    limit: int = 50,         
    level: Optional[str] = None,   
    service: Optional[str] = None,  
    db: Session = Depends(get_db)
):
    """Get all logs with optional filtering and pagination."""
    
    query = db.query(LogEntry)
    
    if level:
        query = query.filter(LogEntry.level == level)
    
    if service:

        query = query.filter(LogEntry.service_name.ilike(f"%{service}%"))
    
    query = query.order_by(LogEntry.timestamp.desc())
    
    logs = query.offset(skip).limit(limit).all()
    
    return logs

@router.get("/{log_id}", response_model=LogResponse)
def get_log(
    log_id: int,
    db: Session = Depends(get_db)
):
    """Get a single log entry by its ID."""
    

    log = db.query(LogEntry).filter(LogEntry.id == log_id).first()
    

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log with id {log_id} not found"
        )
    
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(
    log_id: int,
    db: Session = Depends(get_db)
):
    """Delete a log entry by ID. Returns 204 No Content on success."""
    
    log = db.query(LogEntry).filter(LogEntry.id == log_id).first()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log with id {log_id} not found"
        )
    
    db.delete(log)
    db.commit()
    
    return None
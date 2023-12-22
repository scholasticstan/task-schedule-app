#!/usr/bin/env python3
"""Base class task. This class maps to the 'tasks' table."""

from models.base import Base, Activity
from sqlalchemy import Column, ForeignKey, String, Enum


class Task(Activity, Base):
    """Base class for Activity. This class maps to the 'Activities' table."""

    __tablename__ = "tasks"
    name = Column(String(16), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    start_date = Column(String(16), nullable=False)
    end_date = Column(String(16), nullable=False)
    stop_time = Column(String(16), nullable=False)
    status = Column(Enum("pending", "active", "completed", "abort"), default="pending", server_default="pending")
    priority = Column(Enum("low", "medium", "high"), default="low", server_default="low")

    
    def __init__(self, name, user_id, start_date, end_date, stop_time, status=None, priority=None):
      """ """
      super().__init__()
      self.name = name
      self.user_id = user_id
      self.start_date = start_date
      self.end_date = end_date
      self.stop_time = stop_time
      self.status = status if status is not None and status != "" else "pending"
      self.priority = priority if priority is not None and priority != "" else "low"
      
    
    

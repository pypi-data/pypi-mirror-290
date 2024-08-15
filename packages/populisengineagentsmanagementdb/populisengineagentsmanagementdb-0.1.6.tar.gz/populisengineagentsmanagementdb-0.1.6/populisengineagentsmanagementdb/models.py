from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional, Dict, Any
import datetime

class UserModel(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id") 
    userEmail: str
    whatsApp: str
    language: str
    name: str
    personasStart: List[str]
    personasResume: List[str]
    personas: List[str]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # To allow ObjectId
        json_encoders = {ObjectId: str} 

class CompanyModel(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    name: str
    language: str
    step: str
    erp: List[str]
    personasStart: List[str]
    personasResume: List[str]
    personas: List[str]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
class LogModel(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    timestamp: datetime.datetime
    collection: str
    operation: str
    document: Optional[Dict[str, Any]]
    old_document: Optional[Dict[str, Any]]
    user: Optional[str]
    company: Optional[str]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ContentItem(BaseModel):
    content01: Optional[Dict[str, Any]] = None
    content02: Optional[Dict[str, Any]] = None

class SessionModel(BaseModel):
    idUser: str
    timestamp: datetime.datetime
    content: List[ContentItem]



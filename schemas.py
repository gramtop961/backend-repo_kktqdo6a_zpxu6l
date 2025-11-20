from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class Project(BaseModel):
    title: str = Field(..., description="Project title")
    summary: str = Field(..., description="Short description")
    tags: List[str] = Field(default_factory=list, description="Tags/technologies")
    url: Optional[str] = Field(None, description="Live/demo URL")
    repo: Optional[str] = Field(None, description="Repository URL")

class Message(BaseModel):
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    subject: Optional[str] = Field(None, description="Subject")
    message: str = Field(..., description="Message body")

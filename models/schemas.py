from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Програмний продукт розроблено Соколом Андрієм - Falkon AI

class UserProfile(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime
    credits_left: int = 2
    is_premium: bool = False
    is_admin: bool = False

class ProjectBase(BaseModel):
    title: str
    description: str

class Project(ProjectBase):
    id: str
    user_id: str
    created_at: datetime
    status: str # 'brainstorming', 'researching', 'questioning', 'completed'

class ProjectStep(BaseModel):
    id: str
    project_id: str
    step_type: str # 'brainstorm', 'market_research', 'questions', 'final_prd'
    content: str
    created_at: datetime

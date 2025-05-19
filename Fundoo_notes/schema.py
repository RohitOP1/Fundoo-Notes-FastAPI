from pydantic import BaseModel
from typing import Optional, List

# --- User Schemas ---

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    class Config:
        schema_extra = {
            "example": {
                "username": "Alice Smith",
                "email": "alice@example.com"
            }
        }

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserWithNotes(User):
    notes: List['Note'] = []

# --- Note Schemas ---

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    user_id: int

    class Config:
        schema_extra = {
            "example": {
                "title": "Team Meeting",
                "content": "Discussed project milestones",
                "user_id": 1
            }
        }

class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]

class Note(NoteBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class NoteWithLabels(Note):
    labels: List[str] = []

# --- Label Schemas ---

class LabelBase(BaseModel):
    name: str

class LabelCreate(LabelBase):
    user_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Work",
                "user_id": 1
            }
        }

class LabelUpdate(BaseModel):
    name: Optional[str]

class Label(LabelBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Needed for forward references
UserWithNotes.update_forward_refs()
NoteWithLabels.update_forward_refs()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from DB.database import SessionLocal
import model, schema
from typing import List

router = APIRouter()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- USERS ---

@router.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = model.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[schema.User])
def get_users(db: Session = Depends(get_db)):
    return db.query(model.User).all()

@router.put("/users/{user_id}", response_model=schema.User)
def update_user(user_id: int, updated_user: schema.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if updated_user.username is not None:
        user.username = updated_user.username
    if updated_user.email is not None:
        user.email = updated_user.email
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}

# --- NOTES ---

@router.post("/notes/", response_model=schema.Note)
def create_note(note: schema.NoteCreate, db: Session = Depends(get_db)):
    db_note = model.Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/notes/", response_model=List[schema.Note])
def get_notes(db: Session = Depends(get_db)):
    return db.query(model.Note).all()

@router.put("/notes/{note_id}", response_model=schema.Note)
def update_note(note_id: int, updated_note: schema.NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(model.Note).filter(model.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if updated_note.title is not None:
        note.title = updated_note.title
    if updated_note.content is not None:
        note.content = updated_note.content
    db.commit()
    db.refresh(note)
    return note

@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(model.Note).filter(model.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"msg": "Note deleted"}

# --- LABELS ---

@router.post("/labels/", response_model=schema.Label)
def create_label(label: schema.LabelCreate, db: Session = Depends(get_db)):
    db_label = model.Label(**label.dict())
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

@router.get("/labels/", response_model=List[schema.Label])
def get_labels(db: Session = Depends(get_db)):
    return db.query(model.Label).all()

@router.put("/labels/{label_id}", response_model=schema.Label)
def update_label(label_id: int, updated_label: schema.LabelUpdate, db: Session = Depends(get_db)):
    label = db.query(model.Label).filter(model.Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    if updated_label.name is not None:
        label.name = updated_label.name
    db.commit()
    db.refresh(label)
    return label

@router.delete("/labels/{label_id}")
def delete_label(label_id: int, db: Session = Depends(get_db)):
    label = db.query(model.Label).filter(model.Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    db.delete(label)
    db.commit()
    return {"msg": "Label deleted"}

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
import models
from database import SessionLocal, engine
from schemas import BookCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books", response_model=list[schemas.Book])
def get_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_books(db)


@app.post("/books", response_model=schemas.Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    updated_book = crud.update_book(db, book_id, book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted_book = crud.delete_book(db, book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book

from typing import List, Optional
from sqlalchemy.orm import Session
from models import Book
from schemas import BookCreate, BookUpdate


def get_books(db: Session, skip: int = 0, limit: int = 10) -> List[Book]:
    return db.query(Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: BookUpdate) -> Optional[Book]:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        for key, value in book.dict().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> Optional[Book]:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book

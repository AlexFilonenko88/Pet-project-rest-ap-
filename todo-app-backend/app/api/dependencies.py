from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import db
from app.services.task import TaskService


def get_task_service(db: Session = Dependes(get_db)):
    """ Функция для инъекции зависимости TaskService """
    return TaskService(db)

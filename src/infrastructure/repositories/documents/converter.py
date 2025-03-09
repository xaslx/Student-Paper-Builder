from datetime import datetime
from src.domain.document.entity import Document
from src.domain.document.value_object import TitlePage, Section, Application
import pytz
from src.const import MOSCOW_TZ


def document_to_mongo(document: Document) -> dict:
    return {
        'uuid': document.uuid,
        'user_uuid': document.user_uuid,
        'name': document.name,
        'abbreviations': document.abbreviations,
        'title_page': title_page_to_mongo(title_page=document.title_page),
        'introduction': document.introduction,
        'main_sections': [section_to_mongo(section=sec) for sec in document.main_sections],
        'conclusion': document.conclusion,
        'references': document.references,
        'appendices': [application_to_mongo(app) for app in document.appendices],
        'created_at': document.created_at,
        'updated_at': document.updated_at
    }


def document_from_mongo(data: dict) -> Document:
    created_at = data.get('created_at')
    updated_at = data.get('updated_at')
    
    if created_at and isinstance(created_at, datetime):
        created_at = created_at.replace(tzinfo=pytz.utc).astimezone(MOSCOW_TZ)
    if updated_at and isinstance(updated_at, datetime):
        updated_at = updated_at.replace(tzinfo=pytz.utc).astimezone(MOSCOW_TZ)

    return Document(
        uuid=data.get('uuid'),
        name=data.get('name'),
        user_uuid=data.get('user_uuid'),
        title_page=TitlePage(**data.get('title_page', {})),
        introduction=data.get('introduction'),
        abbreviations=data.get('abbreviations'),
        main_sections=[section_from_mongo(sec) for sec in data.get('main_sections', [])],
        conclusion=data.get('conclusion'),
        references=data.get('references'),
        appendices=[application_from_mongo(app) for app in data.get('appendices', [])],
        created_at=created_at,
        updated_at=updated_at
    )


def section_to_mongo(section: Section) -> dict:
    return {
        'title': section.title,
        'content': section.content,
        'subsection': section.subsection
    }


def section_from_mongo(data: dict) -> Section:
    return Section(
        title=data.get('title'),
        content=data.get('content'),
        subsection=data.get('subsection')
    )


def title_page_to_mongo(title_page: TitlePage) -> dict:
    return {
        'type_of_work': title_page.type_of_work,
        'discipline': title_page.discipline,
        'subject': title_page.subject,
        'educational_institution': title_page.educational_institution,
        'year': title_page.year,
        'student_fullname': title_page.student_fullname,
        'teacher_fullname': title_page.teacher_fullname,
        'faculty': title_page.faculty,
        'city': title_page.city,
        'teaching_position': title_page.teaching_position,
    }


def title_page_from_mongo(data: dict) -> TitlePage:
    return TitlePage(
        type_of_work=data.get('type_of_work'),
        discipline=data.get('discipline'),
        subject=data.get('subject'),
        educational_institution=data.get('educational_institution'),
        year=data.get('year', datetime.now().year),
        student_fullname=data.get('student_fullname'),
        teacher_fullname=data.get('teacher_fullname'),
        faculty=data.get('faculty'),
        city=data.get('city'),
        teaching_position=data.get('teaching_position')
    )


def application_to_mongo(application: Application) -> dict:
    return {
        'path': application.path,
        'description': application.description
    }


def application_from_mongo(data: dict) -> Application:
    return Application(
        path=data.get('path'),
        description=data.get('description')
    )
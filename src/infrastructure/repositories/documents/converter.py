from datetime import datetime
from src.domain.document.entity import Document
from src.domain.document.value_object import TitlePage
from src.domain.document.value_object import Section


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
        'appendices': document.appendices,
        'created_at': document.created_at,
        'updated_at': document.updated_at
    }


def document_from_mongo(data: dict) -> Document:
    
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
        appendices=data.get('appendices', []),
        created_at=data.get('created_at'),
        updated_at=data.get('updated_at')
    )


def section_to_mongo(section: Section) -> dict:

    return {
        'title': section.title,
        'content': section.content,
        'subsections': [section_to_mongo(sub) for sub in section.subsections]
    }


def section_from_mongo(data: dict) -> Section:

    subsections = [section_from_mongo(sub) for sub in data.get('subsections', [])] if data.get('subsections') else []
    
    return Section(
        title=data.get('title'),
        content=data.get('content'),
        subsections=subsections
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
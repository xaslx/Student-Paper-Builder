document.addEventListener('DOMContentLoaded', function () {
    const documentUuid = document.getElementById('documentUuid').value;

    async function updateDocument(documentUuid, section, data) {
        try {
            const response = await fetch(`/documents/${documentUuid}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ [section]: data }),
            });
    
            if (!response.ok) {
                throw new Error('Ошибка при сохранении');
            }
    
            const result = await response.json();
                        
            notie.alert({
                type: 'success',
                text: 'Документ успешно сохранен!',
                position: 'top-right',
                time: 3
            });

        } catch (error) {
            console.error('Ошибка:', error);
            
            notie.alert({
                type: 'error',
                text: 'Ошибка при сохранении документа.',
                position: 'top-right',
                time: 3
            });
        }
    }
    

    const titlePageForm = document.getElementById('titlePageForm');
    if (titlePageForm) {
        titlePageForm.addEventListener('submit', function (event) {
            event.preventDefault();
            updateDocument(documentUuid, 'title_page', {
                type_of_work: document.getElementById('type_of_work').value,
                discipline: document.getElementById('discipline').value,
                subject: document.getElementById('subject').value,
                educational_institution: document.getElementById('educational_institution').value,
                year: document.getElementById('year').value,
                student_fullname: document.getElementById('student_fullname').value,
                teacher_fullname: document.getElementById('teacher_fullname').value,
                faculty: document.getElementById('faculty').value,
                city: document.getElementById('city').value,
                teaching_position: document.getElementById('teaching_position').value,
            });
        });
    }

    const introductionForm = document.getElementById('introductionForm');
    if (introductionForm) {
        introductionForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const introductionText = document.getElementById('introduction_text').value;

            updateDocument(documentUuid, 'introduction', introductionText);
        });
    }


    const conclusionForm = document.getElementById('conclusionForm');
    if (conclusionForm) {
        conclusionForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const conclusionText = document.getElementById('conclusion_text').value;
            
            updateDocument(documentUuid, 'conclusion', conclusionText);
        });
    }
});
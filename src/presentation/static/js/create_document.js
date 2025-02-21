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
                time: 2
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

    
    function checkRequiredSections() {
        const requiredSections = [
            'Титульный лист',
            'Введение',
            'Основная часть',
            'Заключение',
            'Список используемых источников'
        ];

        return requiredSections.every(sectionTitle => {
            const sectionItem = Array.from(document.querySelectorAll('.section-item')).find(item => {
                return item.querySelector('summary').textContent.trim() === sectionTitle;
            });
            
            if (!sectionItem) return false;
            const statusElement = sectionItem.querySelector('.status-wrapper span');
            return statusElement.classList.contains('status-filled');
        });
    }

    function handleSaveButtonClick(e) {
        if (!checkRequiredSections()) {
            e.preventDefault();
            notie.alert({
                type: 'error',
                text: `Нельзя скачать документ, пока не заполнены все обязательные разделы:
            Титульный лист,
            Введение,
            Основная часть,
            Заключение,
            Список используемых источников`,
                position: 'top-right',
                time: 6
            });
        }
    }


    const saveDocxBtn = document.querySelector('.save-docx-btn');
    const savePdfBtn = document.querySelector('.save-pdf-btn');
    
    if (saveDocxBtn) {
        saveDocxBtn.addEventListener('click', handleSaveButtonClick);
    }
    
    if (savePdfBtn) {
        savePdfBtn.addEventListener('click', handleSaveButtonClick);
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

    const abbreviationsForm = document.getElementById('abbreviationsForm');
    if (abbreviationsForm) {
        abbreviationsForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const abbreviationsText = document.getElementById('abbreviations_text').value;

            updateDocument(documentUuid, 'abbreviations', abbreviationsText);
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

    const abbreviationsList = document.getElementById('abbreviations-list');
    const addAbbrBtn = document.getElementById('add-abbreviation-btn');



    function deleteAbbreviation(event) {
        if (!event.target.classList.contains('delete-abbreviation-btn')) return;

        const li = event.target.closest('li');
        if (!li) return;

        const abbrText = li.querySelector('.abbr-text').textContent;


        Swal.fire({
            title: 'Удалить сокращение?',
            text: `Вы уверены, что хотите удалить "${abbrText}"?`,
            icon: 'warning',
            showCancelButton: true,
            cancelButtonText: 'Отмена',
            confirmButtonText: 'Удалить',
        }).then((result) => {
            if (result.isConfirmed) {
                li.remove();
                updateAbbreviationsOnServer();
            }
        });
    }

    function addAbbreviation() {
        Swal.fire({
            title: 'Новое сокращение',
            input: 'text',
            inputPlaceholder: 'Пример: ПО - Программное обеспечение',
            showCancelButton: true,
            confirmButtonText: 'Сохранить',
            cancelButtonText: 'Отмена',
            customClass: {
                input: 'swal-input-custom'
            }
        }).then((result) => {
            if (result.isConfirmed && result.value.trim() !== '') {
                const newAbbr = result.value.trim();
    
                const li = document.createElement('li');
                li.innerHTML = `<span class="abbr-text">${newAbbr}</span>
                                <button type="button" class="delete-abbreviation-btn">&times;</button>`;
                abbreviationsList.appendChild(li);
    
                updateAbbreviationsOnServer();
            }
        });
    }
    
 
    const style = document.createElement('style');
    style.innerHTML = `
        .swal-input-custom {
            height: 35px !important;
            width: 87% !important;
            font-size: 16px !important;
        }
    `;
    document.head.appendChild(style);
    

    function updateAbbreviationsOnServer() {
        const abbreviations = Array.from(abbreviationsList.querySelectorAll('.abbr-text')).map(span => span.textContent);
        updateDocument(documentUuid, 'abbreviations', abbreviations.length > 0 ? abbreviations : []);
    }

    abbreviationsList.addEventListener('click', deleteAbbreviation);
    addAbbrBtn.addEventListener('click', addAbbreviation);



    document.querySelectorAll('.delete-abbreviation-btn').forEach(button => {
        button.addEventListener('click', function () {
            const li = this.closest('li');
            if (!li) return;

            const referenceText = li.querySelector('.reference-text').textContent.trim();

            Swal.fire({
                title: 'Удалить источник?',
                text: `Вы уверены, что хотите удалить "${referenceText}"?`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Удалить',
                cancelButtonText: 'Отмена',
            }).then((result) => {
                if (result.isConfirmed) {
                    li.remove();
                    updateReferencesOnServer();
                }
            });
        });
    });

    function updateReferencesOnServer() {
        const references = Array.from(document.querySelectorAll('.reference-text')).map(span => span.textContent);
        updateDocument(documentUuid, 'references', references);
    }

    
    const modal = document.getElementById('custom-modal');
    const openModalBtn = document.getElementById('add-internet-resource');
    const closeModalBtn = document.querySelector('.close');
    const resourceForm = document.getElementById('resource-form');


    if (openModalBtn) {
        openModalBtn.addEventListener('click', function () {
            modal.style.display = 'block';
        });
    }


    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function () {
            modal.style.display = 'none';
        });
    }


    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });


    if (resourceForm) {
        resourceForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const title = document.getElementById('title').value;
            const siteName = document.getElementById('site-name').value;
            const link = document.getElementById('link').value;
            const accessDate = document.getElementById('access-date').value;
    
            const formattedDate = new Date(accessDate).toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });
    

            const referenceText = `${title} // ${siteName} URL: ${link} (дата обращения: ${formattedDate}).`;

            const referenceList = document.querySelector('.reference-list');
            const newLi = document.createElement('li');
            newLi.innerHTML = `<span class="reference-text">${referenceText}</span>
                               <button type="button" class="delete-abbreviation-btn">&times;</button>`;
            referenceList.appendChild(newLi);
    
            resourceForm.reset();
    
            modal.style.display = 'none';
    
            updateReferencesOnServer();
        });
    }

});



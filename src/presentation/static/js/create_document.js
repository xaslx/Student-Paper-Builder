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
    
            localStorage.setItem('documentUpdated', 'true');
            localStorage.setItem('openSection', section);
    
            window.location.reload();
    
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

    if (localStorage.getItem('documentUpdated') === 'true') {
        notie.alert({
            type: 'success',
            text: 'Документ успешно сохранен!',
            position: 'top-right',
            time: 2
        });

        localStorage.removeItem('documentUpdated');
    }

    const openSection = localStorage.getItem('openSection');
    if (openSection) {
        const sectionElement = document.querySelector(`[data-section="${openSection}"]`);
        if (sectionElement) {
            sectionElement.open = true;
        }
        localStorage.removeItem('openSection');
    }
    

    function handleSaveButtonClick(e) {
        return true;
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



    document.querySelectorAll('.delete-reference-btn').forEach(button => {
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

    const bookModal = document.getElementById('book-modal');
    const openBookModalBtn = document.getElementById('add-book');
    const closeBookModalBtn = bookModal.querySelector('.close');
    const bookForm = document.getElementById('book-form');

    if (openBookModalBtn) {
        openBookModalBtn.addEventListener('click', function () {
            bookModal.style.display = 'block';
        });
    }

    if (closeBookModalBtn) {
        closeBookModalBtn.addEventListener('click', function () {
            bookModal.style.display = 'none';
        });
    }

    window.addEventListener('click', function (event) {
        if (event.target === bookModal) {
            bookModal.style.display = 'none';
        }
    });


    if (bookForm) {
        bookForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const authors = document.getElementById('authors').value;
            const bookTitle = document.getElementById('book-title').value;
            const edition = document.getElementById('edition').value;
            const city = document.getElementById('publishing-city').value;
            const publisher = document.getElementById('publisher').value;
            const year = document.getElementById('publishing-year').value;
            const pages = document.getElementById('pages').value;

            const referenceText = `${authors} ${bookTitle}. - ${edition} изд. - ${city}: ${publisher}, ${year}. - ${pages} с.`;

            const referenceList = document.querySelector('.reference-list');
            const newLi = document.createElement('li');
            newLi.innerHTML = `<span class="reference-text">${referenceText}</span>
                               <button type="button" class="delete-reference-btn">&times;</button>`;
            referenceList.appendChild(newLi);

            bookForm.reset();
            bookModal.style.display = 'none';

            updateReferencesOnServer();
        });
    

    const addChapterBtn = document.getElementById('add-chapter-btn');
    const chapterModal = document.getElementById('chapter-modal');
    const chapterForm = document.getElementById('chapter-form');
    const chaptersList = document.getElementById('chapters-list');

    if (addChapterBtn) {
        addChapterBtn.addEventListener('click', function () {
            chapterModal.style.display = 'block';
            chapterForm.reset();
            document.getElementById('modal-title').textContent = 'Добавить главу';
            chapterForm.dataset.mode = 'add';
        });
    }

    const closeModalBtn = chapterModal.querySelector('.close');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function () {
            chapterModal.style.display = 'none';
        });
    }

    if (chapterForm) {
        chapterForm.addEventListener('submit', function (event) {
            event.preventDefault();
        
            const chapterTitle = document.getElementById('chapter-title').value;
            const subchapterTitle = document.getElementById('subchapter-title').value;
            const chapterContent = document.getElementById('chapter-content').value;
        
            const chapterData = {
                title: chapterTitle,
                content: chapterContent,
                subsection: subchapterTitle || null
            };
        
            if (chapterForm.dataset.mode === 'add') {
                addChapterToDOM(chapterData);
            } else if (chapterForm.dataset.mode === 'edit') {
                const chapterIndex = chapterForm.dataset.chapterIndex;
                updateChapterInDOM(chapterIndex, chapterData);
            }
        
            updateDocument(documentUuid, 'main_sections', getChaptersData());
            chapterModal.style.display = 'none';
    });
    }

    function addChapterToDOM(chapterData) {
        const chapterItem = document.createElement('div');
        chapterItem.classList.add('chapter-item');
        chapterItem.dataset.index = Date.now();
    
        chapterItem.innerHTML = `
            <h3>${chapterData.title}</h3>
            ${chapterData.subsection ? `<h4>${chapterData.subsection}</h4>` : ''}
            <p>${chapterData.content}</p>
            <div class="chapter-actions">
                <button style="font-size: 20px; color: black;" class="edit-chapter-btn" data-index="${chapterItem.dataset.index}">
                    &#9998;
                </button>
                <button style="font-size: 20px; color: red;" class="delete-chapter-btn" data-index="${chapterItem.dataset.index}">
                    &times;
                </button>
            </div>
        `;
    
        chaptersList.appendChild(chapterItem);
    }
    

    function updateChapterInDOM(chapterIndex, chapterData) {
        const chapterItem = chaptersList.querySelector(`.chapter-item[data-index="${chapterIndex}"]`);
        if (chapterItem) {
            chapterItem.querySelector('h3').textContent = chapterData.title;
            chapterItem.querySelector('p').textContent = chapterData.content;

            const subchapterTitleElement = chapterItem.querySelector('h4');
            if (chapterData.subsection) {
                if (subchapterTitleElement) {
                    subchapterTitleElement.textContent = chapterData.subsection;
                } else {
                    const h4 = document.createElement('h4');
                    h4.textContent = chapterData.subsection;
                    chapterItem.insertBefore(h4, chapterItem.querySelector('p'));
                }
            } else if (subchapterTitleElement) {
                subchapterTitleElement.remove();
            }
        }
    }

    function getChaptersData() {
        const chapters = [];
        chaptersList.querySelectorAll('.chapter-item').forEach(chapterItem => {
            const chapterData = {
                title: chapterItem.querySelector('h3').textContent,
                content: chapterItem.querySelector('p').textContent,
                subsection: chapterItem.querySelector('h4')?.textContent || null
            };

            chapters.push(chapterData);
        });

        return chapters;
    }

    chaptersList.addEventListener('click', function (event) {
        const editButton = event.target.closest('.edit-chapter-btn'); 
        if (editButton) {
            const chapterIndex = editButton.dataset.index;
            const chapterItem = chaptersList.querySelector(`.chapter-item[data-index="${chapterIndex}"]`);

            if (chapterItem) {
                const chapterTitle = chapterItem.querySelector('h3').textContent;
                const subchapterTitle = chapterItem.querySelector('h4')?.textContent || '';
                const chapterContent = chapterItem.querySelector('p').textContent;

                document.getElementById('chapter-title').value = chapterTitle;
                document.getElementById('subchapter-title').value = subchapterTitle;
                document.getElementById('chapter-content').value = chapterContent;

                document.getElementById('modal-title').textContent = 'Редактировать главу';
                chapterForm.dataset.mode = 'edit';
                chapterForm.dataset.chapterIndex = chapterIndex;
                chapterModal.style.display = 'block';
            }
        }
    });

    chaptersList.addEventListener('click', function (event) {
        const deleteButton = event.target.closest('.delete-chapter-btn'); 
        if (deleteButton) {
            const chapterIndex = deleteButton.dataset.index;
            const chapterItem = chaptersList.querySelector(`.chapter-item[data-index="${chapterIndex}"]`);
            
            if (chapterItem) {
                Swal.fire({
                    title: 'Удалить главу?',
                    text: `Вы уверены, что хотите удалить главу "${chapterItem.querySelector('h3').textContent}"?`,
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Удалить',
                    cancelButtonText: 'Отмена',
                }).then((result) => {
                    if (result.isConfirmed) {
                        chapterItem.remove();
                        updateDocument(documentUuid, 'main_sections', getChaptersData());
                    }
                });
            }
        }
        })
    
    const saveDocxBtn = document.querySelector('.save-docx-btn');
    const savePdfBtn = document.querySelector('.save-pdf-btn');
    const documentUuid = document.getElementById('documentUuid').value;

    saveDocxBtn.addEventListener('click', function() {
        disableButtonsForSeconds(2);
        showDownloadMessage();
        saveDocument('docx');
    });
    
    savePdfBtn.addEventListener('click', function() {
        disableButtonsForSeconds(2);
        showDownloadMessage();
        saveDocument('pdf');
    });

    function disableButtonsForSeconds(seconds) {
        saveDocxBtn.disabled = true;
        savePdfBtn.disabled = true;

        setTimeout(() => {
            saveDocxBtn.disabled = false;
            savePdfBtn.disabled = false;
        }, seconds * 1000);
    }

    function showDownloadMessage() {
        notie.alert({
            type: 'info',
            text: 'Загрузка скоро начнется...',
            position: 'top',
            time: 3,
        });
    }

    function saveDocument(format) {
        fetch(`/documents/${documentUuid}/download?format=${format}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error('Ошибка при сохранении документа');
            }
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${documentUuid}.${format}`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Ошибка:', error);
            notie.alert({ type: 'error', text: 'Ошибка при сохранении документа', position: 'top', time: 3 });
        });
    }
    }

    function deleteAppendix(event) {
        const deleteBtn = event.target.closest('.delete-appendix-btn');
        if (!deleteBtn) return;
    
        const appendixItem = deleteBtn.closest('.appendix-item');
        if (!appendixItem) return;
    
        Swal.fire({
            title: 'Удалить приложение?',
            text: 'Вы уверены, что хотите удалить это приложение?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Удалить',
            cancelButtonText: 'Отмена',
        }).then((result) => {
            if (result.isConfirmed) {
                appendixItem.remove();
                updateAppendicesNumbers();
                updateAppendicesOnServer();
            }
        });
    }

    function updateAppendicesNumbers() {
        const appendixItems = document.querySelectorAll('.appendix-item');
        appendixItems.forEach((item, index) => {
            const pElement = item.querySelector('p');
            const description = pElement.textContent.split('. ')[1];
        });
    }
    
    function updateAppendicesOnServer() {
        const appendices = Array.from(document.querySelectorAll('.appendix-item')).map(item => {
            const imgSrc = item.querySelector('img').src;
            const fileName = imgSrc.split('/').pop();
            console.log('Имя файла:', fileName);
            
            return {
                path: `src/presentation/static/images/${fileName}`,
                name: fileName,
                description: item.querySelector('p').textContent 
            };            
        });
    
        updateDocument(documentUuid, 'appendices', appendices);
    }
    
    

    document.querySelector('.appendices-container').addEventListener('click', deleteAppendix);

    const imageModal = document.getElementById('image-modal');
    const addImageBtn = document.getElementById('add-image-btn');
    const closeImageModalBtn = imageModal.querySelector('.close');
    const imageForm = document.getElementById('image-form');

    if (addImageBtn) {
        addImageBtn.addEventListener('click', function () {
            imageModal.style.display = 'block';
        });
    }

    if (closeImageModalBtn) {
        closeImageModalBtn.addEventListener('click', function () {
            imageModal.style.display = 'none';
        });
    }

    window.addEventListener('click', function (event) {
        if (event.target === imageModal) {
            imageModal.style.display = 'none';
        }
    });

    if (imageForm) {
        imageForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const description = document.getElementById('image-description').value;
            const fileInput = document.getElementById('image-file');
            const file = fileInput.files[0];

            if (file) {
                const formData = new FormData();
                formData.append('image', file);
                formData.append('description', description);

                fetch(`/documents/${documentUuid}`, {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        localStorage.setItem('openSection', 'appendices');

                        notie.alert({
                            type: 'success',
                            text: 'Документ успешно обновлен',
                            position: 'top-right',
                            time: 3
                        });

                        imageModal.style.display = 'none';

                        imageForm.reset();

                        setTimeout(() => {
                            window.location.reload();
                        }, 1000);
                    } else {
                        notie.alert({
                            type: 'error',
                            text: 'Ошибка при загрузке файла',
                            position: 'top-right',
                            time: 3
                        });
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    notie.alert({
                        type: 'error',
                        text: 'Ошибка при загрузке файла',
                        position: 'top-right',
                        time: 3
                    });
                });
            }
        });
    }
        
});

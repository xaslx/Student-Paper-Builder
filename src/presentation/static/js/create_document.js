document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("titlePageButton").addEventListener("click", async () => {
        await Swal.fire({
            title: "Титульный лист",
            html:
                `<input id="typeOfWork" class="swal2-input" placeholder="Тип работы: пример - Курсовая работа">` +
                `<input id="discipline" class="swal2-input" placeholder="Дисциплина: пример - Программная инженерия">` +
                `<input id="subject" class="swal2-input" placeholder="Тема работы">` + 
                `<input id="educational_institution" class="swal2-input" placeholder="Наименование учебного заведения">` +
                `<input id="student_fullname" class="swal2-input" placeholder="ФИО студента: пример - Иванова А.С">` +
                `<input id="teacher_fullname" class="swal2-input" placeholder="ФИО преподавателя: пример - Иванова А.С">` +
                `<input id="faculty" class="swal2-input" placeholder="Кафедра: пример - Юриспруденция">` +
                `<input id="city" class="swal2-input" placeholder="Город: пример - Москва">` +
                `<input id="teaching_position" class="swal2-input" placeholder="Должность преподавателя: пример - Д-р. техн. наук">`,
            focusConfirm: false,
            showCancelButton: true,
            confirmButtonText: "Сохранить",
            cancelButtonText: "Отмена",
            customClass: {
                popup: 'custom-modal',
            },
            preConfirm: () => {
                return {
                    typeOfWork: document.getElementById("typeOfWork").value,
                    discipline: document.getElementById("discipline").value,
                    subject: document.getElementById("subject").value,
                    educational_institution: document.getElementById("educational_institution").value,
                    student_fullname: document.getElementById("student_fullname").value,
                    teacher_fullname: document.getElementById("teacher_fullname").value,
                    faculty: document.getElementById("faculty").value,
                    city: document.getElementById("city").value,
                    teaching_position: document.getElementById("teaching_position").value,
                };
            },
        });
    });

    document.getElementById("introductionButton").addEventListener("click", async () => {
        Swal.fire({
            title: "Введение",
            html: `<textarea class="swal2-textarea" placeholder="Введите текст введения"></textarea>`,
            customClass: {
                popup: 'custom-intro-modal',
            },
            focusConfirm: false,
            showCancelButton: true,
            confirmButtonText: "Сохранить",
            cancelButtonText: "Отмена",
            preConfirm: () => {
                const introductionText = document.querySelector('.swal2-textarea').value.trim();
                if (!introductionText) {
                    Swal.showValidationMessage("Поле обязательно для заполнения");
                }
                return { introductionText };
            },
        }).then((result) => {
            if (result.isConfirmed) {

            }
        });
    });

    document.getElementById("conclusionButton").addEventListener("click", async () => {
        Swal.fire({
            title: "Заключение",
            html: `<textarea class="swal2-textarea" placeholder="Введите текст заключения"></textarea>`,
            customClass: {
                popup: 'custom-conclusion-modal',
            },
            focusConfirm: false,
            showCancelButton: true,
            confirmButtonText: "Сохранить",
            cancelButtonText: "Отмена",
            preConfirm: () => {
                const conclusionText = document.querySelector('.swal2-textarea').value.trim();
                if (!conclusionText) {
                    Swal.showValidationMessage("Поле обязательно для заполнения");
                }
                return { conclusionText };
            },
        }).then((result) => {
            if (result.isConfirmed) {

            }
        });
    });

    document.getElementById("abbreviationsButton").addEventListener("click", async () => {
        Swal.fire({
            title: "Список сокращений",
            html: `<textarea class="swal2-textarea" placeholder="Введите список сокращений"></textarea>`,
            customClass: {
                popup: 'custom-conclusion-modal',
            },
            focusConfirm: false,
            showCancelButton: true,
            confirmButtonText: "Сохранить",
            cancelButtonText: "Отмена",
            preConfirm: () => {
                const conclusionText = document.querySelector('.swal2-textarea').value.trim();
                if (!conclusionText) {
                    Swal.showValidationMessage("Поле обязательно для заполнения");
                }
                return { conclusionText };
            },
        }).then((result) => {
            if (result.isConfirmed) {

            }
        });
    });
});

document.getElementById("newDocumentButton").addEventListener("click", async () => {
    const isAuthenticated = document.getElementById("isAuthenticated").value === "true";
    if (!isAuthenticated) {
        Swal.fire({
            title: "Ошибка",
            text: "Вы не авторизованы!",
            icon: "error",
            confirmButtonText: "ОК",
            showCloseButton: true,
            allowOutsideClick: true,
        }).then((result) => {
            if (result.isConfirmed || result.dismiss === Swal.DismissReason.close || result.dismiss === Swal.DismissReason.backdrop) {
                window.location.href = "/login";
            }
        });
        return;
    }


    const { value: documentName } = await Swal.fire({
        title: "Создание нового документа",
        input: "text",
        inputLabel: "Введите название документа",
        inputPlaceholder: "Пример: Курсовая работа по программированию",
        showCancelButton: true,
        confirmButtonText: "Создать",
        cancelButtonText: "Отмена",
        inputValidator: (value) => {
            if (!value) {
                return "Название документа обязательно!";
            }
            if (value.length < 5 || value.length > 50) {
                return "Название должно быть от 5 до 50 символов!";
            }
        },
        customClass: {
            input: 'custom-input-class',
        },
    });


    if (documentName) {
        try {
            const documentData = {
                title_page: {
                    type_of_work: null,
                    discipline: null,
                    subject: null,
                    group_number: null,
                    educational_institution: null,
                    year: null,
                    student_fullname: null,
                    teacher_fullname: null,
                    faculty: null,
                    city: null,
                    teaching_position: null,
                },
                name: documentName,
                introduction: null,
                main_sections: [],
                conclusion: null,
                abbreviations: [],
                references: [],
                appendices: [],
            };

            const response = await fetch('/documents', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(documentData),
            });

            if (response.ok) {
                const documentUuid = await response.json();
                Swal.fire({
                    title: "Документ создан",
                    text: "Новый документ был успешно создан",
                    icon: "success",
                    timer: 2000,
                    showConfirmButton: false,
                }).then(() => {
                    window.location.href = `/documents/${documentUuid}`;
                });
            } else {
                const data = await response.json();
                Swal.fire({
                    title: "Ошибка",
                    text: data.detail || "Не удалось создать новый документ",
                    icon: "error",
                    confirmButtonText: "ОК",
                });
            }
        } catch (error) {
            console.error("Ошибка при создании документа:", error);
            Swal.fire({
                title: "Ошибка",
                text: "Произошла ошибка при создании документа",
                icon: "error",
                confirmButtonText: "ОК",
            });
        }
    }
});

function toggleMenu(menuId, event) {
    event.preventDefault();
    event.stopPropagation();

    const menu = document.getElementById(menuId);
    const isOpen = menu.classList.contains('open');

    document.querySelectorAll('.document-menu').forEach(m => m.classList.remove('open'));

    if (!isOpen) {
        menu.classList.add('open');
    }
}


document.addEventListener('click', function(event) {
    const isMenu = event.target.closest('.document-menu');
    const isEllipsis = event.target.closest('.ellipsis');

    if (!isMenu && !isEllipsis) {
        document.querySelectorAll('.document-menu').forEach(menu => menu.classList.remove('open'));
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const newDocumentButton = document.getElementById("newDocumentButton");
    if (newDocumentButton) {
        newDocumentButton.addEventListener("click", createNewDocument);
    } else {
        console.error("Кнопка 'Новый документ' не найдена в DOM");
    }
});


function toggleProfileMenu(event) {
    event.stopPropagation();
    const profileMenu = document.getElementById("profileMenu");
    profileMenu.classList.toggle("active");
}


document.addEventListener('click', function(event) {
    const profileMenu = document.getElementById("profileMenu");
    const profileContainer = document.querySelector('.profile-container');

    if (!profileMenu.contains(event.target) && !profileContainer.contains(event.target)) {
        profileMenu.classList.remove("active");
    }
});

document.querySelector('.profile-container').addEventListener('click', toggleProfileMenu);

async function logout() {
    try {
        const loginUrl = document.getElementById("loginUrl").value;
        const response = await fetch('/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            Swal.fire({
                title: "Выход выполнен успешно",
                text: "Вы будете перенаправлены на страницу входа",
                icon: "success",
                timer: 2000,
                showConfirmButton: false,
            }).then(() => {
                window.location.href = loginUrl;
            });
        } else {
            Swal.fire({
                title: "Ошибка",
                text: "Ошибка при выходе из системы",
                icon: "error",
                confirmButtonText: "ОК",
            });
        }
    } catch (error) {
        console.error("Ошибка при выходе:", error);
        Swal.fire({
            title: "Ошибка",
            text: "Произошла ошибка при выходе из системы",
            icon: "error",
            confirmButtonText: "ОК",
        });
    }
}


async function login(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            Swal.fire({
                title: "Успешный вход",
                text: "Вы будете перенаправлены на главную страницу",
                icon: "success",
                timer: 2000,
                showConfirmButton: false,
            }).then(() => {
                window.location.href = "/";
            });
        } else {
            const data = await response.json();
            Swal.fire({
                title: "Ошибка",
                text: data.detail || "Неверный логин или пароль",
                icon: "error",
                confirmButtonText: "ОК",
            });
        }
    } catch (error) {
        console.error("Ошибка при входе:", error);
        Swal.fire({
            title: "Ошибка",
            text: "Произошла ошибка при входе в систему",
            icon: "error",
            confirmButtonText: "ОК",
        });
    }
}


async function deleteAllDocuments() {
    const isAuthenticated = document.getElementById("isAuthenticated").value === "true";
    if (!isAuthenticated) {
        Swal.fire({
            title: "Ошибка",
            text: "Вы не авторизованы!",
            icon: "error",
            confirmButtonText: "ОК",
        });
        return;
    }

    const confirmation = await Swal.fire({
        title: "Удалить все документы?",
        text: "Это действие нельзя отменить!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Да, удалить!",
        cancelButtonText: "Отмена"
    });

    if (!confirmation.isConfirmed) {
        return;
    }

    try {
        const response = await fetch('/documents', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        if (response.ok) {
            Swal.fire({
                title: "Успешно",
                text: "Все документы удалены",
                icon: "success",
                timer: 2000,
                showConfirmButton: false
            }).then(() => {
                location.reload();
            });
        } else {
            Swal.fire({
                title: "Ошибка",
                text: "Документы не найдены",
                icon: "error",
                confirmButtonText: "ОК"
            });
        }
    } catch (error) {
        console.error("Ошибка при удалении документов:", error);
        Swal.fire({
            title: "Ошибка",
            text: "Произошла ошибка при удалении документов",
            icon: "error",
            confirmButtonText: "ОК"
        });
    }
}



async function register(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });

        if (response.ok) {
            Swal.fire({
                title: "Регистрация успешна",
                text: "Вы будете перенаправлены на страницу входа",
                icon: "success",
                timer: 2500,
                showConfirmButton: false,
            }).then(() => {
                window.location.href = "/login";
            });
        } else {
            const data = await response.json();
            Swal.fire({
                title: "Ошибка регистрации",
                text: data.detail || "Ошибка при регистрации",
                icon: "error",
                confirmButtonText: "ОК",
            });
        }
    } catch (error) {
        console.error("Ошибка при регистрации:", error);
        Swal.fire({
            title: "Ошибка",
            text: "Произошла ошибка при регистрации",
            icon: "error",
            confirmButtonText: "ОК",
        });
    }
}


document.getElementById("register-form").addEventListener("submit", register);


function aboutService() {
    const aboutUrl = document.getElementById("aboutUrl").value;
    window.location.href = aboutUrl;
}

function togglePasswordVisibility(inputId) {
    const passwordInput = document.getElementById(inputId);
    passwordInput.type = passwordInput.type === "password" ? "text" : "password";
}


async function resetPassword(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;

    try {
        const response = await fetch('/reset-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email }),
        });

        if (response.ok) {
            Swal.fire({
                title: "Успешно!",
                text: "Письмо для сброса пароля отправлено на ваш email.",
                icon: "success",
                confirmButtonText: "ОК",
            }).then(() => {
                window.location.href = "/login";
            });
        } else {
            const errorData = await response.json();
            Swal.fire({
                title: "Ошибка",
                text: errorData.detail || "Произошла ошибка при отправке запроса.",
                icon: "error",
                confirmButtonText: "ОК",
            });
        }
    } catch (error) {
        console.error('Ошибка:', error);
        Swal.fire({
            title: "Ошибка",
            text: "Произошла ошибка при отправке запроса.",
            icon: "error",
            confirmButtonText: "ОК",
        });
    }
}

async function resetPasswordConfirm() {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');

    if (!token) {
        Swal.fire({
            title: "Ошибка",
            text: "Токен отсутствует в URL",
            icon: "error",
            confirmButtonText: "ОК",
        });
        return;
    }

    try {
        const response = await fetch(`/reset-password/confirm?token=${encodeURIComponent(token)}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            Swal.fire({
                title: "Успешно!",
                text: "Пароль успешно сброшен, новый пароль отправлен на почту",
                icon: "success",
                confirmButtonText: "ОК",
            }).then(() => {
                window.location.href = "/login";
            });
        } else {
            const errorData = await response.json();
            Swal.fire({
                title: "Ошибка",
                text: errorData.detail || "Не удалось сбросить пароль",
                icon: "error",
                confirmButtonText: "ОК",
            });
        }
    } catch (error) {
        console.error("Ошибка при сбросе пароля:", error);
        Swal.fire({
            title: "Ошибка",
            text: "Произошла ошибка при сбросе пароля",
            icon: "error",
            confirmButtonText: "ОК",
        });
    }
}

document.getElementById("reset-password-btn").addEventListener("click", resetPasswordConfirm);



function confirmDeleteDocument(documentUuid) {
    Swal.fire({
        title: "Вы уверены?",
        text: "Вы уверены, что хотите удалить этот документ?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Да, удалить",
        cancelButtonText: "Отмена",
    }).then((result) => {
        if (result.isConfirmed) {
            deleteDocument(documentUuid);
        }
    });
}


async function deleteDocument(documentUuid) {
    try {
        const response = await fetch(`/documents/${documentUuid}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            Swal.fire("Удалено!", "Документ был удален.", "success").then(() => {
                window.location.reload();
            });
        } else {
            Swal.fire({
                title: "Ошибка",
                text: "Не удалось удалить документ.",
                icon: "error",
                confirmButtonText: "ОК",
            });
        }
    } catch (error) {
        Swal.fire({
            title: "Ошибка",
            text: "Произошла ошибка при удалении документа.",
            icon: "error",
            confirmButtonText: "ОК",
        });
    }
}

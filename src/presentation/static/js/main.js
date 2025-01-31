function toggleProfileMenu() {
    const profileMenu = document.getElementById("profileMenu");
    profileMenu.classList.toggle("active");
}

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


function deleteAllDocuments() {
    Swal.fire({
        title: "Вы уверены?",
        text: "Вы уверены, что хотите удалить все документы?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Да, удалить",
        cancelButtonText: "Отмена",
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire("Удалено!", "Все документы удалены.", "success");
        }
    });
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
                timer: 2000,
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
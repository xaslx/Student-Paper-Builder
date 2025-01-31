function toggleProfileMenu() {
    const profileMenu = document.getElementById("profileMenu");
    profileMenu.classList.toggle("active");
}

function logout() {
    alert("Выход из системы");

}

function login() {
    alert("Вход из системы");


}

function deleteAllDocuments() {
    const confirmDelete = confirm("Вы уверены, что хотите удалить все документы?");
    if (confirmDelete) {
        alert("Все документы удалены");

    }
}
function aboutService() {
    const aboutUrl = document.getElementById("aboutUrl").value;
    window.location.href = aboutUrl;
}
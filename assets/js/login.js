const URL = "https://nomarket.pythonanywhere.com/"
// const URL = "http://127.0.0.1:5000/"


document.getElementById('login').addEventListener('submit', (event) => {
    event.preventDefault()
    var formData = new FormData()
    formData.append("username", document.getElementById("username").value)
    formData.append("contraseña", document.getElementById("password").value)
    fetch(URL + 'iniciar-sesion', {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.mensaje == "Bienvenido") {
            location.href = "index.html"
            let session = document.getElementById("username").value
            localStorage.setItem("session", session)
        } else {
            document.getElementById("error").classList.add("active")
            document.getElementById("errorText").innerHTML = data.mensaje
        }
    })
    .catch(error => {
        alert("Error al iniciar sesión")
        console.log(error)
    })
})

document.getElementById("closeError").addEventListener("click", () => {
    document.getElementById("error").classList.remove("active")
})

window.addEventListener("load", () => {
    localStorage.clear("session")
})
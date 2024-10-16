const URL = "http://127.0.0.1:5000/"


document.getElementById('formulario').addEventListener('submit', (event) => {
    event.preventDefault()
    var formData = new FormData()
    formData.append("username", document.getElementById('username').value)
    formData.append("email", document.getElementById('email').value)
    formData.append("contraseña", document.getElementById('contraseña').value)
    formData.append("rol", document.getElementById('rol').value)
    
    fetch(URL + 'ecommerce', {
        method: 'POST',
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
        alert(data.mensaje)
        document.getElementById("username").value = ""
        document.getElementById("email").value = ""
        document.getElementById("contraseña").value = ""
        document.getElementById("rol").value = ""
        document.getElementById("terminos").checked = false
    })
    .catch((error) => {
        alert("El usuario o el email ya existen!")
    })
})

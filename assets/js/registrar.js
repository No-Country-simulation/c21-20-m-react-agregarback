const URL = "http://127.0.0.1:5000/"


document.getElementById('formulario').addEventListener('submit', (event) => {
    event.preventDefault()
    var formData = new FormData()
    formData.append("username", document.getElementById('username').value)
    formData.append("email", document.getElementById('email').value)
    formData.append("contraseña", document.getElementById('contraseña').value)
    
    fetch(URL + 'agregar-usuario', {
        method: 'POST',
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data.mensaje)
        if(data.mensaje == "Usuario registrado") {
            document.getElementById("errorContainer").classList.add("success")
            document.getElementById("error").classList.add("active")
            document.getElementById("errorText").innerHTML = data.mensaje

            document.getElementById("username").value = ""
            document.getElementById("email").value = ""
            document.getElementById("contraseña").value = ""
            document.getElementById("terminos").checked = false
        } else {
            document.getElementById("errorContainer").classList.remove("success")
            document.getElementById("error").classList.add("active")
            document.getElementById("errorText").innerHTML = data.mensaje
        }
        
    })
    .catch((error) => alert(error))
})

document.getElementById("closeError").addEventListener("click", () => {
    document.getElementById("error").classList.remove("active")
})
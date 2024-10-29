const URL = "https://nomarket.pythonanywhere.com/"
// const URL = "http://127.0.0.1:5000/"


// Agregar usuario
document.getElementById('formulario').addEventListener('submit', (event) => {
    event.preventDefault()
    agregarUsuario()
    // agregarTienda()
})

document.getElementById("closeError").addEventListener("click", () => {
    document.getElementById("error").classList.remove("active")
})

function agregarUsuario() {
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
}

function agregarTienda() {
    var formData2 = new FormData()
    formData2.append("nombre", document.getElementById('username').value)
    formData2.append("imagen", "")
    formData2.append("vendedor", document.getElementById('username').value)
    fetch(URL + "agregar-tienda", {
        method: 'POST',
        body: formData2
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
    })
}
const URL = "http://127.0.0.1:5000/"

document.getElementById('login').addEventListener('submit', (event) => {
    event.preventDefault()
    
    fetch(URL + 'ecommerce')
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
    })
    .catch((error) => {
        alert(`Error al crear el usuario: ${error}`)
    })
})
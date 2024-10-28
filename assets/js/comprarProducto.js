//Recibir producto del back
let codigo = localStorage.getItem("productoSeleccionado")
const URL = "https://nomarket.pythonanywhere.com/"
// const URL = "http://127.0.0.1:5000/"


window.addEventListener("load", () => {
    var formData = new FormData()
    formData.append("codigo", codigo)

    fetch(URL + "mostrar-producto", {
        method: "POST",
        body: formData
    })
    .then((response) => response.json())
    .then((data) => {
        let container = document.getElementById("container")
        
        let content = document.createElement("div")
        content.classList.add("detalles-content")
        content.innerHTML = `
            <h1>${data.producto}</h1>
            <span>$${parseInt(data.precio).toLocaleString()}</span>
            <p>${data.descripcion}</p>
            <div class="input-group">
                <label for="cantidad">Cantidad:</label>
                <input type="number" name="cantidad" id="cantidad" placeholder="Ingrese la cantidad">
            </div>
            <div class="buttons-group">
                <button type="button" class="tienda-btn">Visitar tienda</button>
                <button type="button" class="buy-btn">Comprar</button>
            </div>
        `
        container.appendChild(content)
        let image = document.getElementById("image")
        let imageContent = document.createElement("img")
        imageContent.setAttribute("src", data.imagen)
        imageContent.setAttribute("alt", data.codigo)
        image.appendChild(imageContent)
    })
    .catch((error) => alert(error))
})
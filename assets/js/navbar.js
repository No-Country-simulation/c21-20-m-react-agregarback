document.getElementById("menuButton").addEventListener("click", () => {
    document.getElementById("navbar").classList.toggle("active")
})

window.addEventListener("load", () => {
    let session = localStorage.getItem("session")
    if (session != null) {
        document.getElementById("userContent").innerHTML = `
            <button type="button" class="login" id="login">
                ${session}
                <i class="bx bx-chevron-down"></i>
            </button>
            <div id="loginDropdown" class="login-dropdown">
                <a href="#">Mi tienda</a>
                <a href="iniciarsesion.html">Cerrar sesión</a>
            </div>
        `
        document.getElementById("login").addEventListener("click", () => {
            document.getElementById("loginDropdown").classList.toggle("active")
        })
    } else {
        document.getElementById("userContent").innerHTML = `
            <a href="iniciarsesion.html" class="user" id="user">
                Iniciar sesión
            </a>
        `
    }
})
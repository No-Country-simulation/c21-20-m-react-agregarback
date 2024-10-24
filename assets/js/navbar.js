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
                <div class="login-dropdown-content">
                    <a href="mitienda.html">Mi tienda</a>
                    <a href="iniciarsesion.html">Cerrar sesión</a>
                </div>
            </div>
        `
        document.getElementById("login").addEventListener("click", () => {
            document.getElementById("loginDropdown").classList.toggle("active")
        })
    } else {
        document.getElementById("userContent").innerHTML = `
        <div class="user">
            <a href="iniciarsesion.html" class="user-btn" id="user">
                Iniciar sesión
            </a>
        </div>
        `
    }
})
document.getElementById("filterBtn").addEventListener("click", () => {
    document.getElementById("filterShadow").classList.add("active")
    document.getElementById("filter").classList.add("active")
})

document.getElementById("filterShadow").addEventListener("click", (e) => {
    if (e.target.id == "filterShadow") {
        document.getElementById("filterShadow").classList.remove("active")
    document.getElementById("filter").classList.remove("active")
    }
})
window.addEventListener("scroll", function () {
    const header = document.getElementById("header");
    if (window.scrollY > 50) { // Adjust this value if needed
        header.classList.add("scrolled");
    } else {
        header.classList.remove("scrolled");
    }
});

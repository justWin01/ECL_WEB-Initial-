const params = new URLSearchParams(window.location.search);
const role = params.get("role");

const signupLink = document.getElementById("signup-link");

if (signupLink && role !== "admin") {
    signupLink.style.display = "none";
}

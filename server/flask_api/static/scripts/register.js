const registerForm = document.querySelector("#signup-form")

const password = document.querySelector("#user-password").value
const confirmPassword = document.querySelector("#confirm-user-password").value
registerForm.addEventListener("submit", (e)=>{
    // e.preventDefault()
    if (password.length < 5) {
        e.preventDefault()
        document.querySelector(".short-password").classList.add("showFormErrors")
    }
    if (password != confirmPassword){
        e.preventDefault()
        document.querySelector(".passwords-mismatch").classList.add("showFormErrors")
    }
    

})
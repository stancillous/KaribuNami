const registerForm = document.querySelector("#signup-form")

const password = document.querySelector(".user-password").value
const confirmPassword = document.querySelector(".confirm-user-password").value
registerForm.addEventListener("submit", (e)=>{
    e.preventDefault()
    console.log("passcode")
    console.log(password)
    console.log(confirmPassword)

})
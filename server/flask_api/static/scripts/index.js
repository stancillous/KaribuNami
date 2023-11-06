
sendForm = document.querySelector(".send-location-dets")

sendForm.addEventListener("submit", (e)=>{
    e.preventDefault()  // prevent form submit until the geolocation func is called
    navigator.geolocation.getCurrentPosition(function (position) {
        const { latitude, longitude } = position.coords;


        document.querySelector(".location-lat").value = latitude
        document.querySelector(".location-long").value = longitude

        console.log(document.querySelector(".location-lat").value)
        console.log(document.querySelector(".location-long").value)
        sendForm.submit()   // submit the form

      });

})

logoutBtn = document.querySelector(".user-logout-icon")

logoutBtn.addEventListener("click", ()=>{
  // fetch url (log user out)  
})


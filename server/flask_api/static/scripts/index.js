
sendForm = document.querySelector(".send-location-dets")

// sendForm.addEventListener("submit", (e)=>{
//     e.preventDefault()  // prevent form submit until the geolocation func is called
//     navigator.geolocation.getCurrentPosition(function (position) {
//         const { latitude, longitude } = position.coords;


//         document.querySelector(".location-lat").value = latitude
//         document.querySelector(".location-long").value = longitude

//         console.log(document.querySelector(".location-lat").value)
//         console.log(document.querySelector(".location-long").value)
//         sendForm.submit()   // submit the form

//       });

// })

//DYNAMICALLY SET THE YEAR (ON THE FOOTER)

let currentYear = new Date().getFullYear()

document.querySelector('.cp-year').textContent = currentYear


//ANIMATION
let tl = gsap.timeline()
tl.from(".tp-ttl", {y:-10, opacity:0, duration:1, ease:"back.easeOut"})
tl.from(".tp-p", {y:-10, opacity:0, duration:1, ease:"back.easeOut"})

// gsap.from(".about-app-tag", {
//   scrollTrigger:{
//     trigger:".aus-wrp",
//     markers:true,
//     start:"center center"
//   },
//   opacity:0,
//   y:33,
//   stagger:.2,

// })
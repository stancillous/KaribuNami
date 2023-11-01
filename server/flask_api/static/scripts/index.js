
// // function getCurrentLocation() {
// //   navigator.geolocation.getCurrentPosition(function(result) {
// //     console.log("getting")
// //     a = result.coords.latitude; // latitude value
// //     b = result.coords.longitude; // longitude value

// //     console.log(a)
// //     console.log(b)
// //   });
// // }
// // geolocationSupported();

// // function geolocationSupported() {
// //   if (navigator.geolocation) {
// //     console.log("Geolocation is supported by this browser :)");
// //     getCurrentLocation();
// //   } else {
// //     console.log("Geolocation is NOT supported by this browser :(");
// //   }
// // }






// sendForm = document.querySelector(".send-location-dets")

// sendForm.addEventListener("submit", (e)=>{
//     navigator.geolocation.getCurrentPosition(function (position) {
//         const { latitude, longitude } = position.coords;

//         console.log("inside")
//         console.log("lat is ", latitude)
//         console.log("long is ", longitude)
      
//         // Send the geolocation data to your backend
//         document.querySelector(".location-lat").value = latitude
//         document.querySelector(".location-long").value = longitude

//         console.log(document.querySelector(".location-lat").value)
//         console.log(document.querySelector(".location-long").value)
//         sendForm.submit()

//       });

// })


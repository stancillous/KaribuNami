document.addEventListener('DOMContentLoaded', function() {

    // CLOSING THE LOGIN MODAL WHEN THE X IS CLICKED
    let closeModal = document.querySelector('.close-modal')
    closeModal.addEventListener('click',()=>{
        modal.classList.remove('showModal')

    })
  
});

// show login modal when not-signed-in-users click the SAVE button
function showSignInModal(){
    let modal = document.querySelector('.addmodal')
    modal.classList.add('showModal')

}

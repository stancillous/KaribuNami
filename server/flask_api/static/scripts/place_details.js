document.addEventListener('DOMContentLoaded', function() {

    let button = document.getElementById('user-not-signed-in');
    let modal = document.querySelector('.addmodal')

    button.addEventListener("click", ()=>{
        modal.classList.add('showModal')

    })


    // CLOSING THE LOGIN MODAL WHEN THE X IS CLICKED
    let closeModal = document.querySelector('.close-modal')
    closeModal.addEventListener('click',()=>{
        modal.classList.remove('showModal')

    })
});
document.addEventListener('DOMContentLoaded', function () {
  // CLOSING THE LOGIN MODAL WHEN THE X IS CLICKED
  const closeModal = document.querySelector('.close-modal');
  closeModal.addEventListener('click', () => {
    modal.classList.remove('showModal');
  });
});

// show login modal when not-signed-in-users click the SAVE button
function showSignInModal () {
  const modal = document.querySelector('.addmodal');
  modal.classList.add('showModal');
}


//hide the  login modal when user clicks X/close
function hideSignInModal () {
  const modal = document.querySelector('.addmodal');
  modal.classList.remove('showModal');
}

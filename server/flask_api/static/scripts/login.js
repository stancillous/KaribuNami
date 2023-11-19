document.addEventListener('DOMContentLoaded', function () {
  const button = document.getElementById('user-not-signed-in');
  const modal = document.querySelector('.addmodal');

  // CLOSING THE LOGIN MODAL WHEN THE X IS CLICKED
  const closeModal = document.querySelector('.close-modal');
  closeModal.addEventListener('click', () => {
    modal.classList.add('removeModal');
  });
});

// ALLOWING USER TO TOGGLE BETWEEN SEEING AND HIDING THEIR PASSWORDS WHEN TYPING THEM
const seePassword = document.querySelector('.password-open-img');
const closePassword = document.querySelector('.password-closed-img');

closePassword.addEventListener('click', () => {
  document.querySelector('#passcode-input').type = 'password';
  seePassword.style.display = 'block';
  closePassword.style.display = 'none';
});

seePassword.addEventListener('click', () => {
  document.querySelector('#passcode-input').type = 'text';
  closePassword.style.display = 'block';
  seePassword.style.display = 'none';
});

// ALLOWING USER TO TOGGLE BETWEEN SEEING AND HIDING THEIR PASSWORDS WHEN TYPING THEM

// for the first password input field
const seePassword = document.querySelector('.svg-open-1');
const closePassword = document.querySelector('.svg-close-1');

closePassword.addEventListener('click', () => {
  document.querySelector('#user-password').type = 'password';
  seePassword.style.display = 'block';
  closePassword.style.display = 'none';
});

seePassword.addEventListener('click', () => {
  document.querySelector('#user-password').type = 'text';
  closePassword.style.display = 'block';
  seePassword.style.display = 'none';
});

// for the first password input field
const seePassword2 = document.querySelector('.svg-open-2');
const closePassword2 = document.querySelector('.svg-close-2');

closePassword2.addEventListener('click', () => {
  document.querySelector('#confirm-user-password').type = 'password';
  seePassword2.style.display = 'block';
  closePassword2.style.display = 'none';
});

seePassword2.addEventListener('click', () => {
  document.querySelector('#confirm-user-password').type = 'text';
  closePassword2.style.display = 'block';
  seePassword2.style.display = 'none';
});

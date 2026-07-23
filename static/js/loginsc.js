const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const showSignup = document.getElementById("showSignup");
const showLogin = document.getElementById("showLogin");

showSignup.addEventListener("click", (e) => {
  e.preventDefault();
  loginForm.classList.add("d-none");
  signupForm.classList.remove("d-none");
});

showLogin.addEventListener("click", (e) => {
  e.preventDefault();
  signupForm.classList.add("d-none");
  loginForm.classList.remove("d-none");
});


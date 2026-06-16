function setupToggle(inputId, toggleId) {
    const input = document.getElementById(inputId);
    const toggle = document.getElementById(toggleId);

    if (input && toggle) {
        toggle.addEventListener("click", () => {
            const isHidden = input.type === "password";
            input.type = isHidden ? "text" : "password";
        });
    }
}

setupToggle("loginPassword", "toggleLoginPassword");
setupToggle("registerPassword", "toggleRegisterPassword");
setupToggle("confirmPassword", "toggleConfirmPassword");

const toggleButton = document.getElementById("theme-toggle");

if(localStorage.getItem("theme") === "dark"){
  document.body.classList.add("dark-mode");
}

toggleButton.addEventListener("click",()=>{

  document.body.classList.toggle("dark-mode");

  if(document.body.classList.contains("dark-mode")){
    localStorage.setItem("theme","dark");
  }else{
   localStorage.setItem("theme","light");
  }
});
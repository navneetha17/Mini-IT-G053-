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
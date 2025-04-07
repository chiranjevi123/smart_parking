document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.querySelector("#registerForm");
    const loginForm = document.querySelector("#loginForm");

    if (registerForm) {
        addRealTimeValidation(registerForm);
        addTogglePasswordVisibility("#password", "#togglePassword");
        addTogglePasswordVisibility("#confirm_password", "#toggleConfirmPassword");

        registerForm.addEventListener("submit", function (event) {
            let valid = validateRegisterForm();
            if (!valid) event.preventDefault();
        });
    }

    if (loginForm) {
        addRealTimeValidation(loginForm);
        addTogglePasswordVisibility("#loginPassword", "#toggleLoginPassword");

        loginForm.addEventListener("submit", function (event) {
            let valid = validateLoginForm();
            if (!valid) event.preventDefault();
        });
    }

    function validateRegisterForm() {
        let valid = true;
        const fullName = document.querySelector("#fullname");
        const email = document.querySelector("#email");
        const password = document.querySelector("#password");
        const confirmPassword = document.querySelector("#confirm_password");
        const terms = document.querySelector("#check");

        clearErrors();

        if (fullName.value.trim() === "") {
            showError(fullName, "Full Name is required");
            valid = false;
        }

        if (!validateEmail(email.value)) {
            showError(email, "Enter a valid email");
            valid = false;
        }

        if (!validatePasswordStrength(password.value)) {
            showError(password, "Password must be at least 6 characters with a mix of letters & numbers");
            valid = false;
        }

        if (password.value !== confirmPassword.value) {
            showError(confirmPassword, "Passwords do not match");
            valid = false;
        }

        if (!terms.checked) {
            showError(terms, "You must agree to the terms");
            valid = false;
        }

        return valid;
    }

    function validateLoginForm() {
        let valid = true;
        const email = document.querySelector("#loginEmail");
        const password = document.querySelector("#loginPassword");

        clearErrors();

        if (!validateEmail(email.value)) {
            showError(email, "Enter a valid email");
            valid = false;
        }

        if (password.value.trim() === "") {
            showError(password, "Password is required");
            valid = false;
        }

        return valid;
    }

    function addRealTimeValidation(form) {
        form.querySelectorAll("input").forEach(input => {
            input.addEventListener("input", function () {
                validateInput(input);
            });
        });
    }

    function validateInput(input) {
        clearError(input);

        if (input.id === "email" || input.id === "loginEmail") {
            if (!validateEmail(input.value)) {
                showError(input, "Invalid email format");
            }
        } else if (input.id === "password") {
            let strengthMessage = getPasswordStrengthMessage(input.value);
            if (strengthMessage) {
                showError(input, strengthMessage);
            }
        } else if (input.id === "confirm_password") {
            const password = document.querySelector("#password").value;
            if (input.value !== password) {
                showError(input, "Passwords do not match");
            }
        }
    }

    function showError(input, message) {
        clearError(input);
        const error = document.createElement("p");
        error.className = "error";
        error.style.color = "red";
        error.textContent = message;
        input.parentNode.appendChild(error);
        input.style.border = "2px solid red";
    }

    function clearError(input) {
        if (input) {
            input.style.border = "";
            const error = input.parentNode.querySelector(".error");
            if (error) error.remove();
        }
    }

    function clearErrors() {
        document.querySelectorAll(".error").forEach(e => e.remove());
        document.querySelectorAll("input").forEach(input => (input.style.border = ""));
    }

    function validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function validatePasswordStrength(password) {
        return password.length >= 6 && /[A-Za-z]/.test(password) && /[0-9]/.test(password);
    }

    function getPasswordStrengthMessage(password) {
        if (password.length < 6) return "Password too short";
        if (!/[A-Za-z]/.test(password) || !/[0-9]/.test(password)) return "Use letters & numbers";
        return "";
    }

    function addTogglePasswordVisibility(passwordSelector, toggleButtonSelector) {
        const passwordInput = document.querySelector(passwordSelector);
        const toggleButton = document.querySelector(toggleButtonSelector);

        if (passwordInput && toggleButton) {
            toggleButton.addEventListener("click", function () {
                if (passwordInput.type === "password") {
                    passwordInput.type = "text";
                    toggleButton.textContent = "🙈"; // Eye Closed Emoji
                } else {
                    passwordInput.type = "password";
                    toggleButton.textContent = "👁️"; // Eye Open Emoji
                }
            });
        }
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // ----- Toggle Password Visibility -----
    document.querySelectorAll('.password-toggle').forEach(toggle => {
        toggle.addEventListener('click', function () {
            const input = this.parentElement.querySelector('input');
            const eyeIcon = this.querySelector('i');

            if (input.type === 'password') {
                input.type = 'text';
                eyeIcon.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                input.type = 'password';
                eyeIcon.classList.replace('fa-eye-slash', 'fa-eye');
            }
        });
    });

    // ----- Password Strength Indicator -----
    document.querySelectorAll('#id_password1').forEach(passwordInput => {
        const strengthBar = passwordInput
            .closest('.form-group')
            .querySelector('.password-strength-bar');

        if (strengthBar) {
            passwordInput.addEventListener('input', function () {
                const password = this.value;
                strengthBar.className = 'password-strength-bar'; // reset classes

                if (password.length === 0) {
                    strengthBar.style.width = '0';
                    return;
                }

                let strength = 0;
                if (password.length >= 8) strength += 1;
                if (/[a-z]/.test(password)) strength += 1;
                if (/[A-Z]/.test(password)) strength += 1;
                if (/[0-9]/.test(password)) strength += 1;
                if (/[^A-Za-z0-9]/.test(password)) strength += 1;

                // Update strength bar width (0-100%)
                const width = (strength / 5) * 100;
                strengthBar.style.width = `${width}%`;

                if (strength <= 2) {
                    strengthBar.classList.add('weak');
                } else if (strength <= 4) {
                    strengthBar.classList.add('medium');
                } else {
                    strengthBar.classList.add('strong');
                }
            });
        }
    });

    // ----- Real-Time Required Field Validation -----
    const inputs = document.querySelectorAll('input[required], select[required]');
    inputs.forEach(input => {
        input.addEventListener('blur', function () {
            if (!this.value) {
                let errorElement = this.parentElement.querySelector('.form-error');
                if (!errorElement) {
                    errorElement = document.createElement('div');
                    errorElement.className = 'form-error';
                    this.parentElement.appendChild(errorElement);
                }
                errorElement.innerHTML = '<i class="fas fa-exclamation-circle"></i> This field is required';
            }
        });

        input.addEventListener('input', function () {
            const errorElement = this.parentElement.querySelector('.form-error');
            if (errorElement && this.value) {
                errorElement.textContent = '';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    // Declare lucide variable
    const lucide = window.lucide;
  
    // Sign Up Form Validation
    const signupForm = document.getElementById('signup-form');
    
    if (signupForm) {
      const fullNameInput = document.getElementById('fullName');
      const emailInput = document.getElementById('email');
      const passwordInput = document.getElementById('password');
      const confirmPasswordInput = document.getElementById('confirmPassword');
      const submitButton = document.getElementById('submit-button');
      const successMessage = document.getElementById('success-message');
      
      signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Reset previous errors
        clearErrors();
        
        // Validate form
        let isValid = true;
        
        // Validate full name
        if (!fullNameInput.value.trim()) {
          showError(fullNameInput, 'Full name is required');
          isValid = false;
        }
        
        // Validate email
        if (!emailInput.value.trim()) {
          showError(emailInput, 'Email is required');
          isValid = false;
        } else if (!emailInput.value.includes('@') || !emailInput.value.endsWith('.edu')) {
          showError(emailInput, 'Please enter a valid university email (.edu)');
          isValid = false;
        }
        
        // Validate password
        if (!passwordInput.value) {
          showError(passwordInput, 'Password is required');
          isValid = false;
        } else if (passwordInput.value.length < 8) {
          showError(passwordInput, 'Password must be at least 8 characters');
          isValid = false;
        } else if (!/(?=.*[A-Za-z])(?=.*\d)/.test(passwordInput.value)) {
          showError(passwordInput, 'Password must contain letters and numbers');
          isValid = false;
        }
        
        // Validate confirm password
        if (passwordInput.value !== confirmPasswordInput.value) {
          showError(confirmPasswordInput, 'Passwords do not match');
          isValid = false;
        }
        
        // If form is valid, show success message
        if (isValid) {
          // Disable submit button and show loading state
          submitButton.disabled = true;
          submitButton.textContent = 'Creating Account...';
          
          // Simulate API call with timeout
          setTimeout(() => {
            // Hide form and show success message
            signupForm.style.display = 'none';
            successMessage.style.display = 'flex';
            
            // Redirect to sign in page after 2 seconds
            setTimeout(() => {
              window.location.href = 'signin.html';
            }, 2000);
          }, 1500);
        }
      });
  
      // Helper function to show error message
      function showError(input, message) {
        input.classList.add('error');
        const errorElement = document.getElementById(`${input.id}-error`);
        if (errorElement) {
          errorElement.innerHTML = `<i data-lucide="alert-circle"></i> ${message}`;
          lucide.createIcons();
        }
      }
      
      // Helper function to clear all errors
      function clearErrors() {
        const inputs = [fullNameInput, emailInput, passwordInput, confirmPasswordInput];
        inputs.forEach(input => {
          input.classList.remove('error');
          const errorElement = document.getElementById(`${input.id}-error`);
          if (errorElement) {
            errorElement.textContent = '';
          }
        });
      }
      
      // Clear error when user starts typing
      [fullNameInput, emailInput, passwordInput, confirmPasswordInput].forEach(input => {
        input.addEventListener('input', function() {
          this.classList.remove('error');
          const errorElement = document.getElementById(`${this.id}-error`);
          if (errorElement) {
            errorElement.textContent = '';
          }
        });
      });
    }
    
    // Sign In Form Validation
    const signinForm = document.getElementById('signin-form');
    
    if (signinForm) {
      const emailInput = document.getElementById('email');
      const passwordInput = document.getElementById('password');
      const submitButton = document.getElementById('submit-button');
      const authError = document.getElementById('auth-error');
      
      signinForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Reset previous errors
        clearErrors();
        
        // Validate form
        let isValid = true;
        
        // Validate email
        if (!emailInput.value.trim()) {
          showError(emailInput, 'Email is required');
          isValid = false;
        }
        
        // Validate password
        if (!passwordInput.value) {
          showError(passwordInput, 'Password is required');
          isValid = false;
        }
        
        // If form is valid, attempt login
        if (isValid) {
          // Hide any previous auth errors
          if (authError) {
            authError.style.display = 'none';
          }
          
          // Disable submit button and show loading state
          submitButton.disabled = true;
          submitButton.textContent = 'Signing in...';
          
          // Simulate API call with timeout
          setTimeout(() => {
            // Check for test credentials
            if (emailInput.value === 'test@university.edu' && passwordInput.value === 'Testing123') {
              // Redirect to dashboard
              window.location.href = 'dashboard.html';
            } else {
              // Show auth error
              if (authError) {
                authError.style.display = 'flex';
                lucide.createIcons();
              }
              
              // Re-enable submit button
              submitButton.disabled = false;
              submitButton.textContent = 'Sign in';
            }
          }, 1000);
        }
      });
      
      // Helper function to show error message
      function showError(input, message) {
        input.classList.add('error');
        const errorElement = document.getElementById(`${input.id}-error`);
        if (errorElement) {
          errorElement.innerHTML = `<i data-lucide="alert-circle"></i> ${message}`;
          lucide.createIcons();
        }
      }
      
      // Helper function to clear all errors
      function clearErrors() {
        const inputs = [emailInput, passwordInput];
        inputs.forEach(input => {
          input.classList.remove('error');
          const errorElement = document.getElementById(`${input.id}-error`);
          if (errorElement) {
            errorElement.textContent = '';
          }
        });
      }
      
      // Clear error when user starts typing
      [emailInput, passwordInput].forEach(input => {
        input.addEventListener('input', function() {
          this.classList.remove('error');
          const errorElement = document.getElementById(`${this.id}-error`);
          if (errorElement) {
            errorElement.textContent = '';
          }
          
          // Hide auth error
          if (authError) {
            authError.style.display = 'none';
          }
        });
      });
    }
  });
  
  
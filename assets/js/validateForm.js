  // Function to validate the form
  function validateForm() {
    // Get form inputs
    var name = document.getElementById('user_name').value;
    var email = document.getElementById('user_email').value;
    var password = document.getElementById('user_password').value;
    var confirm_password = document.getElementById('confirm_password').value;

    // Clear previous error messages
    clearErrorMessages();

    // Validate name, email, password, and confirm_password
    var isValid = true;

    if (name.trim() == '') {
      displayErrorMessage('user_name', 'Please enter your name.');
      isValid = false;
    } else if (name.length <= 2) {
      displayErrorMessage('user_name', 'Name must be greater than 2 characters.');
      isValid = false;
    }
    if (email.trim() == '') {
      displayErrorMessage('user_email', 'Please enter your email.');
      isValid = false;
    } else if (!isValidEmail(email)) {
      displayErrorMessage('user_email', 'Please enter a valid email address.');
      isValid = false;
    }
    if (password.trim() == '') {
      displayErrorMessage('user_password', 'Please enter a password.');
      isValid = false;
    } else if (!isValidPassword(password)) {
      displayErrorMessage('user_password', 'Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character.');
      isValid = false;
    }
    if (confirm_password.trim() == '') {
      displayErrorMessage('confirm_password', 'Please confirm your password.');
      isValid = false;
    } else if (password != confirm_password) {
      displayErrorMessage('confirm_password', 'Password and confirm password do not match.');
      isValid = false;
    }

    return isValid;
  }

  // Function to validate email syntax using regular expression
  function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  // Function to validate password syntax using regular expression
  function isValidPassword(password) {
    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]).{8,}$/;
    return passwordRegex.test(password);
  }

  // Function to display error message
  function displayErrorMessage(fieldId, errorMessage) {
    var field = document.getElementById(fieldId);
    var errorElement = field.nextElementSibling;
    if (errorElement && errorElement.classList.contains('error-message')) {
      errorElement.textContent = errorMessage;
    } else {
      var p = document.createElement('p');
      p.classList.add('error-message');
      p.textContent = errorMessage;
      field.parentNode.insertBefore(p, field.nextSibling);
    }
  }

  // Function to clear error messages
  function clearErrorMessages() {
    var errorElements = document.getElementsByClassName('error-message');
    for (var i = 0; i < errorElements.length; i++) {
      errorElements[i].textContent = '';
    }
  }

  // Add input event listener to the name field
  var nameField = document.getElementById('user_name');
  nameField.addEventListener('input', function () {
    var name = this.value;
    if (name.trim() != '') {
      if (name.length > 2) {
        clearErrorMessages();
      } else {
        displayErrorMessage('user_name', 'Name must be greater than 2 characters.');
      }
    }
  });

  // Add input event listener to the email field
  var emailField = document.getElementById('user_email');
  emailField.addEventListener('input', function () {
    var email = this.value;
    if (email.trim() != '') {
      if (isValidEmail(email)) {
        clearErrorMessages();
      } else {
        displayErrorMessage('user_email', 'Please enter a valid email address.');
      }
    }
  });

  // Add input event listener to the password field
  var passwordField = document.getElementById('user_password');
  passwordField.addEventListener('input', function () {
    var password = this.value;
    if (password.trim() != '') {
      if (isValidPassword(password)) {
        clearErrorMessages();
      } else {
        displayErrorMessage('user_password', 'Password must has at least 8 characters that include at least 1 lowercase character, 1 uppercase characters, 1 number, and 1 special character in (!@#$%^&*)');
      }
    }
  });



  //  validate Task Form
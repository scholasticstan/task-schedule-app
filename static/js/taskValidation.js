
  // Store the initial error state for each field
  var errorState = {
    name: false,
    start_date: false,
    end_date: false,
    stop_time: false
  };

  function validateForm() {
    // Get the form inputs
    var name = document.getElementById("name").value;
    var startDate = document.getElementById("start_date").value;
    var endDate = document.getElementById("end_date").value;
    var stopTime = document.getElementById("stop_time").value;
    var status = document.getElementById("status");

    // Remove any existing error messages
    removeErrorMessages();

    // Perform your validation logic here
    var isValid = true;

    if (name === "") {
      createErrorMessage("name", "Name is required.");
      errorState.name = true;
      isValid = false;
    } else if (name.length <= 2) {
      createErrorMessage("name", "Name must be greater than 2 characters.");
      errorState.name = true;
      isValid = false;
    } else {
      errorState.name = false;
    }

    if (startDate === "") {
      createErrorMessage("start_date", "Start date is required.");
      errorState.start_date = true;
      isValid = false;
    } else {
      errorState.start_date = false;
    }

    if (endDate === "") {
      createErrorMessage("end_date", "End date is required.");
      errorState.end_date = true;
      isValid = false;
    } else {
      errorState.end_date = false;
    }

    if (stopTime === "") {
      createErrorMessage("stop_time", "Stop time is required.");
      errorState.stop_time = true;
      isValid = false;
    } else {
      errorState.stop_time = false;
    }

    // Check if start date is not in the past
    var currentDate = new Date().toISOString().split("T")[0];
    if (startDate < currentDate) {
      createErrorMessage("start_date", "Start date must be today or in the future.");
      errorState.start_date = true;
      isValid = false;
    }

    // Check if end date is after start date
    if (endDate < startDate) {
      createErrorMessage("end_date", "End date must be after start date.");
      errorState.end_date = true;
      isValid = false;
    }

    // Check if stop time is in the future
    var currentTime = new Date().toISOString().split("T")[0] + "T" + new Date().toISOString().split("T")[1];
    if (endDate === currentDate && stopTime < currentTime) {
      createErrorMessage("stop_time", "Stop time must be in the future.");
      errorState.stop_time = true;
      isValid = false;
    } else if (endDate < currentDate || (endDate === currentDate && stopTime <= currentTime)) {
      createErrorMessage("end_date", "End date and stop time must be after the current time.");
      errorState.end_date = true;
      errorState.stop_time = true;
      isValid = false;
    } else {
      errorState.stop_time = false;
      errorState.end_date = false;
    }

    // Add or remove CSS class based on status value
    const selectStatus = document.getElementById('status');
    const cardDiv = document.getElementById('cardDiv');
    
    selectStatus.addEventListener('change', function() {
        if (selectStatus.value === 'completed') {
            cardDiv.style.backgroundColor = '#9e9797'; // Set the background color for complete status
        } else {
            cardDiv.style.backgroundColor = ''; // Reset the background color
        }
    });

    // Validation passed, submit the form
    return isValid;
  }

  function createErrorMessage(fieldId, message) {
    var field = document.getElementById(fieldId);
    var errorMessage = document.createElement("p");
    errorMessage.className = "error-message";
    errorMessage.textContent = message;
    field.parentNode.insertBefore(errorMessage, field.nextSibling);
  }

  function removeErrorMessages() {
    var errorMessages = document.getElementsByClassName("error-message");
    while (errorMessages.length > 0) {
      errorMessages[0].parentNode.removeChild(errorMessages[0]);
    }
  }

  // Add event listeners to each input field to check for changes and show/hide error messages
  document.getElementById("name").addEventListener("input", function() {
    if (errorState.name) {
      removeErrorMessages();
      validateForm();
    }
  });

  document.getElementById("start_date").addEventListener("input", function() {
    if (errorState.start_date) {
      removeErrorMessages();
      validateForm();
    }
  });

  document.getElementById("end_date").addEventListener("input", function() {
    if (errorState.end_date) {
      removeErrorMessages();
      validateForm();
    }
  });

  document.getElementById("stop_time").addEventListener("input", function() {
   if (errorState.stop_time) {
      removeErrorMessages();
      validateForm();
    }
  });

  document.getElementById("status").addEventListener("change", function() {
    validateForm();
  });

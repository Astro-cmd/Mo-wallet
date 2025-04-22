document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("signupForm");
  const submitBtn = document.getElementById("submitBtn");
  const spinner = document.getElementById("spinner");
  const btnText = document.querySelector(".btn-text");

  if (!form) return;

  // Get validation URL from form data attribute
  const validateUrl = form.dataset.validateUrl;

  // Add real-time validation on input change
  form.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", () => {
      clearError(input.name);
      validateField(input);
    });
  });

  // Form submission handler
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    // Validate all fields before submission
    let isValid = true;
    const inputs = form.querySelectorAll("input");
    
    inputs.forEach(input => {
      if (!validateField(input)) {
        isValid = false;
      }
    });

    if (!isValid) return;

    // Prepare form data
    const formData = new FormData(form);
    
    // Show loading state
    submitBtn.disabled = true;
    btnText.textContent = "Creating account...";
    spinner.classList.remove("hidden");

    try {
      // First validate with AJAX
      const validationResponse = await fetch(validateUrl, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        }
      });

      const validationData = await validationResponse.json();

      if (!validationResponse.ok) {
        throw new Error("Validation request failed");
      }

      if (validationData.success) {
        // If validation succeeds, submit the form
        form.submit();
      } else {
        // Show validation errors
        showErrors(validationData.errors);
      }
    } catch (error) {
      console.error("Signup error:", error);
      showGlobalError("An error occurred. Please try again.");
    } finally {
      // Reset button state
      submitBtn.disabled = false;
      btnText.textContent = "Create Account";
      spinner.classList.add("hidden");
    }
  });

  // Field validation function
  function validateField(input) {
    const fieldName = input.name;
    const value = input.value.trim();
    let isValid = true;
    let errorMessage = "";

    // Skip validation if field is empty (handled by HTML5 required)
    if (!value) return true;

    switch (fieldName) {
      case "username":
        if (value.length < 4 || value.length > 30) {
          errorMessage = "Username must be 4-30 characters long.";
          isValid = false;
        } else if (!/^[\w.@+-]+$/.test(value)) {
          errorMessage = "Enter a valid username. Letters, digits and @/./+/-/_ only.";
          isValid = false;
        }
        break;
      
      case "email":
        if (!/^[\w.-]+@[\w.-]+\.\w+$/.test(value)) {
          errorMessage = "Enter a valid email address.";
          isValid = false;
        }
        break;
      
      case "phone_number":
        if (!/^(0(7|1)\d{8}|(\+?254(7|1)\d{8}))$/.test(value)) {
          errorMessage = "Enter a valid Kenyan phone number (e.g., 0712345678 or +254712345678).";
          isValid = false;
        }
        break;
      
      case "password1":
        if (value.length < 8) {
          errorMessage = "Password must be at least 8 characters.";
          isValid = false;
        } else if (!/(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])/.test(value)) {
          errorMessage = "Password must include uppercase, lowercase, number, and special character.";
          isValid = false;
        }
        break;
      
      case "password2":
        const password1 = form.querySelector("#id_password1").value;
        if (value !== password1) {
          errorMessage = "Passwords don't match.";
          isValid = false;
        }
        break;
    }

    if (!isValid) {
      showError(fieldName, errorMessage);
    }

    return isValid;
  }

  // Error display functions
  function showError(fieldName, message) {
    const errorElement = document.getElementById(`${fieldName}Error`);
    const inputElement = document.getElementById(`id_${fieldName}`);
    
    if (errorElement) {
      errorElement.textContent = message;
    }
    
    if (inputElement) {
      inputElement.classList.add("error");
    }
  }

  function clearError(fieldName) {
    const errorElement = document.getElementById(`${fieldName}Error`);
    const inputElement = document.getElementById(`id_${fieldName}`);
    
    if (errorElement) {
      errorElement.textContent = "";
    }
    
    if (inputElement) {
      inputElement.classList.remove("error");
    }
  }

  function showErrors(errors) {
    for (const field in errors) {
      showError(field, errors[field]);
    }
  }

  function showGlobalError(message) {
    // You could add a global error display area if needed
    alert(message); // Simple fallback
  }
});
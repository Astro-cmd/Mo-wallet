document.addEventListener("DOMContentLoaded", function() {
    // Open signup page when "Sign up" link is clicked
    const showSignup = document.getElementById("showSignup");
  
    if (showSignup) {
      showSignup.addEventListener("click", function(e) {
        // Optional: prevent default behavior if you need to add something extra before navigation
        // e.preventDefault();
        window.location.href = "/users/signup/";  // Navigate to the signup page
      });
    }
  });
  


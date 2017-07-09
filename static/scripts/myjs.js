"use strict"

$(document).ready(function() {

  /////////////////////////////////////
  // Toggle log in and sign up forms //
  /////////////////////////////////////

  $("#signUpBtn").on("click", function(){
      $("#logInForm").hide();
      $("#fNameSignUp, #lNameSignUp").attr("type", "text");
      $("#emailSignUp").attr("type", "email");
      $("#pwSignUp, #pwConfirmSignUp").attr("type", "password");
      $("#submitSignUp").attr("type", "submit");
      $("#signUpBtn").prop("disabled");
      $("#logInBtn").prop("disabled", false);
  });


  $("#logInBtn").on("click", function(){
      $("#fNameSignUp, #lNameSignUp, #emailSignUp, #pwSignUp, #submitSignUp, #pwConfirmSignUp").attr("type", "hidden");
      $("#logInForm").show();
      $("#logInBtn").prop("disabled");
      $("#signUpBtn").prop("disabled", false);
  });
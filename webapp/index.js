$(document).ready(function(){

  $("#search").click(function(){

    var First = $("#first").val().trim();
    var Last = $("#last").val().trim();
    var County = $("#county").val();
    var State = $("#state").val();

    // Checking for blank fields.
    if( First == '' && Last == ''){
      $('input[type="text"],input[type="text"]').css("border","2px solid red");
      $('input[type="text"],input[type="text"]').css("box-shadow","0 0 3px red");
      alert("At least give me a first or last name to search please.");
    }

    if( (First =='david' || First =='David') && (Last =='turner' || Last == 'Turner') ){
      $('input[type="text"],input[type="text"]').css("border","2px solid red");
      $('input[type="text"],input[type="text"]').css("box-shadow","0 0 3px red");
      alert("Never Search the creator.. Destruction Protocol initiated...");
    }

    else {

          window.location.replace("results.html?id=" + user);

    } /* End of else*/


  }); // End of login.click function
}); // End of ready function

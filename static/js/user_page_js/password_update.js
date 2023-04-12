$(document).ready(function (){
    $(document).on("click", "#update_change_password", function (){
        var user_username = $("#user_username").val();
        var update_password_id = $("#update_password_id").val();
        var old_password = $("#current_password").val();
        var new_password = $("#new_password").val();
        var confirm_password = $("#confirm_password").val();
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            // alert(update_password_id);
 console.log(old_password);
 console.log(new_password);
 console.log(confirm_password);
        $.ajax({
            url:"user_update_password",
            method:"POST",
            headers: {'X-CSRFToken': csrftoken},
            data:{
              user_username:user_username,
              update_password_id:update_password_id,
              old_password:old_password,
              new_password:new_password,
              confirm_password:confirm_password
            },

           success:function (html){

                if(html === "error_old_password"){
                   console.log(html);
                   $("#current_password").addClass("is-invalid");

                   Swal.fire({
                   title: "error",
                   text: "Current Password Is Not Matching...!",
                   icon: "error",
                   showConfirmButton: false,
                   timer:1700
                 });
                }else if(html === "new_and_confirm_not_ok"){
                   console.log(html);
                   $("#current_password").removeClass("is-invalid");
                    $("#new_password").addClass("is-invalid");
                    $("#confirm_password").addClass("is-invalid");

                   Swal.fire({
                   title: "Oppss...!",
                   text: "New and Confirm password not matching...!",
                   icon: "error",
                   showConfirmButton: false,
                   timer:1700
                 });
                }else {
                   console.log(html);

                   Swal.fire({
                   title: "success",
                   text: "Password Updated...!",
                   icon: "success",
                   showConfirmButton: false,
                   timer:1700
                 }).then(function (){
                     location.reload();
                   });

                }
            },

        });
    });
});

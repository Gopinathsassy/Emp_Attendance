
$(document).ready(function(){
    $(document).on('click', '#create_user', function(){
       var emp_id = $("#emp_id").val();
         var username = $("#username").val();
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var dob = $("#dob").val();
        var blood_group = $("#blood_group").val();
        var module = $("#module").val();
        var official_email_id = $("#official_email_id").val();
        var personal_email_id = $("#personal_email_id").val();
        var adhar_no = $("#adhar_no").val();
        var mobile_no = $("#mobile_no").val();
        var password = $("#password").val();
        var confirm_password = $("#confirm_password").val();
        var address = $("#address").val();
        var gender = $("#gender").val();
        var job_role = $("#job_role").val();
        var date_of_join = $("#date_of_join").val();
        var acc_no = $("#acc_no").val();
        var ifsc_code = $("#ifsc_code").val();
        var branch = $("#branch").val();
// alert(acc_no);
        if(first_name =="" || last_name =="" || emp_id =="" || username ==""){
            alert("Please complete field");


        }else{
          if(password===confirm_password ||password!==""){
                $.ajax({
                type: "POST",
                url: "user_registration",
                data:{
                emp_id :emp_id,
                username : username,
                first_name : first_name,
                last_name : last_name,
                dob : dob,
                blood_group:blood_group,
                module:module,
                official_email_id : official_email_id,
                personal_email_id : personal_email_id,
                adhar_no : adhar_no,
                mobile_no : mobile_no,
                password : password,
                address :address,
                gender :gender,
                job_role:job_role,
                date_of_join:date_of_join,
                acc_no:acc_no,
                ifsc_code:ifsc_code,
                branch:branch,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function (html){
                                  Swal.fire({
                                    title: "Success",
                                    text: "User Created Successfully...!",
                                    icon: "success",
                                    showConfirmButton: false,
                                    timer:1500
                                }).then(function () {
                                    location.reload();
                                });
                $("#create").removeAttr("disabled", "disabled");
            },
                error:function (html){
                          Swal.fire({
                            title: "Opps...",
                            text: "User Not Created...!",
                            icon: "warning",
                            showConfirmButton: false,
                            timer:1500
                        });
                $("#create").removeAttr("disabled", "disabled");
            }
            });
          }else{
               if(password!==confirm_password){
                      Swal.fire({
                        title: "Opps...",
                        text: "password did'nt match...!",
                        icon: "warning",
                        showConfirmButton: false,
                        timer:1500
                    });
                $("#create").removeAttr("disabled", "disabled");
            }
               }
            }


    });
});








$('#edit_users').on('click', function(){
        var id = $("#id").val();
         var password = $("#password").val();
        var emp_id = $("#emp_id").val();
        var username = $("#username").val();
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var dob = $("#dob").val();
        var official_email_id = $("#official_email_id").val();
        var personal_email_id = $("#personal_email_id").val();
        var adhar_no = $("#adhar_no").val();
        var mobile_no = $("#mobile_no").val();
        var job_role = $("#job_role").val();
        var address = $("#address").val();
        // if(first_name == "" || last_name == "" || address == "" || username == ""){
        //     alert("Please complete field");
        // }else{
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            Swal.fire({
                title: "Are you sure you want to update?",
                text:"",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Yes",
                cancelButtonText: "No"
            }).then(function(result) {
                if (result.value) {

                      $.ajax({
                      url: 'admin_user_update',
                    method :'POST',
                    headers: {'X-CSRFToken': csrftoken},
                     data: {
                        id: id,
                        password:password,
                        emp_id: emp_id,
                        username: username,
                        first_name: first_name,
                        last_name: last_name,
                        dob: dob,
                        official_email_id: official_email_id,
                        personal_email_id: personal_email_id,
                        adhar_no: adhar_no,
                        mobile_no: mobile_no,
                        job_role:job_role,
                        address:address,
                     },
                    success: function (dataResult) {
                        // if (dataResult === 'no'){

                            Swal.fire({
                                position: "center",
                                icon: "success",
                                title: "User details has been updated...!",
                                showConfirmButton: false,
                                timer: 1500
                            }).then(function (){
                               location.reload();
                            });

                    }
                });

            } else if (result.dismiss === "cancel") {
                 Swal.fire({
                     position: "center",
                     icon: "error",
                     title: "User Details Not updated :)",
                     showConfirmButton: false,
                     timer: 1500
                 });
            }
        });


        });
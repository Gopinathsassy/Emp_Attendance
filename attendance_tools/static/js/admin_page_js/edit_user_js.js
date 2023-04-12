$(document).on('click', '#admin_edit_user_details', function(){
    $id = $(this).attr("name");
    window.location = "admin_edit_user_profile/" + $id;
});




$('#admin_editdfs').on('click', function(){
        var id = $("#id").val();
         var password = $("#password").val();
        var emp_id = $("#emp_id").val();
        var username = $("#username").val();
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var blood_group = $("#blood_group").val();
        var dob = $("#dob").val();
        var module = $("#module").val();
        var gender = $("#gender").val();
        var official_email_id = $("#official_email_id").val();
        var personal_email_id = $("#personal_email_id").val();
        var adhar_no = $("#adhar_no").val();
        var mobile_no = $("#mobile_no").val();
        var job_role = $("#job_role").val();
        var address = $("#address").val();
        var acc_no = $("#acc_no").val();
        var ifsc_code = $("#ifsc_code").val();
        var branch = $("#branch").val();

        console.log(password)
        console.log(emp_id)
        console.log(username)
        console.log(first_name)
        console.log(last_name)
        console.log(blood_group)
        console.log(dob)
        console.log(module)
        console.log(gender)
        console.log(official_email_id)
        console.log(personal_email_id)
        console.log(adhar_no)
        console.log(mobile_no)
        console.log(job_role)
        console.log(address)
        console.log(acc_no)
        console.log(ifsc_code)
        console.log(branch)

        // if(first_name == "" || last_name == "" || address == "" || username == ""){
    alert(id);
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
                      url: "{% url 'admin_user_update_details' %}",
                    method :'POST',
                    headers: {'X-CSRFToken': csrftoken},
                     data: {
                        id: id,
                        password:password,
                        emp_id: emp_id,
                        username: username,
                        first_name: first_name,
                        last_name: last_name,
                        blood_group:blood_group,
                        dob: dob,
                        module:module,
                        gender: gender,
                        official_email_id: official_email_id,
                        personal_email_id: personal_email_id,
                        adhar_no: adhar_no,
                        mobile_no: mobile_no,
                        job_role:job_role,
                        address:address,
                        acc_no:acc_no,
                        ifsc_code:ifsc_code,
                        branch:branch
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
                     title: "User Not updated :)",
                     showConfirmButton: false,
                     timer: 1500
                 });
            }
        });


        });
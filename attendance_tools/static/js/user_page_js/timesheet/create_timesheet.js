
$(document).ready(function (){
   $(document).on("change", "#project_name", function (){
        var jobname = $(this).find("option:selected").data("jobname");
        $("#job_name").val(jobname);
        alert(jobname);
   });
});

        $("#timesheet_submit").click(function (event) {
                event.preventDefault();

                var project_name = $("#project_name").val();
                var project_code = $("#project_name").find("option:selected").data("projectcode");
                var job_name = $("#project_name").find("option:selected").data("jobname");
                var date = $("#date").val();
                var total_hours = $("#total_hours").val();
                var description = $("#description").val();


                 console.log(project_name);
                 console.log(job_name);
                 console.log(date);
                 console.log(total_hours);
                 console.log(description);
                if (project_name == "" || job_name == "" || date == "" || total_hours == "" ||  description == "") {
                 alert("Fill the all fields");
                }
                // Get form
                else{
                var form = $('#pic')[0];
                console.log(form);

                // Create an FormData object
                var data = new FormData(form);
                    console.log(data);
             $.ajax({
                 type: "POST",
                 url: "timesheet_create",
                 enctype: 'multipart/form-data',
                 data: data,
                    processData: false,
                    contentType: false,
                    cache: false,

                 success: function (html) {
                     alert(html);
                     Swal.fire({
                         title: "Success",
                         text: "Done",
                         icon: "success",
                         showConfirmButton: false,
                         timer: 800
                     }).then(function () {
                         location.reload();
                     });
                     $("#create").removeAttr("disabled", "disabled");
                 },
                 error: function (){
                     alert("error");
                 }
             });
         }

});

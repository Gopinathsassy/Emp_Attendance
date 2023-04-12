
$(document).ready(function (){
   $(document).on("change", "#project_name", function (){
        var jobname = $(this).find("option:selected").data("jobname");
        var projectcode = $(this).find("option:selected").data("projectcode");
        $("#job_name").val(jobname);
        $("#project_code").val(projectcode);
   });

//     $("#edit_timesheet_final").click(function (event) {
//                 event.preventDefault();
//
//                 var id = $("#id").val();
//                 // var project_name = $("#project_name").val();
//                 // var project_code = $("#project_name").find("option:selected").data("projectcode");
//                 // var job_name = $("#project_name").find("option:selected").data("jobname");
//                 // var date = $("#date").val();
//                 // var total_hours = $("#total_hours").val();
//                 // var description = $("#description").val();
//
//                 if (project_name == "" || job_name == "" || date == "" || total_hours == "" ||  description == "") {
//                  alert("Fill the all fields");
//                 }
//                 // Get form
//                 else{
//                 var form = $('#pic')[0];
//                 // console.log(form);
//
//                 // Create an FormData object
//                 var data = new FormData(form);
//                     // console.log(data);
//              $.ajax({/
//                  type: "POST",
//                  url: 'timesheet_edit_values/' + id,
//                  enctype: 'multipart/form-data',
//                  data: data,
//
//                  success: function () {
//                      Swal.fire({
//                          title: "Success",
//                          text: "Done",
//                          icon: "success",
//                          showConfirmButton: false,
//                          timer: 800
//                      }).then(function () {
//                          location.reload();
//                      });
//                      // $("#create").removeAttr("disabled", "disabled");
//                  },
//                  error: function (){
//                       alert("error!");
//                  }
//              });
//          }
//
// });
});



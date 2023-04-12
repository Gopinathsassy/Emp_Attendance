$(document).on('click', '#delete_timesheet', function(){
    $id = $(this).attr('value');
    window.location = "timesheet_edit_page/" + $id;
    alert($id);
});

$(function() {
  //check_all checked then check all table rows
   $("#check_all").on("click", function () {
      if ($("input:checkbox").prop("checked")) {
         $("input:checkbox[name='row-check']").prop("checked", true);
      } else {
         $("input:checkbox[name='row-check']").prop("checked", false);
      }
   });
  // Check each table row checkbox
   $("input:checkbox[name='row-check']").on("change", function () {
      var total_check_boxes = $("input:checkbox[name='row-check']").length;
      var total_checked_boxes = $("input:checkbox[name='row-check']:checked").length;


      if (total_check_boxes === total_checked_boxes) {
         $("#check_all").prop("checked", true);
      }
      else {
         $("#check_all").prop("checked", false);
      }
   });
});

$(document).ready(function (){
   $(document).on('click', "#sent_admin", function() {

       var id = [];
       var project_name_code = [];
       var job_name = [];
       var task_name = [];
       var hours = [];
       var date = [];
       var description = [];
       var statuss = [];

       $(":checkbox:checked").closest("td").each(function (){
        id.push($(this).find('.id').val());
        });

       $(":checkbox:checked").closest("td").each(function () {
           project_name_code.push($(this).find('.project_name_code').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           job_name.push($(this).find('.job_name').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           task_name.push($(this).find('.task_name').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           hours.push($(this).find('.hours').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           date.push($(this).find('.date').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           description.push($(this).find('.description').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           statuss.push($(this).find('.status').html());
       });

       $.ajax({
           url: 'timesheet_sent_toadmin',
           method: 'POST',
           headers: {
               "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
           },
           data: {

               id:id,
               project_name_code: project_name_code,
               job_name: job_name,
               task_name: task_name,
               hours: hours,
               date:date,
               description:description,
               statuss:statuss
           },

           success: function (value) {
               alert(value);
               Swal.fire({
                   title: "Success",
                   text: "Done!",
                   icon: "success",
                   showConfirmButton: false,
                   timer: 1500
               }).then(function () {
                   location.reload();
               });
           }
       });
   });
});


$(document).ready(function (){
   $(document).on('click', "#delete_timesheet", function() {

       var id = [];
       var project_name_code = [];
       var job_name = [];
       var task_name = [];
       var hours = [];
       var date = [];
       var description = [];
       var statuss = [];


       $(":checkbox:checked").closest("td").each(function (){
        id.push($(this).find('.id').val());
        });

       $(":checkbox:checked").closest("td").each(function () {
           project_name_code.push($(this).find('.project_name_code').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           job_name.push($(this).find('.job_name').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           task_name.push($(this).find('.task_name').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           hours.push($(this).find('.hours').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           date.push($(this).find('.date').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           description.push($(this).find('.description').html());
       });
       $(":checkbox:checked").closest("td").each(function () {
           statuss.push($(this).find('.status').html());
       });

       $.ajax({
           url: 'timesheet_delete',
           method: 'POST',
           headers: {
               "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
           },
           data: {

               id:id,
               project_name_code: project_name_code,
               job_name: job_name,
               task_name: task_name,
               hours: hours,
               date:date,
               description:description,
               statuss:statuss
           },
           success: function (value) {
               alert(value);
               Swal.fire({
                   title: "Success",
                   text: "Done!",
                   icon: "success",
                   showConfirmButton: false,
                   timer: 1500
               }).then(function () {
                   location.reload();
               });
           }
       });
   });
});




 $(document).on('click','#delete_leave_request',function() {

                        var id = $(this).data("value");
                        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
// alert(id)
                    Swal.fire({
                        title: "Are you sure you want to Remove?",
                        text:"",
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonText: "Yes",
                        cancelButtonText: "No"
                    }).then(function(result) {
                        if (result.value) {

                                  $.ajax({
                                  url: "{% url 'delete_leave_request' %}",
            	                method :'POST',
            	                headers: {'X-CSRFToken': csrftoken},
                                 data: {
                                     'id': id,
                                 },
                                success: function (dataResult) {
                                    // if (dataResult === 'no'){

                                        Swal.fire({
                                            position: "center",
                                            icon: "success",
                                            title: "User has been Removed...!",
                                            showConfirmButton: false,
                                            timer: 1500
                                        }).then(function (){
                                           window.location.href="{%  url 'leave_apply_table' %}"
                                        });

                                }
                            });

                        } else if (result.dismiss === "cancel") {
                             Swal.fire({
                                 position: "center",
                                 icon: "error",
                                 title: "User Not Removed :)",
                                 showConfirmButton: false,
                                 timer: 1500
                             });
                        }
                    });


                });
 $(document).on('click','#admin_delete_user',function() {

                        var id = $(this).data("value");
                        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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
                                  url: 'admin_delete_user',
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
                                           location.reload();
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
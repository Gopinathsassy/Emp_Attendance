
$(document).on('click', '#user_profile', function(){
        $id = $(this).attr("name");
        window.location = 'user_profile_page/' + $id;
    });

$(document).ready(function() {
        $("#user_profilea").click(function () {
             var id = $(this).attr("name");
            alert(id)
            $.ajax({
                type: 'POST',
                url: "user_profile_page",
                data:{
                    id: id,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function (html) {
                    // alert(html);
                },
                error:function (){
                    // alert("error");
                }
            });
        });
     });



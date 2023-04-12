
$(document).ready(function () {
$(document).on("click", "#update_position", function (){
alert("haiiii");

var user_name = $(this).data('user');

alert(user_name);

});
});

    $('#exampleModalCenter_project').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var myid = button.data('myid');
        var pname = button.data('pname');
        var pcode = button.data('pcode');
        var pcode1 = button.data('ptype');
        var pcode2 = button.data('psp');
        var pcode3 = button.data('cname');
        var pcode4 = button.data('cloc');
        var modal = $(this);
        modal.find('.modal-body #myid').val(myid);
        modal.find('.modal-body #pname').val(pname);
        modal.find('.modal-body #pcode').val(pcode);
        modal.find('.modal-body #ptype').val(pcode1);
        modal.find('.modal-body #psp').val(pcode2);
        modal.find('.modal-body #cname').val(pcode3);
        modal.find('.modal-body #cloc').val(pcode4);
    })

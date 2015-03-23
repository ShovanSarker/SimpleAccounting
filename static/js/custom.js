/**
 * Created by shovan on 3/23/15.
 */
$(document).ready(function(){
    var modalMsg = '';

    $('#btnReciveMoney').click(function(e){
        //e.preventDefault();
        //$('#modalRecieveMoney').modal('show');
        var rcvFrmName = $('#rcvFrmName').val();
        var rcvFrmPurpose = $('#rcvFrmPurpose').val();
        var rcvFrmAmount = $('#rcvFrmAmount').val();
        var rcvFrmType = $('#rcvFrmType').val();
        var rcvFrmLoan = $('#rcvFrmLoan').val();
        var rcvFrmNextDate = $('#rcvFrmNextDate').val();
        var rcvFrmRemarks = $('#rcvFrmRemarks').val();
        var validationError = false;
        if (rcvFrmName == '' || rcvFrmPurpose == '' || rcvFrmAmount == '' || isNaN(rcvFrmAmount)){
            validationError = true;
        }
        if (validationError){
            modalMsg = '<div class="alert alert-danger">Please Check your information</div>';
        }else{
            modalMsg = '<div class="alert alert-success"><p>' + 'Name : ' + rcvFrmName + '</br>Purpose : ' + rcvFrmPurpose + '</br>Amount : ' + rcvFrmAmount  +'</p></div>';
            $('#modalRecieveMoney').modal('show');
            e.preventDefault();
        }
    });


    $('#modalRecieveMoney').on('show.bs.modal', function(event){
        var modal = $(this);
        modal.find('.modal-body .col-md-12').html(modalMsg);
    });
});
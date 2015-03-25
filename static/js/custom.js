/**
 * Created by shovan on 3/23/15.
 */
$(document).ready(function(){
    var modalMsg = '';
    var modalFoot = '';

    $('#btnReciveMoney').click(function(e){
        var rcvFrmName = $('#rcvFrmName').val();
        var rcvFrmPurpose = $('#rcvFrmPurpose').val();
        var rcvFrmAmount = $('#rcvFrmAmount').val();
        var rcvFrmType = $('#rcvFrmType').val();
        if (rcvFrmType == 'cash'){
            rcvFrmType = 'Cash';
        }else{
            rcvFrmType = 'Bank';
        }
        var rcvFrmLoan = '';
        if ($('#rcvFrmLoan').is(":checked")){
            rcvFrmLoan = 'YES';
        }else{
            rcvFrmLoan = 'NO';
        }
        var rcvFrmNextDate = $('#rcvFrmNextDate').val();
        if (rcvFrmNextDate == ''){
            rcvFrmNextDate = 'Not Applicable';
        }
        var rcvFrmRemarks = $('#rcvFrmRemarks').val();
        if (rcvFrmRemarks == ''){
            rcvFrmRemarks = 'Not Applicable';
        }
        var validationError = false;
        if (rcvFrmName == '' || rcvFrmPurpose == '' || rcvFrmAmount == '' || isNaN(rcvFrmAmount)){
            validationError = true;
        }
        if (validationError){
            modalMsg = '<div class="alert alert-danger">Please Check your information</div>';
        }else{
            modalMsg = '<div class="alert alert-success"><p>' + 'Receive From : ' + rcvFrmName + '</br>Purpose : ' + rcvFrmPurpose + '</br>Amount : ' + rcvFrmAmount  + '</br>Type : ' + rcvFrmType + '</br>Is it a loan ? : ' + rcvFrmLoan + '</br>Possible Date of return : ' + rcvFrmNextDate + '</br>Remarks : ' + rcvFrmRemarks + '</p></div>';
            modalFoot = '<button type="button" class="btn btn-primary btn-submit" id="btnMoneyRevConfirm">Ok</button><button type="button" class="btn btn-primary btn-submit" data-dismiss="modal">Cancel</button>'
            $('#modalRecieveMoney').modal('show');
            e.preventDefault();
        }
    });

    $('#btnPayMoney').click(function(e){
        var payFrmName = $('#payFrmName').val();
        var payFrmPurpose = $('#payFrmPurpose').val();
        var payFrmAmount = $('#payFrmAmount').val();
        var payFrmType = $('#payFrmType').val();
        if (payFrmType == 'cash'){
            payFrmType = 'Cash';
        }else{
            payFrmType = 'Bank';
        }
        var payFrmLoan = '';
        if ($('#payFrmLoan').is(":checked")){
            payFrmLoan = 'YES';
        }else{
            payFrmLoan = 'NO';
        }
        var payFrmNextDate = $('#payFrmNextDate').val();
        if (payFrmNextDate == ''){
            payFrmNextDate = 'Not Applicable';
        }
        var payFrmRemarks = $('#payFrmRemarks').val();
        if (payFrmRemarks == ''){
            payFrmRemarks = 'Not Applicable';
        }
        var validationError = false;
        if (payFrmName == '' || payFrmPurpose == '' || payFrmAmount == '' || isNaN(payFrmAmount)){
            validationError = true;
        }
        if (validationError){
            modalMsg = '<div class="alert alert-danger">Please Check your information</div>';
        }else{
            modalMsg = '<div class="alert alert-success"><p>' + 'Pay To : ' + payFrmName + '</br>Purpose : ' + payFrmPurpose + '</br>Amount : ' + payFrmAmount  + '</br>Type : ' + payFrmType + '</br>Is it a loan ? : ' + payFrmLoan + '</br>Possible Date of return : ' + payFrmNextDate + '</br>Remarks : ' + payFrmRemarks + '</p></div>';
            modalFoot = '<button type="button" class="btn btn-primary btn-submit" id="btnMoneyPayConfirm">Ok</button><button type="button" class="btn btn-primary btn-submit" data-dismiss="modal">Cancel</button>'
            $('#modalRecieveMoney').modal('show');
            e.preventDefault();
        }
    });


    $( "#modalSubmitBtn" ).on( "click", "#btnMoneyRevConfirm", function() {
        $('#modalRecieveMoney').modal('hide');
        $( "#formRevieveMoney" ).submit();
    });

    $( "#modalSubmitBtn" ).on( "click", "#btnMoneyPayConfirm", function() {
        $('#modalRecieveMoney').modal('hide');
        $( "#formPayMoney" ).submit();
    });

    //$('#btnMoneyRevConfirm').click(function(){
    //    $('#modalRecieveMoney').modal('hide');
    //    $( "#formRevieveMoney" ).submit();
    //});

    //$('#btnMoneyPayConfirm').click(function(){
    //    $('#modalRecieveMoney').modal('hide');
    //    $( "#formPayMoney" ).submit();
    //});
    $('#modalRecieveMoney').on('show.bs.modal', function(event){
        var modal = $(this);
        modal.find('.modal-body .col-md-12').html(modalMsg);
        modal.find('#modalSubmitBtn').html(modalFoot);
    });


    //var maxRows = 10;
    //$('.paginated-table').each(function() {
    //    var cTable = $(this);
    //    var cRows = cTable.find('tr:gt(0)');
    //    var cRowCount = cRows.size();
    //
    //    if (cRowCount < maxRows) {
    //        return;
    //    }
    //
    //    /* add numbers to the rows for visuals on the demo */
    //    cRows.each(function(i) {
    //        $(this).find('td:first').text(function(j, val) {
    //            return (i + 1) + "" + val;
    //        });
    //    });
    //
    //    /* hide all rows above the max initially */
    //    cRows.filter(':gt(' + (maxRows - 1) + ')').hide();
    //
    //    //var cPrev = cTable.siblings('nav ul li .prevBtn');
    //    //var cNext = cTable.siblings('nav ul li .nextBtn');
    //    var cPrev = $('.paginator ul li .prevBtn');
    //    var cNext = $('.paginator ul li .nextBtn');
    //
    //    /* start with previous disabled */
    //    cPrev.addClass('disabled');
    //
    //    cPrev.click(function() {
    //        var cFirstVisible = cRows.index(cRows.filter(':visible'));
    //
    //        if (cPrev.hasClass('disabled')) {
    //            return false;
    //        }
    //
    //        cRows.hide();
    //        if (cFirstVisible - maxRows - 1 > 0) {
    //            cRows.filter(':lt(' + cFirstVisible + '):gt(' + (cFirstVisible - maxRows - 1) + ')').show();
    //        } else {
    //            cRows.filter(':lt(' + cFirstVisible + ')').show();
    //        }
    //
    //        if (cFirstVisible - maxRows <= 0) {
    //            cPrev.addClass('disabled');
    //        }
    //
    //        cNext.removeClass('disabled');
    //
    //        return false;
    //    });
    //
    //    cNext.click(function() {
    //        var cFirstVisible = cRows.index(cRows.filter(':visible'));
    //
    //        if (cNext.hasClass('disabled')) {
    //            return false;
    //        }
    //
    //        cRows.hide();
    //        cRows.filter(':lt(' + (cFirstVisible +2 * maxRows) + '):gt(' + (cFirstVisible + maxRows - 1) + ')').show();
    //
    //        if (cFirstVisible + 2 * maxRows >= cRows.size()) {
    //            cNext.addClass('disabled');
    //        }
    //
    //        cPrev.removeClass('disabled');
    //
    //        return false;
    //    });
    //
    //});

});
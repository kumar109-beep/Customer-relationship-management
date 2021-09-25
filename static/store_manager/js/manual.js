function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function onlyNumberKey(e) {
    var x = e.which || e.keycode;
    if ((x >= 48 && x <= 57))
        return true;
    else
        return false;
}
function AvoidSpace(event) {
    var k = event ? event.which : window.event.keyCode;
    if (k == 32) return false;
}

function searchContact(txt) {
    var text = txt.value;
    document.getElementById('search_contact').style.border = '';
    document.getElementById('invalidContact').innerHTML = '';
    if (text == '') {
        document.getElementById('save_btn').disabled = true;
        document.getElementById('search_contact').style.border = '1px solid red';
        // document.getElementById('invalidContact').innerHTML = 'Only numbers allowed starting with 6,7,8,9';
    } else {
        // var regx = /^[6-9]\d{9}$/;
        // if (text.match(regx)) {
            document.getElementById('search_contact').style.border = '';
            document.getElementById('invalidContact').innerHTML = '';
            document.getElementById('save_btn').disabled = false;
            $('#TitleCustomer').html("");
            $('#customerName').val("");
            $('#customerEmail').val("");
            $('#custDOB').val("");
            $('#custDOM').val("");
            $("input[name='CustomerGender']").prop("checked", false);
            var contact = document.getElementById('search_contact').value;
            const csrftoken = getCookie('csrftoken');
            $.ajax({
                type: 'POST',
                url: "checkExistCustomer",
                headers: { 'X-CSRFToken': csrftoken },
                data: { "ContactNumber": contact },
                success: function (response) {
                    var flagHide = contact.length === 10 ? true : false;
                    flagHide === true ? $("#SetOpacity").css({ 'pointer-events': 'auto', 'opacity': '1' }) : $("#SetOpacity").css({ 'pointer-events': 'none', 'opacity': '.3' });
                    if (response.length === 1 && flagHide) {
                        $('#TitleCustomer').html("Old Customer &nbsp;&nbsp;&nbsp;   <button type='button' class='btn btn-primary btn-sm' onclick='customer_detailed_info()'>Customer History&nbsp;&nbsp;&nbsp;&nbsp;<i class='fas fa-history'></i></button>");
                        
                        for (var key in response) {
                            $('#customerName').val(response[key]['name']);
                            $('#customerEmail').val(response[key]['email']);
                            $('#custDOB').val(response[key]['DOB']);
                            $('#custDOM').val(response[key]['DOM']);

                            console.log(response[0]['gender'])
                            if (response[0]['gender'] == 'NA') {
                                $("#Customer_male").prop("checked", false);
                                $("#Customer_female").prop("checked", false);
                            } else if (response[0]['gender'] == 'M' || response[0]['gender'] == 'm' || response[0]['gender'] == 'MALE' || response[0]['gender'] == 'Male') {
                                $("#Customer_male").prop("checked", true);
                            } else if (response[0]['gender'] == 'F' || response[0]['gender'] == 'f' || response[0]['gender'] == 'FEMALE' || response[0]['gender'] == 'Female') {
                                $("#Customer_female").prop("checked", true);
                            }
                        }
                    } else if (contact.length === 10 && response.length === 0) {
                        $('#TitleCustomer').html("New Customer &nbsp;&nbsp;&nbsp;   <button type='button' class='btn btn-primary btn-sm' onclick='customer_detailed_info()'>Customer History&nbsp;&nbsp;&nbsp;&nbsp;<i class='fas fa-history'></i></button>");
                    }
                }
            })
        } 
        if ((text.length != 10)) {
            document.getElementById('save_btn').disabled = true;
            document.getElementById('search_contact').style.border = '1px solid red';
            document.getElementById('invalidContact').innerHTML = 'Contact must be 10 of digits';

        }
        // else {
        //     document.getElementById('save_btn').disabled = true;
        //     document.getElementById('search_contact').style.border = '1px solid red';
        //     document.getElementById('invalidContact').innerHTML = 'Contact contains numbers only and starts with 6,7,8,9';

        // }
    }
// }





function searchInvoice() {
    var InVoiceNumber = document.getElementById('InvoiceNumber').value;
    var MobileNumber = document.getElementById('search_contact').value;
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url: "checkExistInVoiceNo",
        headers: { 'X-CSRFToken': csrftoken },
        data: { "InVoiceNumber": InVoiceNumber, "MobileNumber": MobileNumber },
        success: function (response) {
            if (response === 'True') {
                for (var key in response) {
                    $("#CheckInvoice").css({ 'color': 'red' });
                    document.getElementById('save_btn').disabled = true;
                }
            } else {
                $("#CheckInvoice").css({ 'color': '' });
                document.getElementById('save_btn').disabled = false;
            }
        }
    })

}


$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: "NewInVoiceNogenrate",
        success: function (response) {
            if (response['invoice'].length > 0) {
                var incoNum = response['invoice'].split(/(\d+)/);
                var noInVO = parseInt(incoNum[1]) + 1;
                var strInVO = incoNum[0] + noInVO.toString();
                $('#InvoiceNumber').val(strInVO);
            } else {
                console.log('B')
            }
        }
    })
});


function validateName(txt) {
    var text = txt.value;
    var regx = /^[a-zA-Z._' ']+$/;
    document.getElementById('customerName').style.border = '';
    document.getElementById('invalidContact').innerHTML = '';
    if (text == '') {
        document.getElementById('save_btn').disabled = true;
        document.getElementById('customerName').style.border = '1px solid red';
        document.getElementById('invalidName').innerHTML = 'Only alphabets allowed';
    } else {
        if (text.match(regx)) {
            document.getElementById('customerName').style.border = '';
            document.getElementById('invalidName').innerHTML = '';
            document.getElementById('save_btn').disabled = false;
        } else {
            document.getElementById('customerName').style.border = '1px solid red';
            document.getElementById('invalidName').innerHTML = 'Only alphabets allowed';
            document.getElementById('save_btn').disabled = true;
        }
    }
}


function validateEmail(txt) {
    var emailData = txt.value;
    var regx = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.]{2,5})+\.([A-Za-z]{2,5})$/;
    if (emailData == '') {
        document.getElementById('save_btn').disabled = true;
        document.getElementById('customerEmail').style.border = '1px solid red';
        document.getElementById('invalidEmail').innerHTML = 'Invalid Email';
    } else {
        if (emailData.match(regx)) {
            document.getElementById('customerEmail').style.border = '';
            document.getElementById('invalidEmail').innerHTML = '';
            document.getElementById('save_btn').disabled = false;
        }
        else {
            document.getElementById('customerEmail').style.border = '1px solid red';
            document.getElementById('invalidEmail').innerHTML = 'Invalid Email';
        }
    }
}


function onlyNumberKey(e) {
    var x = e.which || e.keycode;
    if ((x >= 48 && x <= 57))
        return true;
    else
        return false;
}
function AvoidSpace(event) {
    var k = event ? event.which : window.event.keyCode;
    if (k == 32) return false;
}


function validateAmt(txt) {
    var amtData = parseInt(txt.value);
    // var pattern = /^(\$|)([1-9]\d{0,2}(\,\d{3})*|([1-9]\d*))(\.\d{2})?$/;
    if (amtData == 0) {
        document.getElementById('amount').style.border = '1px solid red';
        document.getElementById('save_btn').disabled = true;
    } else if (amtData.length == 0){
        document.getElementById('amount').style.border = '1px solid red';
        document.getElementById('save_btn').disabled = true;
    } else {
        // if (amtData.match(pattern)) {
            document.getElementById('amount').style.border = '';
            document.getElementById('save_btn').disabled = false;
        // }
    }
}
// ##################################  MANUAL ENTRY USING AJAX  ######################################################
function manualentryAjax() {
    var contact = $('#search_contact').val();
    var invoice = $('#InvoiceNumber').val();
    var name = $('#customerName').val();
    // var gender = $("input[name='CustomerGender']").val();
    var gender = document.getElementsByName('CustomerGender');
    var getGender = '';

    for (i = 0; i < gender.length; i++) {
        if (gender[i].checked){
            getGender = gender[i].value;
        }
            
    } 
    // alert(getGender);
    // return false;
    var DOB = $('#custDOB').val();
    var DOM = $('#custDOM').val();
    var email = $('#customerEmail').val();
    var amount = $('#amount').val();

    // return false;
    
    const csrftoken = getCookie('csrftoken');
    if(amount == ''){
        Swal.fire('Enter shopping amount!');
        return false;
    }else if(amount == '' || contact == '' || invoice == ''){
        Swal.fire('Enter the essential fields(*) data!');
        return false;
    }else{
        if(getGender.length == 0){
            getGender = 'Female';
        }else{
            getGender = 'Male';
        }
        console.log('contact : ', contact, 'invoice : ', invoice, 'name : ', name, 'gender : ', getGender, 'DOB : ', DOB, 'DOM : ', DOM, 'email : ', email, 'amount : ', amount);
        swal.showLoading();
        $.ajax({
            type: 'POST',
            url: "manualEntryData",
            headers: { 'X-CSRFToken': csrftoken },
            data: { 'contact': contact, 'invoice': invoice, 'name': name, 'gender': getGender, 'DOB': DOB, 'DOM': DOM, 'email': email, 'amount': amount },
            success: function (response) {
                console.log(response);
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Entry saved successfully',
                    showConfirmButton: true,
                })
                var contact = $('#search_contact').val("");
                var name = $('#customerName').val("");
                var gender = $("input[name='CustomerGender']").val("");
                var DOB = $('#custDOB').val("");
                var DOM = $('#custDOM').val("");
                var email = $('#customerEmail').val("");
                var amount = $('#amount').val("");
                $.ajax({
                    type: 'GET',
                    url: "NewInVoiceNogenrate",
                    success: function (response) {
                        getGender = '';
                        $("#SetOpacity").css({ 'pointer-events': 'auto', 'opacity': '0.3' });

                        if (response['invoice'].length > 0) {
                            var incoNum = response['invoice'].split(/(\d+)/);
                            var noInVO = parseInt(incoNum[1]) + 1;
                            var strInVO = incoNum[0] + noInVO.toString();
                            $('#InvoiceNumber').val(strInVO);
                        }
                    }
                })
            }
        })
    }
}

// =========================================================    VALIDATE DOB   ==================================================
function validatDob(){
    dobData = $('#custDOB').val();
    console.log(dobData);
    var pattern = /^([0-9]{2})\/([0-9]{2})\/([0-9]{4})$/;

    if (dobData == "") {
        document.getElementById('custDOB').style.border = '1px solid red';
        document.getElementById('save_btn').disabled = true;
    } else {
        if (dobData.match(pattern)) {
            console.log('A');
            document.getElementById('custDOB').style.border = '';
            document.getElementById('save_btn').disabled = false;
            $('#invalidDOB').html('');
        }else{
            console.log('B');
            document.getElementById('custDOB').style.border = '1px solid red';
            document.getElementById('save_btn').disabled = true;
            $('#invalidDOB').html('DOB format should be mm/dd/yyyy');
 
        }
    }
}

// =========================================================    VALIDATE DOM   ==================================================
function validatDom() {
    domData = $('#custDOM').val();
    console.log(domData);
    var pattern = /^([0-9]{2})\/([0-9]{2})$/;

    if (domData == "") {
        document.getElementById('custDOM').style.border = '1px solid red';
        document.getElementById('save_btn').disabled = true;
    } else {
        if (domData.match(pattern)) {
            console.log('A');
            document.getElementById('custDOM').style.border = '';
            document.getElementById('save_btn').disabled = false;
            $('#invalidDOM').html('');
        } else {
            console.log('B');
            document.getElementById('custDOM').style.border = '1px solid red';
            document.getElementById('save_btn').disabled = true;
            $('#invalidDOM').html('DOM format should be dd/mm');

        }
    }
}
// ==============================================================================================================================================
function customer_detailed_info() {
    var search_contact = $('#search_contact').val().trim();
    $('#myModal').modal('show');

    $('#tierInfoData').html("");
    $('#noDataAvailable').css('display', 'none');
    $('#autofillbtn').prop('disabled', false);
    $('#autofillbtn').css('cursor', '');


    $.ajax({
        type: 'GET',
        url: "customer_history_info",
        data: { 'search_contact': search_contact },
        success: function (response) {
            console.log('customer deatiled info : ', response);
            // return false;
            // ------------------------------------------------------------------------
            if (response[0]['name'] == "" & response[0]['email'] == "" & response[0]['DOB'] == "") {
                $('#customer_info_name').val('Customer');
                $('#customer_info_contact').val(response[0]['contact']);
                $('#customer_info_email').val('NA');
                $('#customer_info_dob').val('NA');
                $('#customer_info_dom').val(response[0]['DOM']);
                $('#customer_info_gender').attr('checked', 'checked');
            } else if (response[0]['name'] == "" & response[0]['email'] == "") {
                $('#customer_info_name').val('Customer');
                $('#customer_info_contact').val(response[0]['contact']);
                $('#customer_info_email').val('NA');
                $('#customer_info_dob').val(response[0]['DOB']);
                $('#customer_info_dom').val(response[0]['DOM']);
                $('#customer_info_gender').attr('checked', 'checked');
            } else if (response[0]['email'] == "" & response[0]['DOB'] == "") {
                $('#customer_info_name').val(response[0]['name']);
                $('#customer_info_contact').val(response[0]['contact']);
                $('#customer_info_email').val('NA');
                $('#customer_info_dob').val('NA');
                $('#customer_info_dom').val(response[0]['DOM']);
                $('#customer_info_gender').attr('checked', 'checked');
            } else if (response[0]['name'] == "" & response[0]['DOB'] == "") {
                $('#customer_info_name').val('Customer');
                $('#customer_info_contact').val(response[0]['contact']);
                $('#customer_info_email').val(response[0]['email']);
                $('#customer_info_dob').val('NA');
                $('#customer_info_dom').val(response[0]['DOM']);
                $('#customer_info_gender').attr('checked', 'checked');
            } else {
                $('#customer_info_name').val(response[0]['name']);
                $('#customer_info_contact').val(response[0]['contact']);
                $('#customer_info_email').val(response[0]['email']);
                $('#customer_info_dob').val(response[0]['DOB']);
                $('#customer_info_dom').val(response[0]['DOM']);
                $('#customer_info_gender').attr('checked', 'checked');
            }
            if (response[1].length == 0) {
                $('#autofillbtn').prop('disabled',true);
                $('#autofillbtn').css('cursor', 'not-allowed');
                $('#tierInfoData').html("");
                $('#noDataAvailable').css('display','');

                $('#customer_info_name').val('New Customer');
                $('#customer_info_contact').val('NA');
                $('#customer_info_email').val('NA');
                $('#customer_info_dob').val('NA');
                $('#customer_info_dom').val('NA');
                $('#customer_info_gender').attr('checked', '');
            }
            // ------------------------------------------------------------------------
            if (response[5].length == 0 && response[6].length == 0 && response[7].length == 0) {
                for (var i = 0; i < response[1].length; i++) {
                    var tierDet = response[3][i] == "NA" ? "NA" : "Tier-" + response[3][i];
                    $('#tierInfoData').append("<tr>\
                        <td><b>"+ response[1][i] + "</b></td>\
                         <td>"+ response[2][i]['storeID'] + "</td>\
                        <td>"+ parseInt(response[2][i]['amount']) + "</td>\
                        <td>"+ tierDet + "</td>\
                        </tr>");
                }
            } else {
                for (var i = 0; i < response[1].length; i++) {
                    var tierDet = response[3][i] == "NA" ? "NA" : "Tier-" + response[3][i];
                    $('#tierInfoData').append("<tr>\
                        <td><b>"+ response[1][i] + "</b></td>\
                         <td>"+ response[2][i]['storeID'] + "</td>\
                        <td>"+ parseInt(response[2][i]['amount']) + "</td>\
                        <td>"+ tierDet + "</td>\
                        </tr>");
                }

                for (var i = 0; i < response[5].length; i++) {
                    var tierDet = response[7][i] == "NA" ? "NA" : "Tier-" + response[7][i];
                    $('#tierInfoData').append("<tr>\
                        <td><b>"+ response[5][i] + "</b><small><strong>&nbsp;- (Onboard Entry Customer)</strong></small></td>\
                         <td>"+ response[6][i]['storeID'] + "</td>\
                        <td>"+ parseInt(response[6][i]['amount']) + "</td>\
                        <td>"+ tierDet + "</td>\
                        </tr>");
                }
            }
            // --------------------------------------------------------------------------
        }
    });
}
// ================================================================================================================
function autoFill(){
    var custName = $('#customer_info_name').val().trim();
    var custDob = $('#customer_info_dob').val().trim();
    var custDom = $('#customer_info_dom').val().trim();
    var custEmail = $('#customer_info_email').val().trim();

    if (custName != 'NA') {
        $('#customerName').val(custName);
    } if (custDob != 'NA') {
        $('#custDOB').val(custDob);
    } if (custDom != 'NA') {
        $('#custDOM').val(custDom);
    } if (custEmail != 'NA') {
        $('#customerEmail').val(custEmail);
    }

    $('#myModal').modal('hide');


}
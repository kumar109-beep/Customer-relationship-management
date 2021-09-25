function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// =====================================================================================================
// =====================================================================================================
// =====================================================================================================
function generateAmountOfPurchaseReport(){
    var storeArray = $('#kt_select2_3').val();
    console.log('store array : ',storeArray);

    var dateRange = $('#kt_daterangepicker_1').val();
    console.log('dateRange : ',dateRange);

    if(storeArray.length == 0){
        alert('Select atleast 1 store to continue!');
        return false;
    }
    if(dateRange.length == 0){
        alert('Select date range to continue!');
        return false;
    }
    // ------------------------------------------
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url: "/customer-reports/amount-of-purchase",
        headers: { 'X-CSRFToken': csrftoken },
        data: { 'storeArray[]': storeArray, 'dateRange': dateRange },
        success: function (response) {
            console.log( response['message']);
            if(response['message'] == 'Success'){
                alert('Report Generated Successfully');
                window.location.href = '/customer-reports/amount-of-purchase';
            }else{
                alert('An error Occured. Try Again after sometime!');
                return false;
            }
        }
    });
}




// ------------------------------------------------------
function generateNoOfVisitReport(){
    var storeArray = $('#kt_select2_3').val();
    console.log('store array : ',storeArray);

    var dateRange = $('#kt_daterangepicker_1').val();
    console.log('dateRange : ',dateRange);

    if(storeArray.length == 0){
        alert('Select atleast 1 store to continue!');
        return false;
    }
    if(dateRange.length == 0){
        alert('Select date range to continue!');
        return false;
    }
    // ------------------------------------------
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url: "/customer-reports/no-of-visits",
        headers: { 'X-CSRFToken': csrftoken },
        data: { 'storeArray[]': storeArray, 'dateRange': dateRange },
        success: function (response) {
            console.log( response['message']);
            if(response['message'] == 'Success'){
                alert('Report Generated Successfully');
                window.location.href = '/customer-reports/no-of-visits';
            }else{
                alert('An error Occured. Try Again after sometime!');
                return false;
            }
        }
    });
}
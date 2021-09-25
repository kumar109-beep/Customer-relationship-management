function SupervisorDetails(){
    var storeIdArray = $('#kt_select2_3').val();
    console.log('store id array >> ',storeIdArray)

    if(storeIdArray.length == 0){
        alert('Select atleast 1 store!');
    }else{
        alert('Under development!');
    }
}
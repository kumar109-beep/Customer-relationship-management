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
function getStores(thisTxt){
    var methodType = $('#reportmethodID').val().trim();
    var urlId = $(thisTxt).attr('urlId');
    console.log('id >>> ',urlId);

    if(methodType == 'AND'){
        // -------------------------------------------------------------------------
    $.ajax({
        type: 'GET',
        url: "/getStoresArray/"+urlId,
        success: function (response) {
            console.log(response);
            var dataStr = '';
            for(var i=0;i<response.length;i++){
                var data = '<tr>\
                                <th scope="row">'+(i+1)+'</th>\
                                <td>'+response[i]['StoreID']+'</td>\
                                <td>'+response[i]['storeName']+'</td>\
                                <td><input class="selecte_AND" type="checkbox" onclick="checkSelectCheckBox(this)" id="select_'+i+'" count="'+i+'" name="chk" storeID="'+response[i]['StoreID']+'"></td>\
                                <td><input class="DeSelecte_AND" type="checkbox" onclick="checkDeSelectCheckBox(this)" id="deSelect_'+i+'" count="'+i+'" name="unchk" storeID="'+response[i]['StoreID']+'"></td>\
                            </tr>';
                dataStr = dataStr + data;
            }
            $('#storeDetailAppend').css('display','');
            $('#Selecte_AND_All').prop('checked',false);

            $('#submitBtn').css('display','');
            $('#Deselect').css('display','');
            $('#customer-filtered-data').css('display','');

            $('#Selecte_AND_All').css('pointer-events',"");
            $('#Selecte_AND_All').css('opacity',"1");
            $('#Deselect').html('<input id="DeSelecte_AND_All" onclick="deSelect_All_Inputs()" type="checkbox">&nbsp;&nbsp;Deselect');


            $('#headerTag').css('display','none');

            $('#storeDataAppnd').html('');
            $('#storeDataAppnd').append(dataStr);
        }
    })
    // -------------------------------------------------------------------------
    }
    if(methodType == 'OR'){
            // -------------------------------------------------------------------------
            $.ajax({
                type: 'GET',
                url: "/getStoresArray/"+urlId,
                success: function (response) {
                    console.log(response);
                    var dataStr = '';
                    for(var i=0;i<response.length;i++){
                        var data = '<tr>\
                                        <th scope="row">'+(i+1)+'</th>\
                                        <td>'+response[i]['StoreID']+'</td>\
                                        <td>'+response[i]['storeName']+'</td>\
                                        <td><input class="selecte_AND" type="checkbox" name="chk" storeID="'+response[i]['StoreID']+'"></td>\
                                    </tr>';
                        dataStr = dataStr + data;
                    }
                    $('#storeDetailAppend').css('display','');
                    $('#Selecte_AND_All').prop('checked',false);

                    $('#Deselect').css('display','none');
                    $('#customer-filtered-data').css('display','');


                    $('#submitBtn').css('display','');
                    $('#Selecte_AND_All').css('pointer-events',"");
                    $('#Selecte_AND_All').css('opacity',"1");
                    $('#headerTag').css('display','none');

                    $('#storeDataAppnd').html('');
                    $('#storeDataAppnd').append(dataStr);
                }
            })
            // -------------------------------------------------------------------------
    }
    if(methodType == 'VISIT SINCE'){
        // -------------------------------------------------------------------------
        $.ajax({
            type: 'GET',
            url: "/getStoresArray/"+urlId,
            success: function (response) {
                console.log(response);
                var dataStr = '';
                for(var i=0;i<response.length;i++){
                    var data = '<tr>\
                                    <th scope="row">'+(i+1)+'</th>\
                                    <td>'+response[i]['StoreID']+'</td>\
                                    <td>'+response[i]['storeName']+'</td>\
                                    <td><input class="selecte_AND" name="chk" type="checkbox" onclick="checkSelectCheckBoxDate(this)" id="select_'+i+'" count="'+i+'" name="chk" storeID="'+response[i]['StoreID']+'"></td>\
                                    <td><input class="DeSelecte_AND" type="date" id="deSelect_'+i+'" count="'+i+'" name="unchk" style="opacity:0.2;pointer-events:none;"></td>\
                                </tr>';
                    dataStr = dataStr + data;
                }
                $('#storeDetailAppend').css('display','');
                $('#Deselect').css('display','');
                $('#Deselect').text('No Visit Since');
                $('#customer-filtered-data').css('display','');

                $('#submitBtn').css('display','');
                $('#headerTag').css('display','none');
                $('#storeDataAppnd').html('');
                $('#storeDataAppnd').append(dataStr);
            }
        })
        // -------------------------------------------------------------------------
    }
    if(methodType == 'VISIT NUMBER'){
        $.ajax({
            type: 'GET',
            url: "/getStoresArray/"+urlId,
            success: function (response) {
                console.log(response);
                var dataStr = '';
                for(var i=0;i<response.length;i++){
                    var data = '<tr>\
                                    <th scope="row">'+(i+1)+'</th>\
                                    <td>'+response[i]['StoreID']+'</td>\
                                    <td>'+response[i]['storeName']+'</td>\
                                    <td><input class="selecte_AND" type="checkbox" name="chk" storeID="'+response[i]['StoreID']+'"></td>\
                                </tr>';
                    dataStr = dataStr + data;
                }
                $('#storeDetailAppend').css('display','');
                $('#Selecte_AND_All').prop('checked',false);

                $('#Deselect').css('display','none');
                $('#customer-filtered-data').css('display','');


                $('#submitBtn').css('display','');
                $('#Selecte_AND_All').css('pointer-events',"");
                $('#Selecte_AND_All').css('opacity',"1");

                $('#headerTag').css('display','');
                $('#storeDataAppnd').html('');
                $('#storeDataAppnd').append(dataStr);
            }
        })
    }
    if(methodType == 'MARKED'){
        alert('MARKED method Under development!');
        $('#storeDataAppnd').html('');
        $('#storeDataAppnd').append('');
        $('#submitBtn').css('display','none');
        $('#customer-filtered-data').css('display','none');
        return false;
    }
    if(methodType == 'OR-NOT'){
        // -------------------------------------------------------------------------
    $.ajax({
        type: 'GET',
        url: "/getStoresArray/"+urlId,
        success: function (response) {
            console.log(response);
            var dataStr = '';
            for(var i=0;i<response.length;i++){
                var data = '<tr>\
                                <th scope="row">'+(i+1)+'</th>\
                                <td>'+response[i]['StoreID']+'</td>\
                                <td>'+response[i]['storeName']+'</td>\
                                <td><input class="selecte_AND" type="checkbox" onclick="checkSelectCheckBox(this)" id="select_'+i+'" count="'+i+'" name="chk" storeID="'+response[i]['StoreID']+'"></td>\
                                <td><input class="DeSelecte_AND" type="checkbox" onclick="checkDeSelectCheckBox(this)" id="deSelect_'+i+'" count="'+i+'" name="unchk" storeID="'+response[i]['StoreID']+'"></td>\
                            </tr>';
                dataStr = dataStr + data;
            }
            $('#storeDetailAppend').css('display','');
            $('#Selecte_AND_All').prop('checked',false);

            $('#submitBtn').css('display','');
            $('#Deselect').css('display','');
            $('#customer-filtered-data').css('display','');

            $('#Selecte_AND_All').css('pointer-events',"");
            $('#Selecte_AND_All').css('opacity',"1");
            $('#Deselect').html('<input id="DeSelecte_AND_All" onclick="deSelect_All_Inputs()" type="checkbox">&nbsp;&nbsp;Deselect');


            $('#headerTag').css('display','none');

            $('#storeDataAppnd').html('');
            $('#storeDataAppnd').append(dataStr);
        }
    })
    // -------------------------------------------------------------------------
    }
    
}

// ==================================================================================
// ==================================================================================
function generate_Report(){
    var reportID = $('#reportID').val().trim();
    var methodType = $('#reportmethodID').val().trim();
    console.log(methodType);

    if(methodType == 'AND'){
        var selectedStores = [];
        var DeSelectedStores = [];

        $('.selecte_AND:checkbox:checked').each(function() { selectedStores.push($(this).attr('storeID'));});
        $('.DeSelecte_AND:checkbox:checked').each(function() { DeSelectedStores.push($(this).attr('StoreID'));});

        console.log(selectedStores);
        console.log(DeSelectedStores);

        if(selectedStores.length == 0 && DeSelectedStores.length == 0){
            alert('Please select or deselect atleast 1 Store to continue!');
            return false;
        }else if(selectedStores.length == 0 ){
            alert('Please select atleast 1 Store to continue!');
            return false;
        }
        else{
        Swal.fire({
        position: 'center',
        title: "<b style='font-size:20px;font-weight:500;color:#1eb6e9;'><small>Generating Report ... </small></b>",
        showConfirmButton: false,
        onOpen: () => {
            Swal.showLoading();
        }
        })
        }
        // -------------------------------------------------------------------------
        var id = window.location.href;
        idList = id.split('/');
        var mainId = idList[idList.length - 1];
        console.log('id >>', mainId);

        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: "/create-group-report/"+mainId,
            headers: { 'X-CSRFToken': csrftoken },
            data: { 'reportID': reportID, 'reportMethod': 'AND', 'selectedStores[]': selectedStores,'DeSelectedStores[]': DeSelectedStores},
            success: function (response) {
                console.log(typeof (response['responseData']), response['responseData']);
                Swal.close();

                if(response['responseData'] == 'Success'){
                    alert('Report Generated Successfully');
                    window.location.href = '/store-Group-DataReport-List/'+mainId;
                }else{
                    alert('An error Occured. Try Again!');
                    return false;
                }
            }
        });
        // -------------------------------------------------------------------------
    }
    if(methodType == 'OR'){
        var selectedStores = [];

        $('.selecte_AND:checkbox:checked').each(function() { selectedStores.push($(this).attr('storeID'));});

        console.log(selectedStores);

        if(selectedStores.length == 0 ){
            alert('Please select atleast 1 Store to continue!');
            return false;
        }else{
            Swal.fire({
                position: 'center',
                title: "<b style='font-size:20px;font-weight:500;color:#1eb6e9;'><small>Generating Report ... </small></b>",
                showConfirmButton: false,
                onOpen: () => {
                    Swal.showLoading();
                }
            })
        }
        // -------------------------------------------------------------------------
        var id = window.location.href;
        idList = id.split('/');
        var mainId = idList[idList.length - 1];
        console.log('id >>', mainId);

        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: "/create-group-report/"+mainId,
            headers: { 'X-CSRFToken': csrftoken },
            data: { 'reportID': reportID, 'reportMethod': 'OR', 'selectedStores[]': selectedStores,'DeSelectedStores[]':[]},
            success: function (response) {
                console.log(typeof (response['responseData']), response['responseData']);
                Swal.close();

                if(response['responseData'] == 'Success'){
                    alert('Report Generated Successfully');
                    window.location.href = '/store-Group-DataReport-List/'+mainId;
                }else{
                    alert('An error Occured. Try Again!');
                    return false;
                }
            }
        });
        // -------------------------------------------------------------------------
    }if(methodType == 'VISIT SINCE'){
        var selectedStores = [];
        var idArray = [];
        var dateArray = [];

        $('.selecte_AND:checkbox:checked').each(function() { selectedStores.push($(this).attr('storeID'));idArray.push('deSelect_'+$(this).attr('count')+'');});

        console.log(selectedStores);
        console.log(idArray);

        for(var i=0;i<idArray.length;i++){
            var data = $('#'+idArray[i]).val().trim();
            if(data.length == 0){
                $('#'+idArray[i]).css('border',"2px solid red");
                alert('Please select a valid data!');
                return false;
            }else{
                $('#'+idArray[i]).css('border',"1px solid black");
                dateArray.push(data)
            }
        }
        console.log(dateArray);


        if(selectedStores.length == 0 ){
            alert('Please select atleast 1 Store to continue!');
            return false;
        }
        else{
            Swal.fire({
                position: 'center',
                title: "<b style='font-size:20px;font-weight:500;color:#1eb6e9;'><small>Generating Report ... </small></b>",
                showConfirmButton: false,
                onOpen: () => {
                    Swal.showLoading();
                }
            })
        }
        // -------------------------------------------------------------------------
        var id = window.location.href;
        idList = id.split('/');
        var mainId = idList[idList.length - 1];
        console.log('id >>', mainId);

        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: "/create-group-report/"+mainId,
            headers: { 'X-CSRFToken': csrftoken },
            data: { 'reportID': reportID, 'reportMethod': 'VISIT SINCE', 'selectedStores[]': selectedStores,'DeSelectedStores[]':dateArray},
            success: function (response) {
                console.log(typeof (response['responseData']), response['responseData']);
                Swal.close();

                if(response['responseData'] == 'Success'){
                    alert('Report Generated Successfully');
                    window.location.href = '/store-Group-DataReport-List/'+mainId;
                }else{
                    alert('An error Occured. Try Again!');
                    return false;
                }
            }
        });
        // -------------------------------------------------------------------------
    }

    if(methodType == 'VISIT NUMBER'){
        var selectedStores = [];

        var formula = $('#formula').val();
        var N = $('#visitCount').val();
        if(N.length == 0 ){
            alert('Please enter no. of visits to continue!');
            return false;
        }if(formula.length == 0 ){
            alert('Please select formula to continue!');
            return false;
        }

        var DeSelectedStores = [];
        DeSelectedStores.push(N);
        DeSelectedStores.push(formula);

        $('.selecte_AND:checkbox:checked').each(function() { selectedStores.push($(this).attr('storeID'));});

        console.log(selectedStores);

        if(selectedStores.length == 0 ){
            alert('Please select atleast 1 Store to continue!');
            return false;
        }

        else{
            Swal.fire({
                position: 'center',
                title: "<b style='font-size:20px;font-weight:500;color:#1eb6e9;'><small>Generating Report ... </small></b>",
                showConfirmButton: false,
                onOpen: () => {
                    Swal.showLoading();
                }
            })
        }
        // -------------------------------------------------------------------------
        var id = window.location.href;
        idList = id.split('/');
        var mainId = idList[idList.length - 1];
        console.log('id >>', mainId);

        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: "/create-group-report/"+mainId,
            headers: { 'X-CSRFToken': csrftoken },
            data: { 'reportID': reportID, 'reportMethod': 'VISIT NUMBER', 'selectedStores[]': selectedStores,'DeSelectedStores[]':DeSelectedStores},
            success: function (response) {
                console.log(typeof (response['responseData']), response['responseData']);
                Swal.close();

                if(response['responseData'] == 'Success'){
                    alert('Report Generated Successfully');
                    window.location.href = '/store-Group-DataReport-List/'+mainId;
                }else{
                    alert('An error Occured. Try Again!');
                    return false;
                }
            }
        });
        // -------------------------------------------------------------------------
    }

    if(methodType == 'OR-NOT'){
        var selectedStores = [];
        var DeSelectedStores = [];

        $('.selecte_AND:checkbox:checked').each(function() { selectedStores.push($(this).attr('storeID'));});
        $('.DeSelecte_AND:checkbox:checked').each(function() { DeSelectedStores.push($(this).attr('StoreID'));});

        console.log(selectedStores);
        console.log(DeSelectedStores);

        if(selectedStores.length == 0 && DeSelectedStores.length == 0){
            alert('Please select or deselect atleast 1 Store to continue!');
            return false;
        }else if(selectedStores.length == 0 ){
            alert('Please select atleast 1 Store to continue!');
            return false;
        }
        else{
        Swal.fire({
        position: 'center',
        title: "<b style='font-size:20px;font-weight:500;color:#1eb6e9;'><small>Generating Report ... </small></b>",
        showConfirmButton: false,
        onOpen: () => {
            Swal.showLoading();
        }
        })
        }
        // -------------------------------------------------------------------------
        var id = window.location.href;
        idList = id.split('/');
        var mainId = idList[idList.length - 1];
        console.log('id >>', mainId);

        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: "/create-group-report/"+mainId,
            headers: { 'X-CSRFToken': csrftoken },
            data: { 'reportID': reportID, 'reportMethod': 'OR-NOT', 'selectedStores[]': selectedStores,'DeSelectedStores[]': DeSelectedStores},
            success: function (response) {
                console.log(typeof (response['responseData']), response['responseData']);
                Swal.close();

                if(response['responseData'] == 'Success'){
                    alert('Report Generated Successfully');
                    window.location.href = '/store-Group-DataReport-List/'+mainId;
                }else{
                    alert('An error Occured. Try Again!');
                    return false;
                }
            }
        });
        // -------------------------------------------------------------------------
    }
}


// ======================================================================================================================
// ======================================================================================================================
function select_All_Inputs(){
    const cb = document.getElementById('Selecte_AND_All');
    console.log(cb.checked);
    if(cb.checked){
        var ele=document.getElementsByName('chk');  
        for(var i=0; i<ele.length; i++){  
            if(ele[i].type=='checkbox')  
                ele[i].checked=true;  
                // ---------------------------------
                $(".DeSelecte_AND").css('pointer-events',"none");
                $(".DeSelecte_AND").css('opacity',"0.2");
                $('#DeSelecte_AND_All').css('pointer-events',"none");
                $('#DeSelecte_AND_All').css('opacity',"0.2");

        }  
        var ele=document.getElementsByName('unchk');  
        for(var i=0; i<ele.length; i++){  
            if(ele[i].type=='checkbox')  
                ele[i].checked=false; 
        } 

    }else{
        var ele=document.getElementsByName('chk');  
        for(var i=0; i<ele.length; i++){  
            if(ele[i].type=='checkbox')  
                ele[i].checked=false; 
                $(".DeSelecte_AND").css('pointer-events',"");
                $(".DeSelecte_AND").css('opacity',"1");
                $('#DeSelecte_AND_All').css('pointer-events',"");
                $('#DeSelecte_AND_All').css('opacity',"1");
        } 

    }
}
// ======================================================================================================================
// ======================================================================================================================
function deSelect_All_Inputs(){
    const cb = document.getElementById('DeSelecte_AND_All');
    console.log(cb.checked);
    if(cb.checked){
        var ele=document.getElementsByName('unchk');  
        for(var i=0; i<ele.length; i++){  
            if(ele[i].type=='checkbox')  
                ele[i].checked=true;  
                // ---------------------------------
                $(".selecte_AND").css('pointer-events',"none");
                $(".selecte_AND").css('opacity',"0.2");
                $('#Selecte_AND_All').css('pointer-events',"none");
                $('#Selecte_AND_All').css('opacity',"0.2");

        }  
        var ele=document.getElementsByName('chk');  
        for(var i=0; i<ele.length; i++){  
            if(ele[i].type=='checkbox')  
                ele[i].checked=false; 
        } 

    }else{
        var ele=document.getElementsByName('unchk');  
        for(var i=0; i<ele.length; i++){  
            if(ele[i].type=='checkbox')  
                ele[i].checked=false; 
                $(".selecte_AND").css('pointer-events',"");
                $(".selecte_AND").css('opacity',"1");
                $('#Selecte_AND_All').css('pointer-events',"");
                $('#Selecte_AND_All').css('opacity',"1");
        } 

    }
}
// ======================================================================================================================
// ======================================================================================================================
function checkSelectCheckBox(thisTxt){
    var ids = $(thisTxt).attr('count');
    console.log('ids >>> ',ids);
    var idData = '#deSelect_'+ids;
    console.log('ids >>> ',idData);

    if($('#select_'+ids+'').is(":checked")){
        $(idData).css('pointer-events',"none");
        $(idData).css('opacity',"0.2");
        $('#DeSelecte_AND_All').css('pointer-events',"none");
        $('#DeSelecte_AND_All').css('opacity',"0.3");
    }else{
        $(idData).css('pointer-events',"");
        $(idData).css('opacity',"1");
        $('#DeSelecte_AND_All').css('pointer-events',"");
        $('#DeSelecte_AND_All').css('opacity',"1");
    }

}

function checkDeSelectCheckBox(thisTxt){
    var ids = $(thisTxt).attr('count');
    console.log('ids >>> ',ids);
    var idData = '#select_'+ids;
    console.log('ids >>> ',idData);

    if($('#deSelect_'+ids+'').is(":checked")){
        $(idData).css('pointer-events',"none");
        $(idData).css('opacity',"0.2");
        $('#Selecte_AND_All').css('pointer-events',"none");
        $('#Selecte_AND_All').css('opacity',"0.3");
    }else{
        $(idData).css('pointer-events',"");
        $(idData).css('opacity',"1");
        $('#Selecte_AND_All').css('pointer-events',"");
        $('#Selecte_AND_All').css('opacity',"1");
    }
}



function checkSelectCheckBoxDate(thisTxt){
    var ids = $(thisTxt).attr('count');
    console.log('ids >>> ',ids);
    var idData = '#deSelect_'+ids;
    console.log('ids >>> ',idData);

    if($('#select_'+ids+'').is(":checked")){
        $(idData).css('pointer-events',"");
        $(idData).css('opacity',"1");
        $('#Selecte_AND_All').css('pointer-events',"");
        $('#Selecte_AND_All').css('opacity',"1");
    }else{
        $(idData).css('pointer-events',"none");
        $(idData).css('opacity',"0.2");
        $('#Selecte_AND_All').css('pointer-events',"none");
        $('#Selecte_AND_All').css('opacity',"0.3");
    }
}
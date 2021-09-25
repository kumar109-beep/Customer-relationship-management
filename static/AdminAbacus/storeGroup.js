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
var ek=[];
var sid=[];
var storeIDs=[];

// 
function addNewgroup(){
    ek=[];
    sid=[];
    storeIDs=[];
    $('.storeData:checkbox:checked').each(function() { ek.push($(this).attr('storeName'));sid.push($(this).attr('storeID'));storeIDs.push($(this).attr('storeId')); });
    console.log(ek);
    console.log(sid);
    console.log(storeIDs);

    if(ek.length == 0){
        data = '<tr>\
                    <th scope="row"></th>\
                    <td>No Store Selected</td>\
                    <td></td>\
                </tr>';
    }else{
        var data = '';
        for(var i=1;i<=ek.length;i++){
            var dataStr = '<tr>\
                        <th scope="row">#'+(i)+'</th>\
                        <td>'+ek[i-1]+'</td>\
                        <td>'+sid[i-1]+'</td>\
                    </tr>';

                data = data + dataStr;
        }
    }
    
            $('#storeAppendTable').html('');
            $('#storeAppendTable').append(data);

}
// =====================================================================================================
// =====================================================================================================
function CreateGroup(){
    console.log(ek);
    console.log(sid);
    console.log(storeIDs);

    if(storeIDs.length == 0){
        alert('Please select atleast 1 Store.');
        return false;
    }

    var groupName = $('#groupName').val().trim();
    var groupDescription = $('#groupDescription').val().trim();
    var groupID = $('#groupId').val().trim();

    if(groupName.length == 0){
        alert('Enter Group Name');
        return false;
    }if(groupDescription.length == 0){
        groupDescription = 'NA';
    }

    // ------------------------------------------
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url: "/Create-Store-Group",
        headers: { 'X-CSRFToken': csrftoken },
        data: { 'groupName': groupName, 'groupDescription': groupDescription, 'groupID': groupID, 'storeIDs[]': storeIDs },
        success: function (response) {
            console.log(typeof (response['responseData']), response['responseData']);
            if(response['responseData'] == 'Success'){
                alert('Group Created Successfully');
                window.location.href = '/Store-Group-list';
            }else{
                alert('An error Occured. Try Again!');
                return false;
            }
        }
    });
}
// =====================================================================================================
// =====================================================================================================
// =====================================================================================================
function UpdateGroup(){
    console.log(ek);
    console.log(sid);
    console.log(storeIDs);

    if(storeIDs.length == 0){
        alert('Please select atleast 1 Store.');
        return false;
    }

    var groupName = $('#groupName').val().trim();
    var groupDescription = $('#groupDescription').val().trim();
    var groupID = $('#groupId').val().trim();

    if(groupName.length == 0){
        alert('Enter Group Name');
        return false;
    }if(groupDescription.length == 0){
        groupDescription = 'NA';
    }

    var id = window.location.href;
    idList = id.split('/');
    var mainId = idList[idList.length - 1];
    console.log('id >>', mainId);
    // ------------------------------------------
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url: "/edit-store-group-detail/"+mainId,
        headers: { 'X-CSRFToken': csrftoken },
        data: { 'groupName': groupName, 'groupDescription': groupDescription, 'groupID': groupID, 'storeIDs[]': storeIDs },
        success: function (response) {
            console.log(typeof (response['responseData']), response['responseData']);
            if(response['responseData'] == 'Success'){
                alert('Group Updated Successfully');
                window.location.href = '/edit-store-group-detail/'+mainId;
            }else{
                alert('An error Occured. Try Again!');
                return false;
            }
        }
    });
}
// =====================================================================================================

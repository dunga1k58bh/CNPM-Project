
function addMealFunction(ma_mon, tenmon, giamon) {
    mamon= "'"+ ma_mon +"'";
    tm=",'"+ tenmon +"'";
    idMealAdded= "idMeal"+ ma_mon;
        var html=' <tr id="'
    +idMealAdded
    +'" class="'
    +ma_mon
    +'"> <td style="width :30%"  class="ten__mon">' 
    +tenmon
    +' </td>'  
    +'<td style="width :20%" class="so__luong"> <input style="width: 100px" name="so_luongs" type="number" min="1" step="1" value="1" /> </td>' 
    +'<td style="width :20%" class="gia__mon">'
    + giamon
    + '</td>'
    +'<td style="width :20%" class="thanh__tien"></td>'
    +'<td hidden> <input type="text" value="'+ma_mon+'"name="ma_mons" > </td>'
    +'<td style="width :10%" > <button class="del_mon" type="button" onclick="deleteMealFunction('
    +mamon
    +tm
    +')" >Del</button> </td>'
    + ' </tr>';
    document.getElementById("addMeal"+tenmon).disabled= true;
    document.getElementById('bang_hoa_don').insertAdjacentHTML('afterend', html);
    document.getElementById("addMeal"+tenmon+"db").disabled= true;
    
}

function deleteMealFunction(idMeal, tenmon) {
    var element = document.getElementById("idMeal"+idMeal);
    element.parentNode.removeChild(element);
    document.getElementById("addMeal"+tenmon).disabled= false;
    document.getElementById("addMeal"+tenmon+"db").disabled= false;
}
function useHFunction(){
    document.homeForm.ipname.value= 96;
}
function saveHFunction(){
    document.homeForm.ipname.value= 66;
}
function searchHFunction(){
    document.homeForm.ipname.value= 99;
}
function useTFunction(){
    document.take_awayForm.ipname.value= 96;
}
function saveTFunction(){
    document.take_awayForm.ipname.value= 66;
}
function searchTFunction(){
    document.take_awayForm.ipname.value= 99;
}
function validateHomeForm(){
    var ip = document.homeForm.so_diem_tieu.value;
    var max1 = Number(document.homeForm.dtl.value);
    var tt  =  Number(document.homeForm.tt.value);
    var ipval= Number(document.homeForm.ipname.value);
    if(ipval == 66){
        return true;
    }
    if(ipval == 99){
        return true;
    }
    if(ip != "" && ip < 0){
        alert( "Số điểm tiêu phải > 0.");
        return false;
    }
    if( ip != "" && ip >500000){
        alert( "Số điểm tiêu không được vượt quá 500000.");
        return false;
    }
    if( ip != "" && ip > max1){
        alert( "Số điểm tiêu không được vượt quá số điểm hiện có.");
        return false;
    }
    if( ip != "" && ip > tt ){
        alert( "Số điểm tiêu không được lớn hơn giá trị hóa đơn." );
        return false;
    }
    if(ipval == 96){
        return true;
    }
    var result=confirm("Are you sure?");
    return result ;
}
function validateTake_awayForm(){
    var ip = document.take_awayForm.so_diem_tieu.value;
    var max1 = Number(document.take_awayForm.dtl.value);
    var tt  =  Number(document.take_awayForm.tt.value);
    var ipval= Number(document.take_awayForm.ipname.value);
    if(ipval == 66){
        return true;
    }
    if(ipval == 99){
        return true;
    }
    if(ip != "" && ip < 0){
        alert( "Số điểm tiêu phải > 0.");
        return false;
    }
    if( ip != "" && ip >500000){
        alert( "Số điểm tiêu không được vượt quá 500000.");
        return false;
    }
    if( ip != "" && ip > max1){
        alert( "Số điểm tiêu không được vượt quá số điểm hiện có.");
        return false;
    }
    if( ip != "" && ip > tt ){
        alert( "Số điểm tiêu không được lớn hơn giá trị hóa đơn." );
        return false;
    }
    if(ipval == 96){
        return true;
    }
    var result=confirm("Are you sure?");
    return result ;
}
function menu_monan(ma_menu){
    var x = document.getElementsByClassName("menu_1");
    var y = document.getElementsByClassName("menu_2");
    var z = document.getElementsByClassName("menu_3");
    var t = document.getElementsByClassName("menu_4");
    var k = document.getElementById("savemn");
     var i;
     document.getElementsByClassName("themmonmoi")[0].style.display = 'table-row';
     document.getElementById("table_mon").style.display = 'inline-table';
     document.getElementsByClassName("addd_mon")[0].style.display = 'flex';

    if(ma_menu == 'MN1'){
        for (i = 0; i < x.length; i++) x[i].style.display = 'table-row';
        for (i = 0; i < y.length; i++) y[i].style.display = 'none';
        for (i = 0; i < z.length; i++) z[i].style.display = 'none';
        for (i = 0; i < t.length; i++) t[i].style.display = 'none';
    }
    if(ma_menu == 'MN2'){
        for (i = 0; i < x.length; i++) x[i].style.display = 'none';
        for (i = 0; i < y.length; i++) y[i].style.display = 'table-row';
        for (i = 0; i < z.length; i++) z[i].style.display = 'none';
        for (i = 0; i < t.length; i++) t[i].style.display = 'none';
    }
    if(ma_menu == 'MN3'){
        for (i = 0; i < x.length; i++) x[i].style.display = 'none';
        for (i = 0; i < y.length; i++) y[i].style.display = 'none';
        for (i = 0; i < z.length; i++) z[i].style.display = 'table-row';
        for (i = 0; i < t.length; i++) t[i].style.display = 'none';
    }
    if(ma_menu == 'MN4'){
        for (i = 0; i < x.length; i++) x[i].style.display = 'none';
        for (i = 0; i < y.length; i++) y[i].style.display = 'none';
        for (i = 0; i < z.length; i++) z[i].style.display = 'none';
        for (i = 0; i < t.length; i++) t[i].style.display = 'table-row';
    }
    k.value =ma_menu;
}
function set_ban() {
    var x = document.getElementById("quantity").value;
    alert("Số lượng bàn hiện tại là "+x);
}
function set_emp(){
    document.getElementsByClassName("emp")[0].style.display='contents'
    document.getElementsByClassName("setting_menu")[0].style.display='none'
}
function set_menu(){
    document.getElementsByClassName("emp")[0].style.display='none'
    document.getElementsByClassName("setting_menu")[0].style.display='contents'
}

function add_db(){
    document.getElementById("add_db_popup").style.display='block';
}
function close_add_popup(){
    document.getElementById("add_db_popup").style.display='none';
}
function db_mn1(){
    var x = document.getElementsByClassName("dbmenu_1");
    var y = document.getElementsByClassName("dbmenu_2");
    var z = document.getElementsByClassName("dbmenu_3");
    var t = document.getElementsByClassName("dbmenu_4");
    for (i = 0; i < x.length; i++) x[i].style.display = 'table-row';
    for (i = 0; i < y.length; i++) y[i].style.display = 'none';
    for (i = 0; i < z.length; i++) z[i].style.display = 'none';
    for (i = 0; i < t.length; i++) t[i].style.display = 'none';
}
function db_mn2(){
    var x = document.getElementsByClassName("dbmenu_1");
    var y = document.getElementsByClassName("dbmenu_2");
    var z = document.getElementsByClassName("dbmenu_3");
    var t = document.getElementsByClassName("dbmenu_4");
    for (i = 0; i < x.length; i++) x[i].style.display = 'none';
    for (i = 0; i < y.length; i++) y[i].style.display = 'table-row';
    for (i = 0; i < z.length; i++) z[i].style.display = 'none';
    for (i = 0; i < t.length; i++) t[i].style.display = 'none';
}
function db_mn3(){
    var x = document.getElementsByClassName("dbmenu_1");
    var y = document.getElementsByClassName("dbmenu_2");
    var z = document.getElementsByClassName("dbmenu_3");
    var t = document.getElementsByClassName("dbmenu_4");
    for (i = 0; i < x.length; i++) x[i].style.display = 'none';
    for (i = 0; i < y.length; i++) y[i].style.display = 'none';
    for (i = 0; i < z.length; i++) z[i].style.display = 'table-row';
    for (i = 0; i < t.length; i++) t[i].style.display = 'none';
}
function db_mn4(){
    var x = document.getElementsByClassName("dbmenu_1");
    var y = document.getElementsByClassName("dbmenu_2");
    var z = document.getElementsByClassName("dbmenu_3");
    var t = document.getElementsByClassName("dbmenu_4");
    for (i = 0; i < x.length; i++) x[i].style.display = 'none';
    for (i = 0; i < y.length; i++) y[i].style.display = 'none';
    for (i = 0; i < z.length; i++) z[i].style.display = 'none';
    for (i = 0; i < t.length; i++) t[i].style.display = 'table-row';
}
function themnv(){
    document.getElementsByClassName("themnv")[0].style.display = 'table-row';
}
function bug_del(){
    alert("Không thể xóa quản lý");
}

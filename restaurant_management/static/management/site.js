
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
    +'<td> <input type="text" value="'+ma_mon+'"name="ma_mons" hidden> </td>'
    +'<td style="width :10%" > <button type="button" onclick="deleteMealFunction('
    +mamon
    +tm
    +')" >Del</button> </td>'
    + ' </tr>';
    document.getElementById("addMeal"+tenmon).disabled= true;
    document.getElementById('bang_hoa_don').insertAdjacentHTML('afterend', html);
    
}

function deleteMealFunction(idMeal, tenmon) {
    var element = document.getElementById("idMeal"+idMeal);
    element.parentNode.removeChild(element);
    document.getElementById("addMeal"+tenmon).disabled= false;
}
function deletebill(){
    var result=confirm("Are you sure?");
    if(result== true){
        remove_hoa_don = true;
    }
}

 function menu_monan(ma_menu){
    var x = document.getElementsByClassName("menu_1");
    var y = document.getElementsByClassName("menu_2");
    var z = document.getElementsByClassName("menu_3");
    var t = document.getElementsByClassName("menu_4");
    var k = document.getElementById("savemn");
     var i;
     document.getElementsByClassName("themmonmoi")[0].style.display = 'table-row';
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

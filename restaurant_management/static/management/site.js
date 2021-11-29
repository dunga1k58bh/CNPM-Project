
function addMealFunction(ma_mon, tenmon, giamon) {
    change= "'change" +tenmon + ma_mon+ "'" ;
    tmmm = "change"+tenmon + ma_mon ;
    
        var html=' <tr class="'
    +ma_mon
    +'">  <th scope="row">  </th>  <td class="ten__mon">' 
    +tenmon
    +' </td>'  
    +'<td class="so__luong"> <input onclick="delete_num('
    +change
    +')" type="button" value="-" />'
    +'<input id="'
    +tmmm
    +'" name="so_luongs" type="text" value="1" />'
    +'<input onclick="add_num('
    +change
    +')" type="button" value="+" /> </td>' 
    +'<td class="gia__mon">'
    + giamon
    + '</td>'
    +'<td class="thanh__tien"></td>'
    +' <input type="text" value="'+ma_mon+'"name="ma_mons" hidden>'
    + ' </tr>';
    document.getElementById("addMeal"+tenmon).disabled= true;
    document.getElementById('bang_hoa_don').insertAdjacentHTML('afterend', html);
    
}
function deletebill(){
    var result=confirm("Are you sure?");
    if(result== true){
        remove_hoa_don = true;
    }
}

function add_num(id){
    var result = document.getElementById(id); 
    var qty = result.value; 
    if( !isNaN(qty)) result.value++;
    return false;
}

function delete_num(id){
    var result = document.getElementById(id);
    var qty = result.value; 
    if( !isNaN(qty) && qty > 1 ) result.value--;
    return false;
}

 function menu_monan(ma_menu){
    var x = document.getElementsByClassName("menu_1");
    var y = document.getElementsByClassName("menu_2");
    var z = document.getElementsByClassName("menu_3");
    var t = document.getElementsByClassName("menu_4");
     var i;
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


function deleteMeal(){

}

function addMealFunction(ma_mon, tenmon, giamon) {
    alert("Thêm món "+tenmon+" cho hóa đơn");
    var html=' <tr >  <th scope="row">  </th>  <td class="ten__mon">' 
    +tenmon
    +' </td>  <td class="so__luong"> <input type="text" name="so_luongs"> </td>  <td class="gia__mon">'
    + giamon+ '</td> <input type="text" value="'+ma_mon+'"name="ma_mons" hidden>'
    + '<td> <button  onclick="deleteMeal()"> Delete </button> </td> </tr>';
    document.getElementById('bang_hoa_don').insertAdjacentHTML('afterend', html);
}
 

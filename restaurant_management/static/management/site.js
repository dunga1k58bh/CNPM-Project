
function deleteMeal(){

}

function addMealFunction(tenmon, giamon) {
    alert("Thêm món "+tenmon+" cho hóa đơn");
    var html=' <tr >  <th scope="row">  </th>  <td class="ten__mon">' 
    +tenmon
    +' </td>  <td class="so__luong"> <input type="text" name="name-field"> </td>  <td class="gia__mon">'
    + giamon+ '</td> '
    + '<td> <button  onclick="deleteMeal()"> Delete </button> </td> </tr>   ';
    document.getElementById('bang_hoa_don').insertAdjacentHTML('afterend', html);
}
 

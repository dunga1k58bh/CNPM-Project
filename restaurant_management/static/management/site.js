
function addMealFunction(ma_mon, tenmon, giamon) {
    var result=confirm("Are you sure?");
    // alert("Thêm món "+tenmon+" cho hóa đơn");
    if(result== true){
        var html=' <tr class="monmoithem">  <th scope="row">  </th>  <td class="ten__mon">' 
    +tenmon
    +' </td>  <td class="so__luong"> <input type="text" name="so_luongs" value="1"> </td>  <td class="gia__mon">'
    + giamon
    + '</td>'
    +'<td class="thanh__tien"></td>'
    +' <input type="text" value="'+ma_mon+'"name="ma_mons" hidden>'
    + '<td> <button  onclick="deleteMeal()"> Delete </button> </td> </tr>';
    document.getElementById('bang_hoa_don').insertAdjacentHTML('afterend', html);
    }
}
 

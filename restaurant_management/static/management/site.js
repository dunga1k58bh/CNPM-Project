
function deleteMeal(){

}
function calculate(quantity, dongia){
    return quantity*dongia ;
}
var tongtien=0;
function addMealFunction(tenmon, giamon) {
    alert("Thêm món "+tenmon+" cho hóa đơn");
    var html=' <tr >  <th scope="row">  </th>  <td class="ten__mon">' 
    +tenmon
    +' </td>  <td class="so__luong"> <input type="text" name="name-field" value="1"> </td>  <td class="gia__mon">'
    + giamon+ '</td> '
    + '<td class="thanh_tien">'
    + calculate(1,giamon)
    +'</td>'
    + '<td> <button  onclick="deleteMeal()"> Delete </button> </td> </tr>   ';
    // tongtien+=calculate(1,giamon);
    document.getElementById('bang_hoa_don').insertAdjacentHTML('afterend', html);
}

function getTongtien(){
    return tongtien;
}

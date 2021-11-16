
function newFunction(ban_so, mahoadon){
    document.getElementById("bill__name").innerHTML = "Hóa đơn của bàn "+ban_so;
    if(mahoadon != undefined){
        document.getElementById("bill__id").innerHTML = "Mã hóa đơn: "+mahoadon;
        document.getElementById("create__bill").style.zIndex = '-1' ;
        document.getElementById("pay__bill").style.zIndex = '1' ;
        document.getElementById("add__meal").style.zIndex = '1' ; 
    }else{
        document.getElementById("bill__id").innerHTML = "Bàn "+ ban_so+ " chưa có hóa đơn" ;
        document.getElementById("create__bill").style.zIndex = '1' ;
        document.getElementById("add__meal").style.zIndex = '-1' ; 
        document.getElementById("pay__bill").style.zIndex = '-1' ; 
    }

}
function addMealFunction() {
    alert("Thêm món cho hóa đơn");
    // var retVal = confirm("Do you want to continue ?");

}

function payBillFunction(mahoadon){
    alert("Thanh toán cho hóa đơn"+ mahoadon);
    // var retVal = confirm("Do you want to continue ?");

}
function createBillFunction(){
    alert("Tạo mới hóa đơn");
}

function myFunction(temp) {
    document.getElementById("demo").innerHTML = "Hóa đơn của bàn "+temp;
}
function newFunction(ban_so, mahoadon){
    document.getElementById("demo").innerHTML = "Hóa đơn của bàn "+ban_so;
    if(mahoadon == 5){
        document.getElementById("ttkh").innerHTML = "Thông tin khách hàng "+mahoadon;  
    }else{
        document.getElementById("ttkh").innerHTML = "Thông tin khách hàng "; 
    }

}
function labelFunction(status) {
    if(status=="rảnh"){
        document.getElementById("label").innerHTML = "Hóa đơn của bàn "+ban_so;
    }
}
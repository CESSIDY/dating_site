var myWindow;
function myWindowOpen(elem, url) {
  myWindow = window.open(url, "myWindow", "width=600, height=350");
}

function myWindowClose(){
    window.close();
}
    $( document ).ready(function() {
    var status = $('#status_of_page').val();
    if(status == '1'){
         window.close();
    }});



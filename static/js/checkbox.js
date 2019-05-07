function send(){
    var id = document.getElementsByName('test');
    var value = new Array();
    for(var i = 0; i < id.length; i++){
     if(id[i].checked)
     value.push(id[i].value);
    }
  window.location ='某Action!netWorkingUpdate?concentratorids='+value.toString();


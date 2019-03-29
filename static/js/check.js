$('[name="usertype"]').bootstrapSwitch(
			{
                onText:"教师登录",
                offText:"学生登录",
                onColor:"success",
                offColor:"info",
                size:"normal",
                onSwitchChange:function(event,state)
                {
                    if(state==true){
                        document.getElementById("login_identity").value='TEA';
                    }
                }
   			});



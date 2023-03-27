function encode(return_data,user_name,pwd){
    if(return_data=='no'){
        return null;
    }else{
        var data = return_data;
        var scode=data.split("#")[0];
        var sxh=data.split("#")[1];
        var code=user_name+'%%%'+pwd;
        var encoded ='';
        for(var i=0;i<code.length;i++){
            if(i<20){
                encoded=encoded+code.substring(i,i+1)+scode.substring(0,parseInt(sxh.substring(i,i+1)));
                scode = scode.substring(parseInt(sxh.substring(i,i+1)),scode.length);
              }else{
                encoded=encoded+code.substring(i,code.length);
                i=code.length;
              }
         }
        return encoded
    }
}
// data = '4U4GKBhEf4WnlO3r22V8o688eIs117IM8259oW#31232121132333122111'
// user_name = '201905556824'
// pwd = '20401314521lzl'
// console.log(encode(data,user_name,pwd))
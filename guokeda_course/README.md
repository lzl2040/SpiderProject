## 概述
国科大选课工具。
## 遇到的问题
1.你的会话已失效或身份已改变，请重新登录
这个其实是选上了
## 未来的工作
- 自动识别验证码
- 图形界面
- 选好一门可接着选一门
- 选多门(做这个)

## Note
### 1.16
登录的密码进行了加密
```js
function sepSubmit() {
		var userName1 = $('#userName1').val();
		var pwd1 = $('#pwd1').val();
		var certCode1 = $('#certCode1').val();
		if(pwd1 == '' || pwd1 == 'null') {
			return false;
		} else {
	        var jsePubKey = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxG1zt7VW/VNk1KJC7AuoInrMZKTf0h6S6xBaROgCz8F3xdEIwdTBGrjUKIhIFCeDr6esfiVxUpdCdiRtqaCS9IdXO+9Fs2l6fx6oGkAA9pnxIWL7bw5vAxyK+liu7BToMFhUdiyRdB6erC1g/fwDVBywCWhY4wCU2/TSsTBDQhuGZzy+hmZGEB0sqgZbbJpeosW87dNZFomn/uGhfCDJzswjS/x0OXD9yyk5TEq3QEvx5pWCcBJqAoBfDDQy5eT3RR5YBGDJODHqW1c2OwwdrybEEXKI9RCZmsNyIs2eZn1z1Cw1AdR+owdXqbJf9AnM3e1CN8GcpWLDyOnaRymLgQIDAQAB';
	        var encrypt = new JSEncrypt();
	        encrypt.setKey(jsePubKey);
	        passwordRSA = encrypt.encrypt(pwd1);
	        $('#pwd').val(passwordRSA);
		}
		$('#userName').val(userName1);
		$('#certCode').val(certCode1);
		
		$('#sepform').submit();
    }
```
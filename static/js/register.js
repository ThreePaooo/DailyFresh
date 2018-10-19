$(function(){

	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_email = false;
	var error_check = false;
	var error_phone = false;
	var error_address = false;


	$('#username').blur(function() {
		check_user_name();
	});

	$('#password').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	$('#email').blur(function() {
		check_email();
	});
	$('#phone').blur(function () {
		check_phone();
    });
	$('#address').blur(function () {
		check_address()
    })

	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});


	function check_user_name(){
		var len = $('#username').val().length;
		if(len<5||len>20)
		{
			$('#username').next().html('请输入5-20个字符的用户名')
			$('#username').next().show();
			error_name = true;
		}
		else
		{
			$('#username').next().hide();
			error_name = false;
		}
	}

	function check_pwd(){
		var len = $('#password').val().length;
		if(len<8||len>20)
		{
			$('#password').next().html('密码最少8位，最长20位')
			$('#password').next().show();
			error_password = true;
		}
		else
		{
			$('#password').next().hide();
			error_password = false;
		}		
	}

	// 检查输入的电话格式
	function check_phone() {
		var phone = $('#phone').val().length
		if (phone == 11){
			$('#phone').next().hide()
			error_phone = false
		}
		else{
			$('#phone').next().html('你输入的电话格式不正确')
			$('#phone').next().show()
			error_phone = true
		}
    }

    function check_address() {
		var address = $('#address').val()
		if (address == ''){
			$('#address').next().html('地址不能为空')
			$('#address').next().show()
			error_address = true
		}
		else {
			$('#address').next().hide()
			error_address = false
		}
    }

	function check_cpwd(){
		var pass = $('#password').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致')
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}		
		
	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if(re.test($('#email').val()))
		{
			$('#email').next().hide();
			error_email = false;
		}
		else
		{
			$('#email').next().html('你输入的邮箱格式不正确')
			$('#email').next().show();
			error_check_password = true;
		}

	}


	$('form').submit(function() {
		check_user_name();
		check_pwd();
		check_cpwd();
		check_email();
		check_phone();
		check_address();

		if(error_address == false && error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false && error_phone == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});








})
$(function(){
    $('#regist').click(function(){
        var email = $('#email').val();
        if(!email){
            $('#error_mes').html('邮箱不能为空');
            return false;
        }
        else if(!isValidMail(email)){
            $('#error_mes').html('请输入合法的邮箱地址');
            return false;
        }
    })       
})

function isValidMail(sText){
    var reMail = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    return reMail.test(sText)
}

var isGetVer
function name_filter(s){
    if(s.length == 0){
        return '请输入用户名！'
    }
    if(s.length > 15){
        return '用户昵称长度不得超过15位！'
    }
    if(/^\d{1,}$/.test(s)){
        return '用户名不能为全数字！'
    }
    var patt = /[\\\\/:*?\"<>|]/
    if(patt.test(s)){
        return '用户昵称含有非法字符！'
    }
    return ''
}

function phone_filter(s){
    if (s.length == 0){
        return '请输入手机号码！'
    }
    if(!(/^1[3456789]\d{9}$/.test(s))){
        return '手机号码有误！'
    }
    var check_phone = $.ajax({
        url:"/user/check_phone/",
        type:'post',
        'Content-Type':'application/json',
        data:JSON.stringify({
            'phone':s
        }),
        success:function(result) {
            $('#phone_err')[0].innerHTML = result
            return  result
        }
    })
    ret = check_phone.responseText
    if(ret != 'undefined') {
        return ret
    }
    return ''
}
function pwd_filter(s){
    if(s==0){
        return '请输入密码！'
    }
    if(s.length < 6){
        return '密码位数不得小于6位！'
    }
    if(s.length > 16){
        return '密码位数不得超过16位！'
    }


    // var s1 = '';
    return ''
}
function ver_filter(s){
    return ''
}
function checkVerCode(s){
    if($('.verification button')[0].innerHTML=='获取验证码'){
        return '未获取验证码！请获取验证码'
    }
    var check_vercode = $.ajax({
        url:"/user/check_vercode/",
        type:'post',
        'Content-Type':'application/json',
        data:JSON.stringify({
            'phone':s
        }),
        success:function(result) {
            $('#sub_err')[0].innerHTML = result
            return  result
        }
    })
    ret = check_vercode.responseText
    if(ret != 'undefined') {
        return ret
    }
    return ''
}
function toJSON(values){
    retJson = {}
    for(i=0;i<values.length;i++){
        retJson[values[i]['name']] = values[i]['value']
    }
    return retJson
}
 filters = {
    'nick_name':[name_filter,$('#name_err')[0]],
     'phone':[phone_filter,$('#phone_err')[0]],
     'password':[pwd_filter,$('#pwd_err')[0]],
     'ver_code':[ver_filter,$('#ver_err')[0]],
}

window.onload = function() {

    $('.input-text').blur(function () {
        val = $(this).val()
        id = $(this)[0].id
        err = filters[id][0](val)
        filters[id][1].innerHTML = err
    })
    function check(){
        // ver_err =checkVerCode($('.verification .input-text')[0].value)
        // if(ver_err!=''){
        //     $('#sub_err')[0].innerHTML=ver_err
        //     return false
        // }
        errs = $('.error-tip')
        for(i = 0;i < errs.length-1;i++){
            if(errs[i].innerHTML != ''){
                $('#sub_err')[0].innerHTML = '请按要求填写信息！'
                return false
            }
        }
        texts = ['昵称','手机号码','密码','验证码']
        inputs = $('.input-text')
        for(i = 0;i < inputs.length;i++){
            if(inputs[i].value == ''){
                $('#sub_err')[0].innerHTML = '请输入' + texts[i] + '！'
                return false
            }
        }
        return true
    }
    $('input.register')[0].onclick = function () {
        if( check()){
            // $('#reg_form')[0].submit()
            post_value = toJSON($("#reg_form").serializeArray())
            $.ajax({
                url:"/user/register/",
                type:'post',
                'Content-Type':'application/json',
                data:$("#reg_form").serialize(),
                dataType:'json',
                success:function(result) {
                    if(result['status'] == 200){
                        window.location.replace("/")
                    }else{
                        console.log(result)
                        err_fileds = ['phone','ver_code','password','nick_name']
                        err_tips = ['phone_err','ver_err','pwd_err','name_err']
                        for(i=0;i<err_fileds.length;i++){
                            err = result[err_fileds[i]]
                            console.log(err)
                            if(err != undefined){
                                $('#' + err_tips[i])[0].innerHTML = err[0]
                            }
                        }
                    }
                },
                error:function (msg) {
                    console.log(msg)

                }
            })

        }
        return false
    }
    var interval
    $('.verification button')[0].onclick = function () {
        $.ajax({
            url:"/user/verification/",
            type:'post',

        })
        $(this)[0].disabled=true
        $('#ver_err')[0].innerHTML = ''
        interval = setInterval(reckonTime,1000)

    }
    var Time = 60
    function reckonTime() {
        btn = $('.verification button')[0]
        list_t = /\d+/.exec(btn.innerHTML)

        if(list_t == null){
            btn.innerHTML = '重新发送（'+Time+'）'
            return
        }
        t = list_t[0]
        if(t > 0){
            t -= 1
            btn.innerHTML = '重新发送（'+t+'）'
        }else{
            btn.innerHTML = '重新发送'
            clearInterval(interval)
            btn.disabled = false
        }

    }
}
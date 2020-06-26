function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function () {
    $.get("/api/v1.0/users", function (resp) {
        if ("0" == resp.errno) {
            $("#user-name").val(resp.data.name);
            if (resp.data.avatar_url) {
                $("#user-avatar").attr("src", resp.data.avatar_url)
            }
        }
    });

    $("#form-avatar").submit(function (e) {
        // 阻止表单的默认行为
        e.preventDefault();
        // 利用jquery.form.min.js提供的ajaxSubmit对表单进行异步提交
        $(this).ajaxSubmit({
            url:"/api/v1.0/users/avatar",
            type:"post",
            dataType:"json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success:function (resp) {
                if ("0" == resp.errno){
                    // 上传成功
                    var avatarUrl = resp.data.avatar_url;
                    $("#user-avatar").attr("src",avatarUrl);
                } else {
                    alert(resp.errmsg)
                }
            }
        })
    });

    $("#form-name").submit(function (e) {
        // 阻止表单的默认行为
        e.preventDefault();
        var name = $("#user-name").val();
        if (!name) {
            alert("请填写用户名！");
            return
        }

        $.ajax({
            url: "/api/v1.0/users/" + name,
            type: "post",
            contentType:"application/json",
            dataType: "json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success:function (resp) {
                if ("0" == resp.errno) {
                    showSuccessMsg();
                    $(".error-msg").hide();
                    // location.href = "my.html"
                } else if ("4003" == resp.errno) {
                    $(".error-msg").show()
                } else if ("4101" == resp.errno){
                    alert(resp.errmsg);
                    location.href = "login.html";
                } else {
                    alert(resp.errmsg)
                }
            }
        })
    })
});

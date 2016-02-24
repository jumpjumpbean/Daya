/**
 * Created by nf on 7/15/2015.
 */

var ajaxLock = 0;

/*alert message*/
/*
 * type:normal/info/error/warning
 * timeout:milliseconds
 * */
var alertMsgHtml="<div class='modal ntf-modal in' id='_alertDialog'><div class='modal-dialog modal-sm'><div class='modal-content'>"
    +"<div class='modal-body'><button type='button' class='close' data-dismiss='modal' aria-hidden='true'>&times;</button><p class='rp'></p></div>"
    +"</div></div></div>";
function showMessage(msg, type, timeout, container) {
    var $dlg = $("#_alertDialog");
    if(!$dlg.html()){
        $container = container ? $(container) : $("body");
        $container.append(alertMsgHtml);
        $dlg = $("#_alertDialog");
    }
    type = type ? type : "normal";
    $dlg.addClass(type);
    $dlg.find("p").html(msg);
    $dlg.modal({keyboard:true,backdrop:false,show:true});
    if(timeout != "keep") {
        window.setTimeout(function(){
            $dlg.modal('hide');
        }, timeout?timeout:6000);
    }
    $dlg.on('hidden.bs.modal', function (e) {
        $dlg.remove();
    });
}

function passwordConfirm() {
    var pass = document.getElementById("pswdpop").value;
    var cfmpass = document.getElementById("confirmpop").value;
    if (pass == "") {
        showMessage("请输入新密码！", "error", "keep");
        return;
    }
    if (cfmpass == "") {
        showMessage("请再次输入新密码！", "error", "keep");
        return;
    }
    if (pass != cfmpass) {
        showMessage("两次输入的密码不一致，请重新输入！", "error", "keep");
        return;
    }
    $("#setPasswdDlg").modal("hide");
}

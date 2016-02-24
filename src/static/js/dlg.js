/**
 * 弹出确认dialog
 * @param msgContent 提示内容
 * @param type 消息类型
 */
function confirmDlg(msgContent, type, yesAction) {
	if(msgContent && msgContent.length>0) {
		if(!$('#_cfmDlg').html()){
			$("body").append("<div class='modal in' id='_cfmDlg'><div class='modal-dialog'><div class='modal-content'>"
					+"<div class='modal-header'><button type='button' class='close' data-dismiss='modal' aria-hidden='true'>&times;</button><h4 class='modal-title'>确认信息</h4></div>"
					+"<div class='modal-body'><p>"+msgContent+"</p></div>"
					+"<div class='modal-footer'><button type='button' id='_cfm_yes' class='btn btn-primary'>确定</button><button type='button' id='_cfm_cancel' class='btn btn-default' data-dismiss='modal'>取消</button></div></div></div></div>");
		}else{
			$('#_cfmDlg .modal-body').html(msgContent);
		}
		if(yesAction != undefined && typeof(yesAction) == "function") {
			$("#_cfm_yes").unbind("click");
			$("#_cfm_yes").bind("click",function() {
				$('#_cfmDlg').modal('hide');
				window.setTimeout(yesAction,100);
			});
		}
		if(type=='warning') {
			$("#_cfm_yes").attr("class","btn btn-danger");
		}else{
			$("#_cfm_yes").attr("class","btn btn-primary");
		}
		$('#_cfmDlg').modal({
			backdrop:'static',
			show:true
		});
	}
}
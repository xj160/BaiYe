window.onload = function() {
	layui.use('layer', function(){
  		var $ = layui.$ //由于layer弹层依赖jQuery，所以可以直接得到
  		,layer = layui.layer;

	  	//……
	  	// window.onresize = function(){
    //    		 $('header')[0].style.width = document.body.scrollWidth
    //    		 console.log(document.body.scrollWidth)
    //    		 console.log($('.inner-header')[0])
   	// 	}
    // 	window.onresize()
    	$(".seach-text").focus(function(){
 			$('.seach-bar form')[0].className = 'inputing'
		});
		$(".seach-text").blur(function(){

 			$('.seach-bar form')[0].className = ''
		});
		$('#login')[0].onclick = function () {
			$('#login-fram')[0].className = '';
		};
		$('.close-fram')[0].onclick = function () {
			$('#login-fram')[0].className = 'hide';
		};
		$('.pass-link')[0].onclick = function () {
			$('#phone-login')[0].className = 'hide'
			$('#pass-login')[0].className = 'login-content'
		};
		$('.phone-link')[0].onclick = function () {
			$('#pass-login')[0].className = 'hide'
			$('#phone-login')[0].className = 'login-content'
		}
	});

}
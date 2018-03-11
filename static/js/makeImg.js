/**
 * Created by leiruiqi on 2018/3/3.
 */

var baseinfo;
var http_url = "http://47.94.212.232:80/";
$("#imgloader input").change(function(event){
    $(".shadeBox").fadeIn();
    var oFile = event.target.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(oFile);

    // EXIF.getData(file, function() {
    //     // alert(EXIF.pretty(this));
    //     EXIF.getAllTags(this);
    //     //alert(EXIF.getTag(this, 'Orientation'));
    //     Orientation = EXIF.getTag(this, 'Orientation');
    //     //return;
    // });
    reader.onload = function(e){
        baseinfo = this.result.substring(this.result.indexOf(',')+1);
        sendImg('save_img');
    }
});

function sendImg(url){
    var obj = {
        str:baseinfo
    };
    $.ajax({
        type:'post',
        url:http_url+url,
        data:obj,
        success:function(data){
            if(data.code!=200){
                alert("网络延迟，请稍后尝试～");
            }else{
                $(".shadeBox").fadeOut();
                $(".imgContent").fadeOut();
                window.setTimeout(function(){
                    $(".saveImg").show();
                    $("#myImg").fadeIn();
                    creatImg(data.file);
                    $(".tagImg").show();
                },600);
            }
        },
        error:function(){
            alert("网络延迟，请稍后尝试～");
        },
        dataType:'json'
    });
}

function creatImg(tsrc){
    $("#myImg").html(
        "<img id='mainPhoto' class='photo' src='"+tsrc+"' crossOrigin='anonymous'>"
    );
}

$(".tagType").click(function(){
    for(var i=0; i<$(".tagType").length; i++){
        $(".typeBox .typeltem").eq(i).removeClass("showHeight");
    }
    $(".typeBox .typeltem").eq($(this).index()).addClass("showHeight");
});

$(".filter div").click(function(){

   $(this).addClass("check").siblings().removeClass("check");
    if($(".shadeImg").length){
        $(".shadeImg").attr('src',$(this).children("img").attr('src'));
    }else{
        $("#myImg").prepend("<img src='"+$(this).children("img").attr('src')+"' class='shadeImg absol'>");
    }
    window.setTimeout(function(){
       $(".shadeImg").css({'width':$("#myImg").width(),'height':$("#myImg").height()});
    },500);
});
$(".paper div").click(function(){
   if($(".opaperImg").length<=5){
       if($(this).index()<=3){
           $("#myImg").prepend(
               "<div class='opaperImg absol'>"+
               "<div class='real'><img src='img/close.png' class='absol closeImg' ></div>"+
               "<img src='"+$(this).children("img").attr('src')+
               "' class='tpaper'></div>");
       }else if($(this).index()>3&&$(this).index()<=9){
           $("#myImg").prepend(
               "<div class='opaperImg absol'>"+
               "<div class='real'><img src='img/close.png' class='absol closeImg' ></div>"+
               "<img src='"+$(this).children("img").attr('src')+
               "' class='mpaper'></div>");
       }else if($(this).index()==11){
           $("#myImg").prepend(
               "<div class='opaperImg absol'>"+
               "<div class='real'><img src='img/close.png' class='absol closeImg' ></div>"+
               "<img src='"+$(this).children("img").attr('src')+
               "' class='stpaper'></div>");
       }else{
           $("#myImg").prepend(
               "<div class='opaperImg opaperText absol'>"+
               "<div class='real'><img src='img/close.png' class='absol closeImg' ></div>"+
               "<img src='"+$(this).children("img").attr('src')+
               "' class='bigpaper'></div>");
       }
       $(".tpaper").on('load',function(){
           zzd("opaperImg","myImg");
           //
       });
       $(".mpaper").on('load',function(){
           zzd("opaperImg","myImg");
       });
       $(".stpaper").on('load',function(){
           zzd("opaperImg","myImg");
       });
       $(".bigpaper").on('load',function(){
           zzd("opaperImg","myImg");
       });
       window.setTimeout(function(){
           $(".opaperImg").eq(0).addClass("opaperImgCheck").siblings().removeClass("opaperImgCheck");
           $(".textPaper").removeClass("opaperImgCheck");
           $(".closeImg").on("click",function(){
               $(this).parent().parent().remove();
           });
           $(".opaperImg img").on('click',function(){
               $(".textPaper").removeClass("opaperImgCheck");
               $(this).parent().addClass("opaperImgCheck").siblings().removeClass("opaperImgCheck");
           });
       },500);
   }else{
       alert("最多添加6张贴纸");
   }
});

function opaperFocs(othis){
    $(".textPaper").removeClass("opaperImgCheck");
    $(".opaperImg").eq(othis).addClass("opaperImgCheck").siblings().removeClass("opaperImgCheck");
}

$(".oinput").bind('input propertychange', function() {
    if($.trim($(this).val()).length!=0){
        $("#addtbox").addClass("btnClick");
    }else{
        $("#addtbox").removeClass("btnClick");
    }
});

var textColor = "<div class='textPaper absol'>";
$("#addtbox").click(function(){
   if($(this).hasClass("btnClick") && ($(".textPaper").length==0)){
       $("#deltbox").addClass("deltbox");
       $("#myImg").prepend(
           textColor+
           "<div class='real'><img src='img/close.png' class='absol closeText' ></div>"+
           $.trim($(".oinput").val())+
           "</div>");
       window.setTimeout(function(){
           zzd("textPaper","myImg");

           $(".textPaper").addClass("opaperImgCheck");
           $(".opaperImg").removeClass("opaperImgCheck");
           $("#addtbox").removeClass("btnClick");
           $("#deltbox").addClass("btnClick");
           $(".closeText").on("click",function(){
               $(this).parent().parent().remove();
               $("#addtbox").addClass("btnClick");
               $("#deltbox").removeClass("btnClick");
           });
       },500);
   }
});
$("#deltbox").click(function(){
    if($(this).hasClass("btnClick") && ($(".textPaper").length==1)){
        $(".textPaper").remove();
        $("#addtbox").addClass("btnClick");
        $("#deltbox").removeClass("btnClick");
    }
});
$(".textColor p").click(function(){
    $(this).addClass("checkP").siblings().removeClass("checkP");
    if($(this).index()==0){
        textColor = "<div class='textPaper absol' style='color:#e61010'>";
        $(".textPaper").css('color','#e61010');
    }else if($(this).index()==1){
        textColor = "<div class='textPaper absol' style='color:#107ee6'>";
        $(".textPaper").css('color','#107ee6');
    }else if($(this).index()==2){
        textColor = "<div class='textPaper absol' style='color:#10e66b'>";
        $(".textPaper").css('color','#10e66b');
    }
});

function zzd(obj,parent){
    var block = document.getElementsByClassName(obj)[0];
    var oparent = document.getElementById(parent);
    var oW,oH;
    // 绑定touchstart事件
    block.addEventListener("touchstart", function(e) {
        var touches = e.touches[0];
        oW = touches.clientX - block.offsetLeft;
        oH = touches.clientY - block.offsetTop;
        //阻止页面的滑动默认事件
        document.addEventListener("touchmove",defaultEvent,false);
    },false)

    block.addEventListener("touchmove", function(e) {
        var touches = e.touches[0];
        var oLeft = touches.clientX - oW;
        var oTop = touches.clientY - oH;
        if(oLeft < 0) {
            oLeft = 0;
        }else if(oLeft > oparent.offsetHeight - block.offsetWidth) {
            oLeft = (oparent.offsetHeight - block.offsetWidth);
        }else if(oTop < 0){
            oTop = 0;
        }else if(oTop > oparent.offsetHeight-block.offsetHeight){
            oTop = (oparent.offsetHeight - block.offsetHeight);
        }
        block.style.left = oLeft + "px";
        block.style.top = oTop + "px";
    },false);

    block.addEventListener("touchend",function() {
        document.removeEventListener("touchmove",defaultEvent,false);
    },false);
    function defaultEvent(e) {
        e.preventDefault();
    }
}

$(".saveImg").click(function(){
    $(".shadeBox").fadeIn();
    $(this).hide();
    $(".textPaper").removeClass("opaperImgCheck");
    $(".opaperImg").removeClass("opaperImgCheck");
    $(".tagImg").fadeOut();
    var MaxWImg = ($("#mainPhoto").width());
    var MaxHImg = ($("#mainPhoto").height());
    html2canvas(document.getElementById("myImg"),{
        allowTaint:true,
        useCORS: true
    }).then(function(canvas) {
        $("#myImg").empty();
        $(".content").css("padding",0);

        var canvasUrl = canvas.toDataURL();
        console.log(canvasUrl);
        canvasUrl = canvasUrl.substring(canvasUrl.indexOf(',')+1);
        var formImg = {
            str:canvasUrl
        }
        $.ajax({
            url:http_url+'save_img_end',
            type: 'POST',
            data: formImg,
            success: function (data) {
                if(data.code!=200){
                    alert("网络延迟，请稍后尝试～");
                }else{
                    $(".shadeBox").fadeOut();
                    $("#myImg").html(
                        "<img class='photo' src='"+data.file+"' >"+
                        "<div class='textInfo'>制作完成，长按图片保存本地</div>"
                    );
                }
            },
            error: function () {
                alert("网络延迟，请稍后尝试～");
            },
            dataType:'json'
        });
    });
});







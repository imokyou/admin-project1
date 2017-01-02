/**
 * Created by sin on 2016/11/21.
 */
$(function () {
/*    $(".nav_bar a").on("click", function () {
        $(this).addClass("on").parents("li").siblings("li").find("a").removeClass("on");
        $(this).children("i").removeClass("icon_nav01").addClass("icon_nav02").parents("li").siblings("li").find("i").removeClass("icon_nav02").addClass("icon_nav01")
        });*/
    $(".nav_bar a").each(function(){
        $this = $(this);
        if($(this)[0].href==String(window.location)){
            $(this).addClass("on").parents("li").siblings("li").find("a").removeClass("on");
            $(this).children("i").removeClass("icon_nav01").addClass("icon_nav02").parents("li").siblings("li").find("i").removeClass("icon_nav02").addClass("icon_nav01")
        }
    });

    $(".dashboard_tab > li").on("click",function(){
        $(this).find("span").addClass("blue").end().siblings("li").find("span").removeClass("blue")
    });
   /* 左侧导航*/
    $(".left_nav li").on("click",function(){
        $(this).find("h5").addClass("in").end().siblings("li").find("h5").removeClass("in");
        $(this).find("dl").slideDown().end().siblings("li").find("dl").slideUp()
    });

    $(".left_nav li dl dd").on("click",function(){
        $(this).find("a").addClass("ck").end().siblings("dd").find("a").removeClass("ck");
        $(this).parents("li").siblings("li").find("a").removeClass("ck")
    });

    <!--点击投票按钮弹出层-->
    $(".vote_before").on('click',function(){
        $(this).parents(".vote_item").find(".vote_tip").show()
    });
    $('.close_voteTip').on('click',function(){
        $('.vote_tip').hide()
    });

    /*交易所表*/

});


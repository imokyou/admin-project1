/**
 * Created by sin on 2016/11/21.
 */
$(function () {
/*    $(".nav_bar a").on("click", function () {
        $(this).addClass("on").parents("li").siblings("li").find("a").removeClass("on");
        $(this).children("i").removeClass("icon_nav01").addClass("icon_nav02").parents("li").siblings("li").find("i").removeClass("icon_nav02").addClass                ("icon_nav01")
    });
    $(".dashboard_tab > li").on("click",function(){
        $(this).find("span").addClass("blue").end().siblings("li").find("span").removeClass("blue")
    });*/
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
    var myChart = echarts.init(document.getElementById('graph'));
    option = {
        backgroundColor: '#fff',
        title: {
            text: "XXX走势图"
        },
        grid: {
            left: '0',
            right: '10px',
            top:'35px',
            bottom: '0',
            containLabel: true
        },
        tooltip : {
            trigger: 'axis'
        },
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : ['9/1','9/2','9/3','9/4','9/5','9/6','9/7','9/8','9/9','9/10','9/11']
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel : {
                    formatter: '{value}万元'
                }
            }
        ],
        series: [
            {
                name:'数值',
                type:'line',
                itemStyle : {
                    normal : {
                        color:'#f5bf58',
                        lineStyle:{
                            color:'#000'
                        }
                    }
                },
                data:[0.3, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.05],
                formatter: '{data}万元'
            }
        ]
    };
    myChart.setOption(option);
});


$(function(){

    $(".backgroundSlider #backgroundImages").supersized({
        slide_interval:4e3,
        transition:1,
        transition_speed:900,
        slide_links:!1,
        slides:[
            {
                image:"images/bg1.jpg",
                title:"",
                thumb:"",
                url:""
            },
            {
                image:"images/bg2.jpg",
                title:"",
                thumb:"",
                url:""
            },
            {
                image:"images/bg3.jpg",
                title:"",
                thumb:"",
                url:""
            },
            {
                image:"images/bg4.jpg",
                title:"",
                thumb:"",
                url:""
            }
        ]
    });

    var e=!1;

    $(window).width()>=992&&(e=!0, $("#bgndVideo").mb_YTPlayer()), $("#text_slider").cycle({
        fx:"fade",
        timeout:4e3,
        speed:900,
        slides:".slide"
    });

    $("#text_slider2").cycle({
        fx:"fade",
        timeout:4e3,
        speed:900,
        slides:".slide"
    });

    $("#text_slider3").cycle({
        fx:"fade",
        timeout:4e3,
        speed:900,
        slides:".slide"
    });

    $("#countdown").countdown({
        until:someDate,padZeroes:!0, layout:$("#countdown").html()
    });

    $(".open_aboutus").click(function(){
        $("#about_us").removeClass("animated fadeOut").addClass("animated fadeIn").fadeIn();
        return false;
    });

    $(".close_aboutus").click(function(){
        $("#about_us").removeClass("animated fadeIn").addClass("animated fadeOut").fadeOut();
        return false;
    });
});

var someDate=new Date(2016,7,11,9,0,0);
//someDate.setDate(someDate.getDate()+rango);
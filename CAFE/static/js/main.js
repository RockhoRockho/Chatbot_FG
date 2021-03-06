const spyEls = document.querySelectorAll('.scroll-spy');
spyEls.forEach(function (spyEl) {
    new ScrollMagic.Scene({
            // 감시할 장면(Scene)을 추가
            triggerElement: spyEl, // 보여짐 여부를 감시할 요소를 지정
            triggerHook: 0.3, // 화면의 80% 지점에서 보여짐 여부 감시
        })
        .setClassToggle(spyEl, 'show') // 요소가 화면에 보이면 show 클래스 추가
        .addTo(new ScrollMagic.Controller()); // 컨트롤러에 장면을 할당(필수!)
});

function goTop() {
    $('html').scrollTop(0);
}


// 실시간 디지털시계
const clock = document.querySelector(".h1");

function getClock() {
    const d = new Date();
    const h = String(d.getHours()).padStart(2, "0");
    const m = String(d.getMinutes()).padStart(2, "0");
    const s = String(d.getSeconds()).padStart(2, "0");
    clock.innerText = `${h}:${m}:${s}`;
}

getClock(); //맨처음에 한번 실행
setInterval(getClock, 1000); //1초 주기로 새로실행


// 메뉴 설명 탭
function openTab(tabName) {
    var i, tabcontent;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    document.getElementById(tabName).style.display = "block";
}

// $(function(){
//     $('.tab1 > div').click(function(){
//         $('.tab1 > div').removeClass()
//         $(this).addClass('on')
//     })
// })



// $(document).scroll(function(){
//     var con = $("#remoCon");
//     var position = $(window).scrollTop();
//     if(position > 250){
//         con.fadeIn(500);
//     }	
//     else if(position < 250){
//         con.fadeOut(500);
//     }
// });
// $("#remoCon").click(function(){
//     $("html, body").animate({scrollTop: 0}, 1000);
// });

function goTop() {
    $('html').scrollTop(0);
}




// 챗봇 모달창
$(function () {

    $(".bot").click(function () {
        $(".modal").fadeIn();
    });

    $(".exit").click(function () {
        $(".modal").fadeOut();
    });


    // $(document).on("click", function(e){
    //     if($(".modal").is(e.target)){
    //         $(".modal").fadeOut();
    //     }
    // });
});



var aud1 = document.getElementById("audio1");
var vid1 = document.getElementById("video1");
var aud2 = document.getElementById("audio2");
var vid2 = document.getElementById("video2");
var aud3 = document.getElementById("audio3");
var vid3 = document.getElementById("video3");
var aud4 = document.getElementById("audio4");
var vid4 = document.getElementById("video4");
var fgcafe = document.getElementById("fgcafe")
var time = document.getElementById("time")
aud1.onplay = function() {
    vid1.style.display='block';
    vid2.style.display='none';
    vid3.style.display='none';
    vid4.style.display='none';
    aud2.pause();
    aud3.pause();
    aud4.pause();
    fgcafe.style.fontFamily = 'SBAggroB'
    time.style.fontFamily = 'SBAggroB'
    fgcafe.style.fontSize = '80px';
    time.style.fontSize = '60px';
};
aud2.onplay = function() {
    vid2.style.display='block';
    vid1.style.display='none';
    vid3.style.display='none';
    vid4.style.display='none';
    aud1.pause();
    aud3.pause();
    aud4.pause();
    fgcafe.style.fontFamily = 'elsie';
    time.style.fontFamily = 'elsie';
    fgcafe.style.fontSize = '90px';
    time.style.fontSize = '70px';
};
aud3.onplay = function() {
    vid3.style.display='block';
    vid2.style.display='none';
    vid1.style.display='none';
    vid4.style.display='none';
    aud2.pause();
    aud1.pause();
    aud4.pause();
    fgcafe.style.fontFamily = 'CartooNature';
    time.style.fontFamily = 'CartooNature';
    fgcafe.style.fontSize = '100px';
    time.style.fontSize = '80px';
};
aud4.onplay = function() {
    vid4.style.display='block';
    vid2.style.display='none';
    vid3.style.display='none';
    vid1.style.display='none';
    aud2.pause();
    aud3.pause();
    aud1.pause();
    fgcafe.style.fontFamily = 'ocean-sunshine'
    time.style.fontFamily = 'ocean-sunshine'
    fgcafe.style.fontSize = '80px';
    time.style.fontSize = '60px';
};



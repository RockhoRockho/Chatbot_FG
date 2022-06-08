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
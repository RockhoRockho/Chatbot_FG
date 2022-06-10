$(function(){
    // SEND 버튼을 누르거나
    $("#sendbtn").click(function(){
        send_message();
    }); 

    // ENTER key 가 눌리면
    $("#chattext").keyup(function(event){
        if(event.keyCode == 13){
            send_message()
        }
    })

})

$(function(){
    // 이미지 슬라이드 컨트롤를 사용하기 위해서는 carousel를 실행해야한다.
    $('#carousel-example-generic').carousel({
        // 슬리아딩 자동 순환 지연 시간
        // false면 자동 순환하지 않는다.
        interval: 1000,
        // hover를 설정하면 마우스를 가져대면 자동 순환이 멈춘다.
        pause: "hover",
        // 순환 설정, true면 1 -> 2가면 다시 1로 돌아가서 반복
        wrap: true,
        // 키보드 이벤트 설정 여부(?)
        keyboard : true
    });	
});


function send_message(){
    const chattext = $("#chattext").val().trim();

    // 입력한 메세지가 없으면 리턴
    if(chattext == ""){
        $("#chattext").focus();
        return;
    }

    // 입력한 채팅 화면에 출력
    const addtext = "<div style='margin:15px 0;text-align:right;'> <span style='padding:8px 13px;background-color:#c08552;color:white;border-radius:3px;display:inline-block;font-weight:bold;'>" +
    chattext + "</span></div>";

    // 먼저 입력했던 것은 지우기
    $("#chattext").val("");
    $("#chattext").focus();

    // API 서버에 요청할 데이터
    const jsonData = {
        query: chattext,
        user: sessionStorage.getItem('User'),
    }

    $.ajax({
        url: 'http://127.0.0.10:5000/query/ProjectFG_Cafe',
        type: "POST",
        data: JSON.stringify(jsonData),
        dataType: "JSON",   // 응답받을 데이터 타입
        contentType: "application/json; charset=utf-8",
        crossDomain: true,

        success: function(response){
            // 답변텍스트는 response.Answer 에 담겨 있다

            $chatbox = $("#chatbox");

            if (response.Intent == '메뉴'){ 

                const bottext1 = 
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color: #F5F5DC;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                    response.Answer[i] + "</div></div>"; +

                    "<div style='width: 300px;margin: 100px;'>" + 
                    "<div id='carousel-example-generic' class='carousel slide' >" + '<ol class="carousel-indicators">' +
                    '<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>' +
                    '<li data-target="#carousel-example-generic" data-slide-to="1"></li>' +
                    '</ol><div class="carousel-inner" role="listbox"><div class="item active">' +
                    '<img src="https://tistory2.daumcdn.net/tistory/1041549/skin/images/nowonbuntistory.png" style="width:100%">' +
                    '<div class="carousel-caption" style="color:black;">설명글</div></div>' + 
                    '<div class="item"><img src="https://www.nowonbun.com/img/nowonbuntistory1.png" style="width:100%">' +
                    '<div class="carousel-caption" style="color:black;"></div></div></div>' +
                    '<a class="left carousel-control" href="#carousel-example-generic" role="button" data-slide="prev">' +
                    '<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span></a>' +
                    '<a class="right carousel-control" href="#carousel-example-generic" role="button" data-slide="next">' +
                    '<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span></a></div></div>'

                $chatbox.append(bottext);

            // 답변 출력
            if (response.Intent == '메뉴'){ // 상품 리스트 뽑을 때
                for (let i = 0; i < response.AnswerImageUrl.length; i++){
                    const bottext =
                        "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color: #386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                        response.Answer[i] + "<image src='/static/img/" + response.AnswerImageUrl[i] + "'></image>"+ response.Detail[i] +
                        "</div></div>";
                    $chatbox.append(bottext);
                }
            }   else if (response.Intent == '메뉴판 요구' && response.AnswerImageUrl != null){ //메뉴판 뽑을 때
                const bottext =
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                    "<image style='width:450px' src='/static/img/" + response.AnswerImageUrl + "'></image>" + 
                    "</div></div>";
                $chatbox.append(bottext);
            }  else if (response.Intent == '주문' && response.AnswerImageUrl != null){ //상품 하나 뽑을 때
                const bottext =
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                    response.Answer + "<image src='/static/img/" + response.AnswerImageUrl + "'></image>" + response.Detail +
                    "</div></div>";
                $chatbox.append(bottext);
            }  else { // 텍스트만 뽑을 때
                const bottext =
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                    response.Answer +
                    "</div></div>";
                $chatbox.append(bottext);
            }

            $('#kakaopay').click(function (){
                    location.href = "chatbot/kakaopay/";
                })

            // 스크롤 조정하기
            $chatbox.animate({scrollTop: $chatbox.prop('scrollHeight')})

            
        }

    }
});



}
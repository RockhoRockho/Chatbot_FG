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

function send_message(){
    const chattext = $("#chattext").val().trim();

    // 입력한 메세지가 없으면 리턴
    if(chattext == ""){
        $("#chattext").focus();
        return;
    }

    // 입력한 채팅 화면에 출력
    const addtext = "<div style='margin:15px 0;text-align:right;'> <span style='padding:3px 10px;background-color:#3388cc;border-radius:3px;'>" + chattext + "</span></div>";
    $("#chatbox").append(addtext);

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

            // 답변 출력
            if (response.Intent == '메뉴'){ // 상품 리스트 뽑을 때
                for (let i = 0; i < response.AnswerImageUrl.length; i++){
                    const bottext =
                        "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#DDD;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                        response.Answer[i] + "<image src='/static/img/" + response.AnswerImageUrl[i] + "'></image>"+ response.Detail[i] +
                        "</div></div><br>";
                    $chatbox.append(bottext);
                }
            }  else if (response.Intent == '주문' && response.AnswerImageUrl != null){ //상품 하나 뽑을 때
                const bottext =
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#DDD;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                    response.Answer + "<image src='/static/img/" + response.AnswerImageUrl + "'></image>" + response.Detail +
                    "</div></div>";
                $chatbox.append(bottext);
            }  else{ // 텍스트만 뽑을 때
                const bottext =
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#DDD;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
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

    });



}
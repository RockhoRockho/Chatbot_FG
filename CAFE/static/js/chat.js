$(document).ready(function(){
    // 가장 처음 작동
    const bottext ="<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
        "어서오세요. FG카페입니다~<br>무엇을 도와드릴까요?" + "</div></div>" +
        "<button class='bb' id='all' style='width:23.5%; border-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; height:30px; border-radius:5px; margin-bottom:2%;border:none;'>전체메뉴</button>" +
        "<button class='bb' id='por' style='width:23.5%; background-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; height:30px; border-radius:5px; margin-bottom:2%;border:none;'>인기메뉴</button>" +
        "<button class='bb' id='ord' style='width:23.5%; background-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; height:30px; border-radius:5px; margin-bottom:2%;border:none;'>주문내역</button>" +
        "<button class='bb' id='req' style='width:23.5%; background-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; height:30px; border-radius:5px; margin-bottom:2%;border:none;'>할인</button>" +
        "<button class='bb' id='que' style='width:23.5%; background-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; height:30px; border-radius:5px; margin-bottom:2%;border:none;'>추천메뉴</button>" +
        "<button class='bb' id='ori' style='width:23.5%; background-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; height:30px; border-radius:5px; margin-bottom:2%;border:none;'>원산지</button>"

    $("#chatbox").append(bottext);

    $chatbox.animate({scrollTop: $chatbox.prop('scrollHeight')})

})


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
    });

    $("#all").click(function (){
        $("#chattext").val('전체메뉴')
        $("#sendbtn").trigger('click')
    });
    $("#por").click(function (){
        $("#chattext").val('인기메뉴')
        $("#sendbtn").trigger('click')
    });
    $("#ord").click(function (){
        $("#chattext").val('주문내역')
        $("#sendbtn").trigger('click')
    });
    $("#req").click(function (){
        $("#chattext").val('할인')
        $("#sendbtn").trigger('click')
    });
    $("#que").click(function (){
        $("#chattext").val('와이파이 및 시설')
        $("#sendbtn").trigger('click')
    });
    $("#ori").click(function (){
        $("#chattext").val('원산지')
        $("#sendbtn").trigger('click')
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

            if (response.Intent == '메뉴' || response.Intent == '추천메뉴 검색'){ 

                var bottext1 = 
                    "<div style='width:70%;margin: 10px;'>" + 
                    "<div id='carousel-example-generic' class='carousel slide' >" +
                    '<div class="carousel-inner" role="listbox">' + 
                    '<div class="item active" style="color:black; font-size:20px; font-weight:bold;">' + response.Answer[0] + 
                    '<image src="/static/img/' + response.AnswerImageUrl[0] + '" style="width:100%"></image>' +
                    '<div class="carousel-caption" style="color:black; text-shadow:None; font-size:14px; position:relative; right:0%; left:0%">' + response.Detail[0] + '</div></div>'

                var bottext2 = ''
                for (let i = 1; i < response.AnswerImageUrl.length; i++){
                    bottext2 += '<div class="item" style="color:black; font-size:20px; font-weight:bold;">' + response.Answer[i] +
                    '<image src="/static/img/' + response.AnswerImageUrl[i] + '" style="width:100%"></image>' +
                    '<div class="carousel-caption" style="color:black; text-shadow:None; font-size:14px; position:relative; right:0%; left:0%">' + response.Detail[i] + '</div></div>'
                }
                var bottext3 =
                    '</div><a class="left carousel-control" style="background-image:None;" href="#carousel-example-generic" role="button" data-slide="prev">' +
                    '<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span></a>' +
                    '<a class="right carousel-control" style="background-image:None;" href="#carousel-example-generic" role="button" data-slide="next">' +
                    '<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span></a></div></div>' +
                    '<script>$(function(){$("#carousel-example-generic").carousel({interval: 1000, pause: "hover", wrap: true, keyboard : true});});</script>'

                var bottext = bottext1 + bottext2 + bottext3

                $chatbox.append(bottext);

            // 답변 출력
            }   else if (response.Intent == '주문내역'){
                var ordernum = Object.keys(response.Answer)
                var orderproduct = Object.values(response.Answer)
                
                var bottext1 =
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>"
                var bottext2 = '<br>주문내역<hr>'
                for (let i = 0; i < ordernum.length; i++){
                    bottext2 += '주문번호 : ' + ordernum[i] + '<br>상품이름 : ' + orderproduct[i] + '<hr>'
                }
                var bottext = bottext1 + bottext2 + "</div></div>";
                $chatbox.append(bottext);

            }   else if (response.Intent == '메뉴'){ // 상품 리스트 뽑을 때
                for (let i = 0; i < response.AnswerImageUrl.length; i++){
                    var bottext =
                        "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color: #386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                        response.Answer[i] + "<image src='/static/img/" + response.AnswerImageUrl[i] + "'></image>"+ response.Detail[i] +
                        "</div></div>";
                    $chatbox.append(bottext);
                }
            }   else if (response.Intent == '메뉴판 요구' && response.AnswerImageUrl != null){ //메뉴판 뽑을 때
                var bottext =
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                    response.Answer + "<image style='width:450px' src='/static/img/" + response.AnswerImageUrl + "'></image>" + 
                    "</div></div>";
                $chatbox.append(bottext);
            }   else if (response.Intent == '처음으로'){ // 초기화면
                    $chatbox.append(response.Answer);
            }  else if (response.Intent == '주문' && response.AnswerImageUrl != null){ //상품 하나 뽑을 때
                var bottext =
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                    "<image src='/static/img/" + response.AnswerImageUrl + "'></image>" + response.Detail + '&emsp;' + response.Price + '원' +
                    "</div></div>" +
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                    response.Answer + "</div></div>" + 
                    "<div style='margin-top: -25px; padding-top: 0; text-align:left; max-width:70%; background-color: rgba(0, 0, 0, 0); font-weight:bold;'>" + 
                    "<br><button class='bb'; id='One' style='width:23.5%; background-color: #386641; color:white; margin-right:2%; height:30px; border-radius:5px; margin-bottom:2%; border:none;'>1번</button>" +
                    "<button class='bb' id='Two' style='width:23.5%; background-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; height:30px; border-radius:5px; margin-bottom:2%;border:none;'>2번</button>" +
                    "<button class='bb' id='Three' style='width:23.5%; background-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; margin-bottom:2%;border:none;'>3번</button>" +
                    "<button class='bb' id='Four' style='width:23.5%; background-color: #386641; color:white; height:30px; border-radius:5px; margin-top:-2%;border:none;'>4번</button>" +
                    "<button class='bb' id='Five' style='width:23.5%; background-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; margin-bottom:2%;margin-bottom:2%;border:none;'>5번</button>" +
                    "<button class='bb' id='Six' style='width:23.5%; background-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; margin-bottom:2%;border:none;'>6번</button>" +
                    "<button class='bb' id='Seven' style='width:23.5%; background-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; margin-bottom:2%;border:none;'>7번</button>" +
                    "<button class='bb' id='Eight' style='width:23.5%; background-color: #386641; color:white; height:30px; border-radius:5px; margin-top:-2%;border:none;'>8번</button>" +
                    "<button class='bb' id='cart' style='width:49%; background-color: #386641; color:white; margin-right:1%; height:30px; border-radius:5px; margin-right:2%; margin-bottom:2%;border:none;'>장바구니</button>" +
                    "<button class='bb' id='choice' style='width:49%; background-color: #386641; color:white;height:30px; border-radius:5px;margin-top:-2%;border:none;'>선택완료</button></div>" +
                    "<script>$('#One').click(function(){send_option(1)});" +
                    "$('#Two').click(function(){send_option(2)});" +
                    "$('#Three').click(function(){send_option(3)});" +
                    "$('#Four').click(function(){send_option(4)});" +
                    "$('#Five').click(function(){send_option(5)});" +
                    "$('#Six').click(function(){send_option(6)});" +
                    "$('#Seven').click(function(){send_option(7)});" +
                    "$('#Eight').click(function(){send_option(8)});" +
                    "$('#cart').click(function(){send_option('장바구니')});" +
                    "$('#choice').click(function(){send_option('선택완료')});" +
                    "$(function(){$(document).ready(function(){$('.bb').hover(function(){$(this).css('background-color','#81c147');},function(){$(this).css('background-color','#386641');});});})</script>";
                $chatbox.append(bottext);
            }  else if (response.Intent == '원산지' && response.AnswerImageUrl != null){ //상품 하나 뽑을 때
                var image = response.AnswerImageUrl.split(', ')
                var bottext = 
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                    response.Answer + "</div></div>" +
                    "<div style='width:70%;margin: 10px;'>" + 
                    "<div id='carousel-example-generic' class='carousel slide' >" +
                    '<div class="carousel-inner" role="listbox">' + 
                    '<div class="item active">' +
                    '<image src="/static/img/' + image[0] + '" style="width:100%"></image></div>' +
                    '<div class="item">' +
                    '<image src="/static/img/' + image[1] + '" style="width:100%"></image></div>' +
                    '<div class="item">' +
                    '<image src="/static/img/' + image[2] + '" style="width:100%"></image></div>'+
                    '</div><a class="left carousel-control" style="background-image:None;" href="#carousel-example-generic" role="button" data-slide="prev">' +
                    '<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span></a>' +
                    '<a class="right carousel-control" style="background-image:None;" href="#carousel-example-generic" role="button" data-slide="next">' +
                    '<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span></a></div></div>' +
                    '<script>$(function(){$("#carousel-example-generic").carousel({interval: 1000, pause: "hover", wrap: true, keyboard : true});});</script>'

                $chatbox.append(bottext);
            }  else { // 텍스트만 뽑을 때
                var bottext =
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                    response.Answer +
                    "</div></div>";
                $chatbox.append(bottext);
            };

            
            

            $('#kakaopay').click(function (){
                    location.href = "chatbot/kakaopay/";
            });

            // 스크롤 조정하기
            $chatbox.animate({scrollTop: $chatbox.prop('scrollHeight')})

            
        }

    })
};


function send_option(optionNm){
    // API 서버에 요청할 데이터
    const jsonData = {
        query: optionNm,
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

            $chatbox = $("#chatbox");

            var bottext =
                    "<div style='margin:15px 0;text-align:left; max-width:70%;'><div style='padding:3px 10px;background-color:#386641;color:white;border-radius:3px; display:inline-block; word-break: keep-all;'>" +
                    "👉옵션" + optionNm + "번👈을 선택하셨습니다.<br><br>" +
                    "주문을 하시려면 ⭕선택완료⭕를<br>"+
                    "다른 상품을 더 담으시려면 🤜장바구니🤛를<br>" +
                    "옵션을 변경하시려면 위에 ◼숫자◼버튼을<br>" +
                    "초기화면으로 돌아가시려면<br>❌처음으로❌를 입력해주세요" +
                    "</div></div>"
                    
                $chatbox.append(bottext);

            
            $('#kakaopay').click(function (){
                location.href = "chatbot/kakaopay/";
            });
    
            // 스크롤 조정하기
            $chatbox.animate({scrollTop: $chatbox.prop('scrollHeight')})
    
        }
    })
}
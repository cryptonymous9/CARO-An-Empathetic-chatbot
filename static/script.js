
//"http://18.219.111.242:1337/"   directly to server
//"http://localhost:9000/api-server/"  proxy pass to aws server
//"http://localhost:9000/api-local/"   proxy pass to local server
// var accessToken = "ca0ab94c7104450ea34585ee8a7a00b8";
// var serverbaseUrl = "http://localhost:9000/api-local/";
// var dialogbaseUrl = "https://api.api.ai/v1/";


// var username, email;

//define chat color
// if (typeof(Storage) !== "undefined") 
// {
//   if (localStorage.getItem('fab-color') === null) 
//   {
//     localStorage.setItem("fab-color", "blue");
//   }
//   $('.fabs').addClass(localStorage.getItem("fab-color"));
// } else {
//   $('.fabs').addClass("blue");
// }


// $('#fab_feedback').hide();
// $('#namelogin').hide();
// $('#close').hide();
// $('#feedback').hide();

//feedbackicon
// $('#fab_feedback').click(function() {
//   $('#feedback').show();
//   hideChat(true);
//   $('#chat_loader').hide();
//   $('#close').show();
//   toggleFab1();
// });

var rate;
 $(':radio').change(function() {
      rate= this.value;
      console.log(rate)
  });


 $('#submit-rf').on("click", function(){

  var payload = {
       "feedback":$('#chat_log_feedback').val(),
       "rating":rate,

      };
    console.log(payload);
    sendAJAXRequest('sendFeedback',"POST", payload,  function(data, status){
            console.log(payload);
            console.log(data);
            if(data && data.success){
              console.log("success");
            }
            else if(data && !data.success){
              if(data.message){
                console.log("failure");
                }
              }
      })
    
});

//closefeedback
$('#close').click(function() {
  $('#feedback').hide();
  hideChat(false);
  $('#chat_loader').show();
  $('#close').hide();
});

//Fab click
$('#prime').click(function() {
  toggleFab();
});

$('#fab_help').click(function() {
  getResponse('help');
});

function toggleFab1() {
  $('.prime1').toggleClass('zmdi-plus');
  $('.prime1').toggleClass('zmdi-close');
  $('.prime1').toggleClass('is-active');
  $('#prime1').toggleClass('is-float');
  $('.chat1').toggleClass('is-visible');
  $('.fab1').toggleClass('is-visible');
}

//Toggle chat and links
function toggleFab() {
  $('.prime').toggleClass('zmdi-plus');
  $('.prime').toggleClass('zmdi-close');
  $('.prime').toggleClass('is-active');
  $('#prime').toggleClass('is-float');
  $('.chat').toggleClass('is-visible');
  $('.fab').toggleClass('is-visible');
}


//User msg
function userSend(text) {
  var img = '<i class="zmdi zmdi-account"></i>';
  $('#chat_converse').append('<div class="chat_msg_item chat_msg_item_user"><div class="chat_avatar">' + img + '</div>' + text + '</div>');
  $('#chatSend').val('');
  if ($('.chat_converse').height() >= 256) {
    $('.chat_converse').addClass('is-max');
  }
  $('.chat_converse').scrollTop($('.chat_converse')[0].scrollHeight);
}


//Admin msg
function adminSend(text) {
  $('#chat_converse').append('<div class="chat_msg_item chat_msg_item_admin"><div class="chat_avatar"><img src="../static/Images/doctor2.png" class="boticon"/></div>' + text + '</div>');
  // botSpeak(text);
  if ($('.chat_converse').height() >= 256) {
    $('.chat_converse').addClass('is-max');
  }
  $('.chat_converse').scrollTop($('.chat_converse')[0].scrollHeight);
}


//Speak admin msg
// function botSpeak(text) {
//   if ('speechSynthesis' in window) {
//     var msg = new SpeechSynthesisUtterance(text);
//     window.speechSynthesis.speak(msg);
//   }
// }

//Send input using enter and send key
$('#chatSend').bind("enterChat", function(e) {
  val = $('#chatSend').val();
  userSend(val);
  getResponse(val);
});
// Button ---
$('#fab_send').bind("enterChat", function(e) {
  val = $('#chatSend').val();
  userSend(val);
  getResponse(val);
});

$('#chatSend').keypress(function(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    if (jQuery.trim($('#chatSend').val()) !== '') {
      $(this).trigger("enterChat");
    }
  }
});


function replaceURLWithHTMLLinks(text)
{
    var exp = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;()]*[-A-Z0-9+&@#\/%=~_|()])/ig;
    return text.replace(exp,"<a href='$1'>$1</a>")
}

function getResponse(text) {

let response="";
    // $.ajax({
    //             type: "POST",
    //             url: dialogbaseUrl + "query?v=20150910",
    //             contentType: "application/json; charset=utf-8",
    //             dataType: "json",
    //             headers: {
    //                 "Authorization": "Bearer " + accessToken
    //             },
    //             data: JSON.stringify({ query: text, lang: "en", sessionId: "5974685264812741854158548745" }),
    //             success: function(data) {

    //               var response = data.result.fulfillment.speech;

    //                 response = replaceURLWithHTMLLinks(response);                    
    //                 console.log(response);
    //                 adminSend(response);

    //             },
    //             error: function() {
    //                 let response = "Internal Server Error";
    //                 adminSend(response);
    //             }
    //         });
    var rawText = text;
    // var userHtml = '<p class="userText"><span>' + rawText + '</span></p>';
    // $("#textInput").val("");
    // $("#chatbox").append(userHtml);
    // document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
    $.get("/get", { msg: rawText }).done(function(data) {
      // var botHtml = '<p class="botText"><span>' + data + '</span></p>';
      // var botHtml = '<div class="botText"><span>' + data + '</span></div>';
      // console.log(data);
      var response = data;
      adminSend(response);
      // var botHtml = '<div class="botText"><span>' + textLimiter(data) + '</span></div>';
      // $("#chatbox").append(botHtml);
      // document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
    });


}


$('#fab_send').click(function(e) {
  if (jQuery.trim($('#chatSend').val()) !== '') {
    $(this).trigger("enterChat");
  }
});

//Listen user voice
// $('#fab_listen').click(function() {
//   var recognition = new webkitSpeechRecognition();
//   recognition.onresult = function(event) {
//     userSend(event.results[0][0].transcript);
//   }
//   recognition.start();
// });

// Color options
$(".chat_color").click(function(e) {
  $('.fabs').removeClass(localStorage.getItem("fab-color"));
  $('.fabs').addClass($(this).attr('color'));
  localStorage.setItem("fab-color", $(this).attr('color'));
});

$('.chat_option').click(function(e) {
  $(this).toggleClass('is-dropped');
});

//Loader effect
function loadBeat(beat) {
  beat ? $('.chat_loader').addClass('is-loading') : $('.chat_loader').removeClass('is-loading');
}

// Ripple effect
var target, ink, d, x, y;
$(".fab").click(function(e) {
  target = $(this);
  //create .ink element if it doesn't exist
  if (target.find(".ink").length == 0)
    target.prepend("<span class='ink'></span>");

  ink = target.find(".ink");
  //incase of quick double clicks stop the previous animation
  ink.removeClass("animate");

  //set size of .ink
  if (!ink.height() && !ink.width()) {
    //use parent's width or height whichever is larger for the diameter to make a circle which can cover the entire element.
    d = Math.max(target.outerWidth(), target.outerHeight());
    ink.css({
      height: d,
      width: d
    });
  }

  //get click coordinates
  //logic = click coordinates relative to page - parent's position relative to page - half of self height/width to make it controllable from the center;
  x = e.pageX - target.offset().left - ink.width() / 2;
  y = e.pageY - target.offset().top - ink.height() / 2;

  //set the position and add class .animate
  ink.css({
    top: y + 'px',
    left: x + 'px'
  }).addClass("animate");
});


//Cookies handler
function createCookie(name, value, days) {
  var expires;

  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toGMTString();
    } 
    else {
    expires = "";
    }
    document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value) + expires + "; path=/";
  }

function readCookie(name) {
  var nameEQ = encodeURIComponent(name) + "=";
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return decodeURIComponent(c.substring(nameEQ.length, c.length));
    }
  return null;
  }

function eraseCookie(name) {
  createCookie(name, "", -1);
  }



//Email login
function logUser() {
  hideChat(true);
  $('#chat_send_email').click(function(e) {
    email = $('#chat_log_email').val();
    if (jQuery.trim(email) !== '' && validateEmail(email)) {
      $("#chat_login_alert1").html('');
      loadBeat(true);
      createCookie('fab_chat_email', email, 100);
      if (checkEmail(email)) {
        //email exist and get and set username in session
        hideChat(false);
      } else {
        setTimeout(createUsername, 3000);
      }
    } else {
      $('#chat_login_alert1').html('Invalid email.');
    }
  });


   $('#chat_log_email').on("keyup", function(e){
    if (e.which == 13){
      email = $('#chat_log_email').val();
      if (jQuery.trim(email) !== '' && validateEmail(email)) {
      $("#chat_login_alert1").html('');
      loadBeat(true);
      createCookie('fab_chat_email', email, 100);
      if (checkEmail(email)) {
        //email exist and get and set username in session
        hideChat(false);
      } else {
        setTimeout(createUsername, 3000);
      }
    } else {
      $('#chat_login_alert1').html('Invalid email.');
    }
  }
});
    }
    

//name login
function createUsername() {
  loadBeat(false);
  $('#emaillogin').hide();
  $('#namelogin').show();
  $('#chat_send_username').click(function(e) {
    username = $('#chat_log_username').val();
    if (jQuery.trim(username) !== '') {
      check();
      loadBeat(true);
      if (checkUsername(username)) {
        //username is taken

        $('#chat_login_alert2').html('Username is taken.');
      } else {
        //save username in DB and session
        createCookie('fab_chat_username', username, 100);
        $('#fab_feedback').show();
        hideChat(false);
       }
    }
    else {
      $('#chat_login_alert2').html('Please provide username.');
    }
    });


  $('#chat_log_username').on("keyup", function(e){
    if (e.which == 13){
        username = $('#chat_log_username').val();
        
        if (jQuery.trim(username) !== '') {
            check();
            loadBeat(true);
            if (checkUsername(username)) {
              //username is taken
              $('#chat_login_alert2').html('Username is taken.');
            } else {
              //save username in DB and session
              createCookie('fab_chat_username', username, 100);
              hideChat(false);
              $('#fab_feedback').show();
            }
          } else {
              $('#chat_login_alert2').html('Please provide username.');
            }
          }
        });
      }



function check(){
  var payload = {
                "name":username,
                "email":email,
                };
  console.log(payload);
  sendAJAXRequest('createUser',"POST", payload,  function(data, status){
    if(data && data.success){
      console.log("success");
      welcomemsg = "Hello " + data.data;
      adminSend(welcomemsg);
      
    }else if(data && !data.success){
      if(data.message){
        console.log("failure");
      }
    }
  })

}


function sendAJAXRequest(url, method, payload, successCallBack){
        var obj = {
          type: method,
            url: serverbaseUrl + url,
            dataType: 'JSON',
            contentType: 'application/json',
            success: function( data, status, xhr) {
                console.log(data, status);
                console.log("successful");
                return successCallBack(data, status);
            },
            error: function(xhr, status, error){
                //hideAjaxInProgress();
                //showNotification('error', "Something went wrong, please try again later");
                console.log("failure");
            }
        }
        
        if(method.toUpperCase() == "POST" && payload ){
          obj.data = JSON.stringify(payload);
        }
        $.ajax(obj);
    }


function hideChat(hide) {
  if (hide) {
    $('.chat_converse').css('display', 'none');
    $('.fab_field').css('display', 'none');
    } 
    else {
    $('#chat_head').html(readCookie('fab_chat_username'));
    // Help
    // $('#fab_feedback').click(function(){userSend('Help!');});
    $('.chat_login').css('display', 'none');
    $('.chat_converse').css('display', 'block');
    $('.fab_field').css('display', 'inline-block');
  }
}

// function checkEmail(email) {
//   //check if email exist in DB
//   return false;
// }

// function checkUsername(username) {
//   //check if username exist in DB
//   return false;
// }

// function validateEmail(email) {
//   var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
//   if (!emailReg.test(email)) {
//     return false;
//   } else {
//     return true;
//   }
// }

// if (readCookie('fab_chat_username') === null || readCookie('fab_chat_email') === null) {
//   logUser();
// } else {
//   hideChat(false);
//   $('#fab_feedback').show();

// }
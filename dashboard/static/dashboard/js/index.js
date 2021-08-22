
myStorage = window.localStorage;
function ActivateDarkMode(){
$('body').css("background-color","#24292e");
$('h1,h2,h3,h5,p').css("color","#fff");
$('nav').removeClass("nav-light");
$('nav').addClass("nav-dark");
$('ol').removeClass("breadcrumb-light");
$('ol').addClass("breadcrumb-dark");
$('.breadcrumb-dark.active').css("color","#fff");
$('.card-light').addClass("card-dark");
$('.card-dark').removeClass("card-light");
$('.card-header-light').addClass("card-header-dark");
$('.card-header-dark').removeClass("card-header-light");
$('.card-body-light').addClass("card-body-dark");
$('.card-body-dark').removeClass("card-body-light");
$('.footer-links-light').addClass("footer-links-dark");
$('.footer-links-dark').removeClass("footer-links-light");
$('#btn-mode').css("color","#fff");
$('.navbar-brand-light').addClass("navbar-brand-dark");
$('.navbar-brand-dark').removeClass("navbar-brand-light");
$('.copyright-light').addClass("copyright-dark");
$('.copyright-dark').removeClass("copyright-light");
$('.nav-link-light').addClass("nav-link-dark");
$('.nav-link-dark').removeClass("nav-link-light");
$('.search-field-light').addClass("search-field-dark");
$('.search-field-dark').removeClass("search-field-light");
$("#btn-mode").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>');
$('a.copyright-dark').css("color","#35e6ac");
$('.table').css("color","#fff");

}
function ActivateLightMode(){
$('body').css("background-color","#fff");
$('h1,h2,h3,h5,p').css("color","#24292e");
$('nav').removeClass("nav-dark");
$('nav').addClass("nav-light");
$('ol').removeClass("breadcrumb-dark");
$('ol').addClass("breadcrumb-light");
$('.breadcrumb-dark.active').css("color","#333");
$('.card-dark').addClass("card-light");
$('.card-light').removeClass("card-dark");
$('.card-header-dark').addClass("card-header-light");
$('.card-header-light').removeClass("card-header-dark");
$('.card-body-dark').addClass("card-body-light");
$('.card-body-light').removeClass("card-body-dark");
$('.footer-links-dark').addClass("footer-links-light");
$('.footer-links-light').removeClass("footer-links-dark");
$('#btn-mode').css("color","gray");
$('.navbar-brand-dark').addClass("navbar-brand-light");
$('.navbar-brand-light').removeClass("navbar-brand-dark");
$('.copyright-dark').addClass("copyright-light");
$('.copyright-light').removeClass("copyright-dark");
$('.nav-link-dark').addClass("nav-link-light");
$('.nav-link-light').removeClass("nav-link-dark");
$('.search-field-dark').addClass("search-field-light");
$('.search-field-light').removeClass("search-field-dark");
$("#btn-mode").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>');
$('a.copyright-light').css("color","#9e1ace");
$('.table').css("color","#333");

}

window.addEventListener('load', (event) => {
  console.log('page is fully loaded');


      if ( myStorage.getItem("mode") === null) {
      myStorage.setItem('mode', 'day');
    }


    console.log(myStorage.getItem('mode'))
    if(myStorage.getItem('mode') === "day"){
    $('#theme').attr('href','/static/dashboard/css/light-theme.css');
$("#btn-mode").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>');


//  ActivateLightMode();
       }
       else{
       $('#theme').attr('href', '/static/dashboard/css/dark-theme.css');
$("#btn-mode").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>');

//  ActivateDarkMode();

       }
});
// file: /static/dashboard/css/themes.css
$( document ).ready(function() {
 console.log($('#theme').attr('href'));
  console.log( "ready!" );
$( "#btn-mode" ).on( "click", function() {
if(myStorage.getItem('mode') === "day"){
console.log("its day");
myStorage.setItem('mode','night');
$('#theme').attr('href', '/static/dashboard/css/dark-theme.css');
$("#btn-mode").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>');

}
else{
console.log("its night");
myStorage.setItem('mode','day');
$('#theme').attr('href','/static/dashboard/css/light-theme.css');
$("#btn-mode").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>');

}
});
});




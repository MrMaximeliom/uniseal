$( document ).ready(function() {
    myStorage = window.localStorage;
    myStorage.setItem('mode', 'day');
    console.log( "ready!" );
    $( "#btn-mode" ).on( "click", function() {
    if(myStorage.getItem('mode') === "day"){
     myStorage.setItem('mode','night');
    $("nav").removeClass('bg-light');
    $("nav").css("background-color","#24292e");
    $("body").css("background-color","#24292e");
    $("h1").css("color","#fff");
    $("p").css("color","#fff");
    $(".card").css("background-color","#4a4a4a");
    $(".card-header").css("background-color","#4a4a4a");
    $(".card-body").css("background-color","#24292e");
    $("h5.card-header").css("color","#fff");
    $("a.nav-link").css("color","#fff");
    $("a.navbar-brand").css("color","#fff");
    $("#btn-mode").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>');
    $("#btn-mode").css("color","#fff");
     $("a.nav-link").removeClass('text-secondary');
//    $("a.nav-link.text-secondary").css("color","#fff");
    }
    else{
    $("nav").addClass('bg-light');
    $("nav").css("background-color","#fff");
    $("body").css("background-color","#fff");
    $("h1").css("color","#24292e");
    $("p").css("color","#24292e");
    $(".card").css("background-color","#fff");
    $(".card-header").css("background-color","rgba(0,0,0,.03)");
    $(".card-body").css("background-color","#fff");
    $("h5.card-header").css("color","#24292e");
    $("a.nav-link").css("color","#333");
    $("a.navbar-brand").css("color","#333");
     myStorage.setItem('mode','day');
     $("#btn-mode").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>');
     $("#btn-mode").css("color","gray");
     $("a.nav-link").removeClass('text-secondary');

    }
        $("a.nav-link.active").css("color","#0d6efd");

});
});

myStorage = window.localStorage;
     body = document.getElementById('body')
 btn_mode = document.getElementById('#btn-mode')
$( document ).ready(function() {
console.log("Screen width is: ",screen.width)
$(window).on("resize",function(){
  var w = window.outerWidth;
  var h = window.outerHeight;
  if(w >= 1400){
   if (document.getElementById("mySidenav").style.display === "none"){
     document.getElementById("mySidenav").style.display = "block"



   }

  }
})
let audio;
 console.log($('#theme').attr('href'));
  console.log( "ready!" );
$( "#btn-mode" ).on( "click", function() {
if(myStorage.getItem('mode') === "day"){
console.log("its day");
myStorage.setItem('mode','night');
body.classList.add("dark-theme");
audio = document.querySelector('.theme-audio--light-on');
audio.currentTime = 0;
audio.play();
$("#btn-mode").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>');

}
else{
console.log("its night");
myStorage.setItem('mode','day');
body.classList.remove("dark-theme");
audio = document.querySelector('.theme-audio--light-off');
audio.currentTime = 0;
audio.play();
$("#btn-mode").html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>');

}
});
function closeSideBar(){
  document.getElementById("mySidenav").style.display = "none";
  myStorage.setItem('sidebar-status','closed');
}
$("#sidebar-btn-slide").on("click",function(){
 if (myStorage.getItem('sidebar-status') !== null){
 if(myStorage.getItem('sidebar-status') === 'opened')
 {
 closeSideBar();


 }
 else {
     document.getElementById("mySidenav").style.display = "block";
  document.getElementById("mySidenav").style.width = "256px";
  document.getElementById("first-side-item").focus();
  myStorage.setItem('sidebar-status','opened');

 }

 }
 else{
      document.getElementById("mySidenav").style.display = "block";
  document.getElementById("mySidenav").style.width = "256px";
  document.getElementById("first-side-item").focus();
  myStorage.setItem('sidebar-status','opened');
 }





})
$("#close").on("click",function(){
closeSideBar();

});


});




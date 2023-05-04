$(document).ready(function(){
  $("input").focus(function(){
      $(this).siblings(".label-text").css("top", "-10px");
      $(this).siblings(".label-text").css("font-size", "14px");
  });
  $("input").blur(function(){
      if(!$(this).val()){
          $(this).siblings(".label-text").css("top", "20px");
          $(this).siblings(".label-text").css("font-size", "18px");
      }
  });
});
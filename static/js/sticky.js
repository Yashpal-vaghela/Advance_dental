// Create a clone of the menu, right next to original.
$(".menu")
  .addClass("original")
  .clone()
  .insertAfter(".menu")
  .addClass("cloned")
  .css("position", "fixed")
  .css("top", "0")
  .css("margin-top", "0")
  .css("z-index", "500")
  .removeClass("original")
  .hide();
scrollIntervalID = setInterval(stickIt, 10);
function stickIt() {
  var orgElementPos = $(".original").offset();
  // var homeBannerElement = $('.hero-section1').offset();
  orgElementTop = orgElementPos.top;
  if ($(window).scrollTop() >= orgElementTop) {
    orgElement = $(".original");
    coordsOrgElement = orgElement.offset();
    leftOrgElement = coordsOrgElement.left;
    widthOrgElement = orgElement.css("width");
    $(".header .cloned")
      .css("left", leftOrgElement + "px")
      .css("top", 0)
      .css("width", widthOrgElement)
      .show();
    $(".original").css("visibility", "hidden");
    // if(window.innerWidth > 992){
    //   $('.zir-logo1').css('padding-top',50+'px');
    // }else{
    //   $('.hero-section1').css('padding-top',0+'px');
    // }
  } else {
    // not scrolled past the menu; only show the original menu.
    $(".header .cloned").hide();
    $(".original").css("visibility", "visible");
    // $('.zir-logo1').css('padding-top',0+'px');
  }
}

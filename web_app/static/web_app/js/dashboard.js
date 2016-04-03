$(document).ready(function() {
  console.log("hello world");

  $('input[type=radio][name=device_listing]').change(function() {
  console.log($(this).val());
  var fieldToShow = $(this).val();
  $("#" + fieldToShow).css("display", "block");
  if (("#" + fieldToShow) == '#all_devices') {
      $('#all_devices').css("display", "block");
      $('#online').css("display", "none");
      $('#offline').css("display", "none");
  } else if (("#" + fieldToShow) == '#online'){
    $('#online').css("display", "block");
    $('#all_devices').css("display", "none");
    $('#offline').css("display", "none");
  } else {
    $('#offline').css("display", "block");
    $('#all_devices').css("display", "none");
    $('#online').css("display", "none");
  }
  });

})
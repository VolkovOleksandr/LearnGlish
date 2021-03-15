$("button[name=deleteWord]").click(async function () {
    // Get word id and save into input field
    var clickedId = $(this).val();
    $("input[name=deleteId]").val(clickedId);
  });
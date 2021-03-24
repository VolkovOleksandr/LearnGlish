$("button[name=btnNewsDelete]").click(async function () {
    // Get news id and save into input field
    var clickedId = $(this).val();
    $("input[name=deleteNewsId]").val(clickedId);
  });
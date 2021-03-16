$("button[name=deletePhrase]").click(async function () {
    // Get phrase id and save into input field
    var clickedId = $(this).val();
    $("input[name=deleteId]").val(clickedId);
  });
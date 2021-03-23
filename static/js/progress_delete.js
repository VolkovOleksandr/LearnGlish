$("button[name=deleteStatistics]").click(async function () {
    // Get word id and save into input field
    var clickedId = $(this).val();
    $("input[name=deletedTopicId]").val(clickedId);
  });
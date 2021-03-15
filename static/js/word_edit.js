$("button[name=editWord]").click(async function () {
    var clickedId = $(this).val();
    $("#wordId").val(clickedId);
    try {
      requestWord = await fetch("/study/getWordById", {
        method: "POST",
        body: JSON.stringify(clickedId),
        credentials: "include",
        headers: { "Content-Type": "application/json" },
      });
      // Get response from server
      jsonResponse = await requestWord.json();
      $('input[name="wordOrigin"]').val(jsonResponse.origin);
      $('input[name="wordTranslate"]').val(jsonResponse.translate);
    } catch (error) {
      console.log("Error: ", error);
    }
  });
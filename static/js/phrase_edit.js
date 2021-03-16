$("button[name=editPhrase]").click(async function () {
    var clickedId = $(this).val();
    $("#phraseId").val(clickedId);
    try {
      requestPh = await fetch("/study/getWordById", {
        method: "POST",
        body: JSON.stringify(clickedId),
        credentials: "include",
        headers: { "Content-Type": "application/json" },
      });
      // Get response from server
      jsonResponse = await requestPh.json();
      $('input[name="phraseOrigin"]').val(jsonResponse.origin);
      $('input[name="phraseTranslate"]').val(jsonResponse.translate);
    } catch (error) {
      console.log("Error: ", error);
    }
  });
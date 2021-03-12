
$(document).ready(function (e) {
    $("#topic").on("input", async function (e) {
    inputData = $("#topic").val();
    const url = "/topicSearch";

    try {
        requestTopic = await fetch(url, {
        method: "POST",
        body: JSON.stringify(inputData),
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        });

        // Get response from server
        jsonResponse = await requestTopic.json();

        // If resolve cleare options and set new one
        $("#topics").empty();
        
        $.each(jsonResponse, function (i, item) {
        $("#topics").append(
            $("<option>").attr("value", item.topic)
        );
        });
    } catch (error) {
        // TODO Error handler 
        console.error("Error:", error);
    }
    })
});

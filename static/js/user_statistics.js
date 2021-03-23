var ctx = document.getElementById("vocabChart").getContext("2d");
var ctxr = document.getElementById("progressChart").getContext("2d");
// Chart configuration
Chart.defaults.global.legend.display = false;
// Get data from server
var userStatsJson = $('#userTotalStat').data("stats");
// First diadram for worda and phrases
var myChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["Word", "Phrases"],
    datasets: [
      {
        data: userStatsJson.totalWordsAndPhrases,
        backgroundColor: [
            "rgba(255, 206, 86, 0.2)",
            "rgba(54, 162, 235, 0.2)",
        ],
        borderColor: [ "rgba(255, 206, 86, 1)", "rgba(54, 162, 235, 1)"],
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
            stepSize: 1
          },
        },
      ],
    },
  },
});
// Second diagram for attempts and successfuly passes quiz
var myChartRound = new Chart(ctxr, {
  type: "doughnut",
  data: {
    labels: ["Attempts", "Success"],
    datasets: [
      {
        data: userStatsJson.totalAttemptsAndSuccess,
        backgroundColor: [
            "rgba(153, 102, 255, 0.2)",
            "rgba(75, 192, 192, 0.2)",
        ],
        borderColor: [ "rgba(153, 102, 255, 1)", "rgba(75, 192, 192, 1)"],
        borderWidth: 1,
      },
    ],
  },
});
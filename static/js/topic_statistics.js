var ctx = document.getElementById("myChart").getContext("2d");
var ctxr = document.getElementById("myChartRound").getContext("2d");
Chart.defaults.global.legend.display = false;
var userStatsJson = $('#userStat').data("stats");

var myChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["Word", "Phrases"],
    datasets: [
      {
        data: userStatsJson.wordAndPhrases,
        backgroundColor: [
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
        ],
        borderColor: ["rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)"],
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
          },
        },
      ],
    },
  },
});
// ROUND
var myChartRound = new Chart(ctxr, {
  type: "doughnut",
  data: {
    labels: ["Word", "Phrases"],
    datasets: [
      {
        data: userStatsJson.attemptsAndSuccess,
        backgroundColor: [
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
        ],
        borderColor: ["rgba(75, 192, 192, 1)", "rgba(153, 102, 255, 1)"],
        borderWidth: 1,
      },
    ],
  },
});
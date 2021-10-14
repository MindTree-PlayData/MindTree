// Charts from Chart.js
// bar chart
new Chart(document.getElementById("bar-chart"), {
    type: 'bar',
    data: {
      labels: ["Positive", "Neutral", "Negative"],
      datasets: [
        {
          label: "Sentiment",
          backgroundColor: ["#028000", "#808000","#800000"],
          data: [0.3,0.4,0.3]
        }
      ]
    },
    options: {
      legend: { display: false },
      title: {
        display: true,
        text: 'your sentiment statement'
      }
    }
});

//doughnut chart
new Chart(document.getElementById("doughnut-chart"), {
    type: 'doughnut',
    data: {
      labels: ["Positive", "Neutral", "Negative"],
      datasets: [
        {
          label: "Sentiment",
          backgroundColor: ["#028000", "#808000","#800000"],
          data: [0.3,0.4,0.3]
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'your sentiment statement'
      }
    }
});

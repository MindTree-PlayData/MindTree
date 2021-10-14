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
      responsive: false,
      legend: {
        position: 'top',
        display: false 
      },
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
      responsive: false,
      title: {
        display: true,
        text: 'your sentiment statement'
      }
    }
});

// rader chart
new Chart(document.getElementById("radar-chart"), {
    type: 'radar',
    data: {
      labels: ["Positive", "Neutral", "Negative"],
      datasets: [
        {
          label: "Sentiment",
          fill: true,
          backgroundColor: "rgba(179,181,198,0.2)",
          borderColor: "rgba(179,181,198,1)",
          pointBorderColor: "#fff",
          pointBackgroundColor: "rgba(179,181,198,1)",
          data: [0.3,0.4,0.3]
        }
      ]
    },
    options: {
      responsive:false,
      title: {
        display: true,
        text: 'your sentiment statement'
      }
    }
});

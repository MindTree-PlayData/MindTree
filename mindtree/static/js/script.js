// 단순 변수만 선언해서 Array 타입의 데이터로 만들면
// 아래 차트의 data에 넣으면 된다.
let sentiment2 = userData.document.confidence
    console.log(sentiment2)
let sentimentArray = Object.values(sentiment2)
    console.log(sentimentArray)


// bar chart
new Chart(document.getElementById("bar-chart"), {
    type: 'bar',
    data: {
      labels: ["Negative", "Neutral", "Positive"],
      datasets: [
        {
          label: "Sentiment",
          backgroundColor: ["#ff5959", "#b0b0b0","#59ff64"],
          data: sentimentArray
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
      labels: ["Negative", "Neutral", "Positive"],
      datasets: [
        {
          label: "Sentiment",
          backgroundColor: ["#ff5959", "#b0b0b0","#59ff64"],
          data: sentimentArray
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

// radar chart
new Chart(document.getElementById("radar-chart"), {
    type: 'radar',
    data: {
      labels: ["Negative", "Neutral", "Positive"],
      datasets: [
        {
          label: "Sentiment",
          fill: true,
          backgroundColor: "rgba(179,181,198,0.2)",
          borderColor: "rgba(179,181,198,1)",
          pointBorderColor: "#fff",
          pointBackgroundColor: "rgba(179,181,198,1)",
          data: sentimentArray
        }
      ]
    },
    options: {
      responsive:false,
      title: {
        display: true,
        text: 'your sentiment statement'
      },
      scale: {
        ticks: {
          display: true,
          beginAtZero: true,
          max: 1
        }
      }
    }
});

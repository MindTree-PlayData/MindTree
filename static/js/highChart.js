
// 그냥 로컬디스크의 파일을 주소로 주면 에러가 난다. flask 로 로컬 서버를 만들어주고 거기서 데이터를 반환받아야 한다.

const URL = "http://127.0.0.1:5000/json_data";
console.log(userData)

$(document).ready(function() {
    $(function(){
        // 받아온 데이터에서 필요한 부분을 가져옴
        let sentiment = userData.document.confidence
        console.log(sentiment);

        //for 문 돌리기 위해 array 로 만듬
        let sentimentArray = Object.values(sentiment)
        console.log(sentimentArray)

        for (let i=0; i<3; i++){
            barChart.series[i].addPoint(sentimentArray[i])
        }


        // for (let j=0; j<3; j++){
        //     pieChart.series[j].addPoint(sentimentArray[j])
        // };

    });

    let barChart = new Highcharts.chart({
        chart: {
            renderTo: 'container',
            type: 'bar'
        },
        title: {
            text: 'Stacked bar chart'
        },
        xAxis: {
            categories: ['Sentiments']
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total fruit consumption'
            }
        },
        legend: {
            reversed: true
        },
        plotOptions: {
            series: {
                stacking: 'normal'
            }
        },
        series: [{
            name: 'negative',
            data: []
        }, {
            name: 'positive',
            data: []
        }, {
            name: 'neutral',
            data: []
        }]
    });

    // let pieChart = new Highcharts.chart('container2', {
    //     chart: {
    //         plotBackgroundColor: null,
    //         plotBorderWidth: null,
    //         plotShadow: false,
    //         type: 'pie'
    //     },
    //     title: {
    //         text: 'Pie Chart for Sentiments'
    //     },
    //     tooltip: {
    //         pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    //     },
    //     accessibility: {
    //         point: {
    //             valueSuffix: '%'
    //         }
    //     },
    //     plotOptions: {
    //         pie: {
    //             allowPointSelect: true,
    //             // cursor: 'pointer',
    //             dataLabels: {
    //                 enabled: true,
    //                 format: '<b>{point.name}</b>: {point.percentage:.1f} %'
    //             }
    //         }
    //     },
    //     series: [{
    //         name: 'negative',
    //         data: []
    //     }, {
    //         name: 'positive',
    //         data: []
    //     }, {
    //         name: 'neutral',
    //         data:[]
    //     }]
    // });

});


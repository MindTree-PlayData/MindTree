
// 변수 받을 수 있는지 확인.
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

    // --------- Stacked bar chart -----------

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

    // ----------- Pie Chart -------------

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


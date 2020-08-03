'use strict';

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

$(document).ready(function () {
    var $linechart = $('#morris-line-chart');
    var $barchart = $('#morris-bar-chart');
    var $piechart = $('#morris-pie-chart');
    var $specializationChart = $('#morris-specialization-chart');

    $.ajax({
        type: 'post',
        url: '/analytics_dataset/',
        success: function (res) {
            var ctx = $linechart[0].getContext("2d");
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: res.labels,
                    datasets: [{
                        label: res.chartlabels,
                        backgroundColor: 'aqua',
                        data: res.data
                    }]
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'top',
                    },
                    scales: {
                        xAxes: [{
                            display: true
                        }],
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });

        },
        error: function (err) {
            console.log(err);
        }
    });

    $.ajax({
        type: 'post',
        url: '/analytics_dataset2/',
        success: function (res) {
            var ctx = $barchart[0].getContext("2d");
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: res.labels,
                    datasets: [{
                        label: res.chartlabels,
                        backgroundColor: 'grey',
                        data: res.data
                    }]
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'top',
                    },
                    scales: {
                        xAxes: [{
                            display: true
                        }],
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });

        },
        error: function (err) {
            console.log(err);
        }
    });

    $.ajax({
        type: 'post',
        url: '/analytics_dataset3/',
        success: function (res) {
            var ctx = $piechart[0].getContext("2d");
            var colorarray = [];
            for (var i = 0; i < res['labels'].length; i++)
                colorarray.push(getRandomColor());
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: res.labels,
                    datasets: [{
                        label: res.chartlabels,
                        backgroundColor: colorarray,
                        data: res.data
                    }]
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'top',
                    }
                }
            });
        },
        error: function (err) {
            console.log(err);
        }
    });

    $.ajax({
        type: 'post',
        url: '/analytics_dataset4/',
        success: function (res) {
            var ctx = $specializationChart[0].getContext("2d");
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: res.labels,
                    datasets: [{
                        label: res.chartlabels,
                        backgroundColor: getRandomColor(),
                        data: res.data
                    }]
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'top',
                    },
                    scales: {
                        xAxes: [{
                            display: true
                        }],
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        },
        error: function (err) {
            console.log(err);
        }
    });
});
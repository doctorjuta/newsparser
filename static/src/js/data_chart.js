import Chart from "chart.js";
import $ from "jquery";
import {getCookie, csrfSafeMethod} from "./ajax_helpers";


export default function DataChart(obj) {

    let self = this;
    let charts_positive_color = "#00ff00";
    let charts_negative_color = "#ff0000";

    function requestStart() {
        obj.addClass("loading");
    }

    function requestEnd() {
        obj.removeClass("loading");
    }

    function requestError(text) {
        console.log("Error");
    }

    function renderChart(data) {
        let chart_title = obj.attr("data-title");
        let chart_labels = [];
        let data_positive = [];
        let data_negative = [];
        let count_val = data.length;
        for (let i=0;i<count_val;i++) {
            let it = data[i];
            let it_date = new Date(it["news_date"]);
            chart_labels.push(it_date.getMonth()+1 + "/" + it_date.getDate() + " " + it_date.getHours() + ":" + it_date.getMinutes());
            if (it["tonality_index"] >= 0) {
                data_positive.push(it["tonality_index"]);
                data_negative.push(0);
            } else {
                data_positive.push(0);
                data_negative.push(it["tonality_index"]);
            }
        }
        let ctx = obj[0].getContext("2d");
        let chart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: chart_labels,
                datasets: [
                    {
                        label: "Positive",
                        data: data_positive,
                        backgroundColor: charts_positive_color,
                        barPercentage: 1.0
                    },
                    {
                        label: "Negative",
                        data: data_negative,
                        backgroundColor: charts_negative_color,
                        barPercentage: 1.0
                    }
                ]
            },
            options: {
                title: {
                    display: true,
                    text: chart_title
                },
                legend: {
                    display: false
                },
				responsive: true,
				scales: {
					xAxes: [{
						stacked: true,
					}],
					yAxes: [{
						stacked: true,
                        ticks: {
                            suggestedMin: 10,
                            suggestedMax: 10
                        }
					}]
				}
            }
        });
    }

    self.init = function() {
        let param = {
            action: "tonality_charts"
        }
        let request_time = obj.attr("data-time");
        if (request_time) {
            param.time = request_time;
        }
        $.ajax({
            url: rest_url,
            dataType: "json",
            type: "POST",
            data: param,
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    let csrftoken = getCookie("csrftoken");
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
                requestStart();
            },
            complete: function() {
                requestEnd();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                let errorMessage = "Projects error: " + errorThrown + " URL: " + window.location.href;
                requestError(errorMessage);
            },
            success: function(resp, textStatus, jqXHR) {
                renderChart(resp.data);
            }
        });
    }

}

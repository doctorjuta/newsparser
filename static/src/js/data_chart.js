import Chart from "chart.js";
import $ from "jquery";
import {getCookie, csrfSafeMethod} from "./ajax_helpers";


export default function DataChart(obj) {

    let self = this;

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
        let chart_border_color = obj.attr("data-bcolor");
        let chart_point_color = obj.attr("data-pcolor");
        let chart_data = data.map(function(it) {
            return it["tonality_index"];
        });
        let chart_labels = data.map(function(it) {
            let it_date = new Date(it["news_date"]);
            return it_date.getMonth() + "/" + it_date.getDate() + " " + it_date.getHours() + ":" + it_date.getMinutes();
        });
        let ctx = obj[0].getContext("2d");
        let chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: chart_labels,
                datasets: [{
                    label: chart_title,
                    data: chart_data,
                    backgroundColor: "transparent",
                    borderColor: chart_border_color,
                    pointBackgroundColor: chart_point_color,
                    lineTension: 0,
                    pointBorderWidth: 0,
                    borderWidth: 1
                }]
            },
            options: {
                legend: {
                    display: false
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

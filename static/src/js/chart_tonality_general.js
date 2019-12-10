import Chart from "chart.js";
import $ from "jquery";
import {getCookie, csrfSafeMethod} from "./ajax_helpers";
import ChartGeneral from "./chart_general";


export default class ChartTonalityGeneral extends ChartGeneral {

    renderChart(data) {
        let self = this;
        let chart_title = self.obj.attr("data-title");
        let chart_labels = [];
        let data_positive = [];
        let data_negative = [];
        let count_val = data.length;
        for (let i=0;i<count_val;i++) {
            let it = data[i];
            let it_date = new Date(it["news_date"]);
            chart_labels.push(it_date.getMonth()+1 + "/" + it_date.getDate() + " " + ("0" + it_date.getHours()).slice(-2) + ":" + ("0" + it_date.getMinutes()).slice(-2));
            if (it["tonality_index"] >= 0) {
                data_positive.push(it["tonality_index"]);
                data_negative.push(0);
            } else {
                data_positive.push(0);
                data_negative.push(it["tonality_index"]);
            }
        }
        let ctx = self.obj[0].getContext("2d");
        self.bar_options.data.labels = chart_labels;
        self.bar_options.data.datasets[0].data = data_positive;
        self.bar_options.data.datasets[1].data = data_negative;
        self.bar_options.options.title.text = chart_title;
        let chart = new Chart(ctx, self.bar_options);
    }

    init() {
        let self = this;
        let param = {
            action: "tonality_charts"
        }
        let request_time = self.obj.attr("data-time");
        if (request_time) {
            param.time = request_time;
        }
        let request_source = self.obj.attr("data-source");
        if (request_source) {
            param.source_id = request_source;
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
                self.requestStart();
            },
            complete: function() {
                self.requestEnd();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                let errorMessage = "Projects error: " + errorThrown + " URL: " + window.location.href;
                self.requestError(errorMessage);
            },
            success: function(resp, textStatus, jqXHR) {
                self.renderChart(resp.data);
            }
        });
    }

}

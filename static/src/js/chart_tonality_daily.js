import Chart from "chart.js";
import $ from "jquery";
import {getCookie, csrfSafeMethod} from "./helpers";
import ChartGeneral from "./chart_general";


export default class ChartTonalityDaily extends ChartGeneral {

    renderChart(data) {
        let self = this;
        let chart_title = self.obj.attr("data-title");
        let chart_labels = [];
        let data_vals = [];
        let count_val = data.length;
        for (let i=0;i<count_val;i++) {
            let it = data[i];
            let it_date = new Date(it["date"]);
            chart_labels.push(it_date.getMonth()+1 + "/" + it_date.getDate());
            data_vals.push(it["tonality_index"]);
        }
        let ctx = self.obj[0].getContext("2d");
        if (chart_title != undefined) {
            this.line_options.options.title = {
                display: true,
                text: chart_title
            };
        }
        this.line_options.data.labels = chart_labels;
        this.line_options.data.datasets[0].data = data_vals;
        let chart = new Chart(ctx, this.line_options);
    }

    init() {
        let self = this;
        let param = {
            action: "tonality_daily"
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

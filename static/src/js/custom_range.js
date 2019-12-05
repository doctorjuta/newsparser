import jQuery from "jquery";
import "../css/daterangepicker.css";
import "./moment.min.js";
import "./daterangepicker.min.js";
import Chart from "chart.js";
import {getCookie, csrfSafeMethod} from "./ajax_helpers";
import ChartGeneral from "./chart_general";


jQuery.noConflict();
(function($) {


    class CustomRangeScript extends ChartGeneral {


        initCharts() {
            let self = this;
            self.rend.click(function(e) {
                e.preventDefault();
                let param = {
                    action: "tonality_custom",
                    range: self.sel.val()
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
                        self.requestError(jqXHR.responseText);
                    },
                    success: function(resp, textStatus, jqXHR) {
                        self.renderChart(resp.data);
                    }
                });
            });
        }

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
            let chart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: chart_labels,
                    datasets: [
                        {
                            label: "Positive",
                            data: data_positive,
                            backgroundColor: self.charts_positive_color,
                            barPercentage: 1.0
                        },
                        {
                            label: "Negative",
                            data: data_negative,
                            backgroundColor: self.charts_negative_color,
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

        initDatePicker() {
            let self = this;
            let enddate = new Date();
            let startdate = new Date();
            startdate.setDate(startdate.getDate()-1);
            let maxdate = new Date();
            var mindate = new Date();
            mindate.setDate(mindate.getDate()-30);
            self.sel.daterangepicker({
                startDate: startdate,
                endDate: enddate,
                timePicker: true,
                timePicker24Hour: true,
                minDate: mindate,
                maxDate: maxdate,
                locale: {
                    format: "YYYY-MM-DD HH:mm"
                }
            });
        }

        init() {
            this.sel = $("#custom_date_range_select");
            this.rend = $("#custom_date_range_render");
            this.clear = $("#custom_date_range_clear");
            this.initDatePicker();
            this.initCharts();
        }

    }


    $(function() {
        let chart = new CustomRangeScript($("#tonality-graph-custom"));
        chart.init();
    });


})(jQuery);

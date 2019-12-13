import jQuery from "jquery";
import "../css/daterangepicker.css";
import "./moment.min.js";
import "./daterangepicker.min.js";
import Chart from "chart.js";
import {getCookie, csrfSafeMethod} from "./ajax_helpers";
import ChartGeneral from "./chart_general";
const moment = require("moment");


jQuery.noConflict();
(function($) {


    class CustomRangeScript extends ChartGeneral {


        initDailyChart(data_range, chart_title) {
            let self = this;
            let param = {
                action: "tonality_daily_custom",
                range: data_range
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
                    self.clearChart();
                    self.requestStart();
                },
                complete: function() {
                    self.requestEnd();
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    self.requestError(jqXHR.responseText);
                },
                success: function(resp, textStatus, jqXHR) {
                    self.renderChart(resp.data, "line", chart_title);
                }
            });
        }


        initCustomRangeChart() {
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
                        self.clearChart();
                        self.requestStart();
                    },
                    complete: function() {
                        self.requestEnd();
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        self.requestError(jqXHR.responseText);
                    },
                    success: function(resp, textStatus, jqXHR) {
                        self.renderChart(resp.data, "bar", self.obj.attr("data-title"));
                    }
                });
            });
        }

        clearChart() {
            let self = this;
            if (self.chart) {
                self.chart.destroy();
            }
        }

        renderChart(data, chart_type, chart_title) {
            let self = this;
            let chart_labels = [];
            let ctx = self.obj[0].getContext("2d");
            if (chart_type == "bar") {
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
                self.bar_options.data.labels = chart_labels;
                self.bar_options.data.datasets[0].data = data_positive;
                self.bar_options.data.datasets[1].data = data_negative;
                self.bar_options.options.title.text = chart_title;
                self.chart = new Chart(ctx, self.bar_options);
            } else {
                let data_vals = [];
                let count_val = data.length;
                for (let i=0;i<count_val;i++) {
                    let it = data[i];
                    let it_date = new Date(it["news_date"]);
                    chart_labels.push(it_date.getMonth()+1 + "/" + it_date.getDate());
                    data_vals.push(it["tonality_index"]);
                }
                self.line_options.data.labels = chart_labels;
                self.line_options.data.datasets[0].data = data_vals;
                self.line_options.options.title = {
                    display: true,
                    text: chart_title
                };
                self.chart = new Chart(ctx, self.line_options);
            }

        }

        initDatePicker() {
            let self = this;
            let enddate = new Date();
            let startdate = new Date();
            startdate.setDate(startdate.getDate()-1);
            let maxdate = new Date();
            self.sel.daterangepicker({
                startDate: startdate,
                endDate: enddate,
                timePicker: true,
                timePicker24Hour: true,
                maxDate: maxdate,
                locale: {
                    format: self.date_format
                }
            });
        }

        init() {
            let self = this;
            self.date_format = "YYYY-MM-DD HH:mm";
            self.sel = $("#custom_date_range_select");
            self.rend = $("#custom_date_range_render");
            self.clear = $("#custom_date_range_clear");
            self.chart = false;
            self.initDatePicker();
            self.initCustomRangeChart();

            let fin_d = moment();
            let start_d = moment().subtract(1, "month");
            let data_range = start_d.format(self.date_format) + " - " + fin_d.format(self.date_format)
            self.initDailyChart(data_range, "Тональність за останній місяць");

            $("#custom_date_year").click(function(e) {
                e.preventDefault();
                let fin_d = moment();
                let start_d = moment().subtract(1, "year");
                let data_range = start_d.format(self.date_format) + " - " + fin_d.format(self.date_format)
                self.initDailyChart(data_range, "Тональність за останній рік");
            });
            $("#custom_date_half_year").click(function(e) {
                e.preventDefault();
                let fin_d = moment();
                let start_d = moment().subtract(6, "month");
                let data_range = start_d.format(self.date_format) + " - " + fin_d.format(self.date_format)
                self.initDailyChart(data_range, "Тональність за останні пів року");
            });
            $("#custom_date_3_month").click(function(e) {
                e.preventDefault();
                let fin_d = moment();
                let start_d = moment().subtract(3, "month");
                let data_range = start_d.format(self.date_format) + " - " + fin_d.format(self.date_format)
                self.initDailyChart(data_range, "Тональність за останні три місяці");
            });
            $("#custom_date_month").click(function(e) {
                e.preventDefault();
                let fin_d = moment();
                let start_d = moment().subtract(1, "month");
                let data_range = start_d.format(self.date_format) + " - " + fin_d.format(self.date_format)
                self.initDailyChart(data_range, "Тональність за останній місяць");
            });
        }

    }


    $(function() {
        let chart = new CustomRangeScript($("#tonality-graph-custom"));
        chart.init();
    });


})(jQuery);

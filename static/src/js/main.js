import jQuery from "jquery";
import "bulma/css/bulma.css";
import "../less/style.less";
import DataChart from "./data_chart";


jQuery.noConflict();
(function($) {


    function ThemeScript() {

        let body = $("body");
        let wind = $(window);
        let self = this;

        function initCharts() {
            $(".chart").each(function() {
                let chart = new DataChart($(this));
                chart.init();
            });
        }

        self.run = function() {
            initCharts();
        }

    }


    $(function() {
        let ts = new ThemeScript();
        ts.run();
    });


})(jQuery);

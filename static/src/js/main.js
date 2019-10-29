import jQuery from "jquery";
import "bulma/css/bulma.css";
import "../less/style.less";
import DataChart from "./data_chart";
import { CountUp } from 'countup.js';


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

        function initNumberCouts() {
            if ($(".dnmc_number").length > 0) {
                $(".dnmc_number").each(function() {
                    let countUp = new CountUp($(this).attr("id"), $(this).attr("data-targ"));
                    countUp.start();
                });
            }
        }

        self.run = function() {
            initCharts();
            initNumberCouts();
        }

    }


    $(function() {
        let ts = new ThemeScript();
        ts.run();
    });


})(jQuery);

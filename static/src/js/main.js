import jQuery from "jquery";
import "bulma/css/bulma.css";
import "../less/style.less";
import ChartTonalityGeneral from "./chart_tonality_general";
import ChartTonalityDaily from "./chart_tonality_daily";
import { CountUp } from 'countup.js';


jQuery.noConflict();
(function($) {


    function ThemeScript() {

        let body = $("body");
        let wind = $(window);
        let self = this;

        function initCharts() {
            $(".chart_tonality_general").each(function() {
                let chart = new ChartTonalityGeneral($(this));
                chart.init();
            });
            $(".chart_tonality_daily").each(function() {
                let chart = new ChartTonalityDaily($(this));
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

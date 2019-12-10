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
        let html_obj = $("html");
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

        function initNotifications() {
            $("body").on("click", "button.delete", function() {
                let mess = $(this).closest(".message");
                mess.animate({opacity: 0}, 500, function() {
                    mess.remove();
                });
                return false;
            });
        }

        function initHeader() {
            let lastScrollTop = 0;
            $(window).scroll(function(event) {
                let st = $(this).scrollTop();
                if (st < 80) {
                    body.removeClass("scroll-up").removeClass("scroll-down");
                    return;
                }
                if (st > lastScrollTop){
                    body.removeClass("scroll-up").addClass("scroll-down");
                } else {
                    body.removeClass("scroll-down").addClass("scroll-up");
                }
                lastScrollTop = st;
            });
            $("#top-menu-toggle").click(function(e) {
                e.preventDefault();
                $("#top-menu, #top-menu-toggle").toggleClass("is-active");
                $("header .logo").toggleClass("menu-open");
                html_obj.toggleClass("menu-open");
            });
        }

        self.run = function() {
            initCharts();
            initNumberCouts();
            initNotifications();
            initHeader();
        }

    }


    $(function() {
        let ts = new ThemeScript();
        ts.run();
    });


})(jQuery);

import jQuery from "jquery";
import "bulma/css/bulma.css";
import "../less/style.less";
import ChartTonalityGeneral from "./chart_tonality_general";
import ChartTonalityDaily from "./chart_tonality_daily";
import { CountUp } from 'countup.js';
import {getCookie, csrfSafeMethod, renderErrorMess} from "./helpers";


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

        function initLoadMoreLast() {
            $("#last_news_more").click(function() {
                let btn = $(this);
                let cont = $("#last_news");
                let cont_wrp = cont.find(".last_news_wrp");
                let param = {
                    action: "last_news_more",
                    source_id: parseInt(cont.attr("data-source")),
                    page: parseInt(cont.attr("data-page"))
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
                        cont.addClass("loading");
                        btn.attr("disabled", "disabled");
                    },
                    complete: function() {
                        cont.removeClass("loading");
                        btn.removeAttr("disabled");
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        let errorMessage = "Projects error: " + errorThrown + " URL: " + window.location.href;
                        renderErrorMess(errorMessage, cont);
                    },
                    success: function(resp, textStatus, jqXHR) {
                        for (let i=0;i<resp.data.length;i++) {
                            let tonality_style = "background-color: transparent;";
                            if (resp.data[i].tonality_index > 0) {
                                tonality_style = "background-color: #00ff00;";
                            } else if (resp.data[i].tonality_index < 0) {
                                tonality_style = "background-color: #c70000; color: #ffffff;";
                            }
                            cont_wrp.append(`
                                <div class="last_news_item">
                                    <p class="last_news_tonality" style="${tonality_style}">${resp.data[i].tonality_index}</p>
                                    <p class="last_news_title"><a target="_blank" href="${resp.data[i].link}">${resp.data[i].title}</a><span class="last_news_date">${resp.data[i].date}</span></p>
                                </div>
                            `);
                        }
                        cont.attr("data-page", param.page+1);
                    }
                });
                return false;
            });
        }

        self.run = function() {
            initCharts();
            initNumberCouts();
            initNotifications();
            initHeader();
            initLoadMoreLast();
        }

    }


    $(function() {
        let ts = new ThemeScript();
        ts.run();
    });


})(jQuery);

import jQuery from "jquery";
import "bulma/css/bulma.css";
import "../less/style.less";


jQuery.noConflict();
(function($) {


    function ThemeScript() {

        let body = $("body");
        let wind = $(window);
        let self = this;

        self.run = function() {

        }

    }


    $(function() {
        let ts = new ThemeScript();
        ts.run();
    });


})(jQuery);

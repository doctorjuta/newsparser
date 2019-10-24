import Chart from "chart.js";
import $ from "jquery";
import {getCookie, csrfSafeMethod} from "./ajax_helpers";


export default function DataChart(obj) {

    let self = this;

    function requestStart() {
        obj.addClass("loading");
    }

    function requestEnd() {
        obj.removeClass("loading");
    }

    function requestError(text) {
        console.log("Error");
    }

    self.init = function() {
        let model = obj.attr("data-model");
        let param = {
            model: model,
            action: "charts"
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
                requestStart();
            },
            complete: function() {
                requestEnd();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                let errorMessage = "Projects error: " + errorThrown + " URL: " + window.location.href;
                requestError(errorMessage);
            },
            success: function(resp, textStatus, jqXHR) {
                console.log(resp.data);
            }
        });
    }

}

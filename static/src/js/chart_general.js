export default class ChartGeneral {

    constructor(obj) {
        this.obj = obj;
        this.charts_positive_color = "#00ff00";
        this.charts_negative_color = "#c70000";
        this.charts_neitral_color = "#520000";
    }

    requestStart() {
        if (this.obj.parent(".loading_wrapper").length > 0) {
            this.obj.parent(".loading_wrapper").addClass("loading");
        } else {
            this.obj.addClass("loading");
        }
    }

    requestEnd() {
        if (this.obj.parent(".loading_wrapper").length > 0) {
            this.obj.parent(".loading_wrapper").removeClass("loading");
        } else {
            this.obj.removeClass("loading");
        }
    }

    requestError(text) {
        let message = `
            <div class="notification is-danger">
                <button class="delete"></button>
                ${text}
            </div>
        `;
        this.obj.before(message);
    }

    renderChart(data) {}

    init() {}

}

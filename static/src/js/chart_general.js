export default class ChartGeneral {

    constructor(obj) {
        this.obj = obj;
        this.charts_positive_color = "#00ff00";
        this.charts_negative_color = "#ff0000";
    }

    requestStart() {
        this.obj.addClass("loading");
    }

    requestEnd() {
        this.obj.removeClass("loading");
    }

    requestError(text) {
        console.log(text);
    }

    renderChart(data) {}

    init() {}

}

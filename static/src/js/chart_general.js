export default class ChartGeneral {

    constructor(obj) {
        this.obj = obj;
        this.charts_positive_color = "#00ff00";
        this.charts_negative_color = "#c70000";
        this.charts_neitral_color = "#520000";
        this.bar_options = {
            type: "bar",
            data: {
                labels: [],
                datasets: [
                    {
                        label: "Positive",
                        data: [],
                        backgroundColor: this.charts_positive_color,
                        barPercentage: 1.0
                    },
                    {
                        label: "Negative",
                        data: [],
                        backgroundColor: this.charts_negative_color,
                        barPercentage: 1.0
                    }
                ]
            },
            options: {
                title: {
                    display: true,
                    text: ""
                },
                legend: {
                    display: false
                },
                responsive: true,
                scales: {
                    xAxes: [{
                        stacked: true,
                    }],
                    yAxes: [{
                        stacked: true,
                    }]
                }
            }
        };
        this.line_options = {
            type: "line",
            data: {
                labels: [],
                datasets: [
                    {
                        label: "Tonality",
                        data: [],
                        borderColor: this.charts_neitral_color,
                        barPercentage: 1.0,
                        backgroundColor: "transparent",
                        borderJoinStyle: "round",
                        borderWidth: 2,
                        lineTension: 0
                    }
                ]
            },
            options: {
                title: {
                    display: false
                },
                legend: {
                    display: false
                },
                responsive: true
            }
        };
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

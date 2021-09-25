const primary = '#EC732F';
const success = '#1BC5BD';
const info = '#8950FC';
const warning = '#FFA800';
const danger = '#F64E60';
function ShowLineGraph(id, dataArr, titleText, pointer,color) {
        const apexChart =  id;
        var options = {
            series: [{
                name: pointer,
                data: dataArr
            }],
            chart: {
                height: 350,
                type: 'line',
                zoom: {
                    enabled: false
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'straight',
                width: 3
            },
            grid: {
                row: {
                    colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                    opacity: 0.5
                },
            },
            xaxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep','Oct','Nov','Dec'],
            },
            yaxis: {
                title: {
                    text: titleText
                }
            },
            colors: [color]
        };

        var chart = new ApexCharts(document.querySelector(apexChart), options);
        chart.render();
    }
// #########################################################################################################################
jQuery(document).ready(function () {
    adminCustomerGraph1();
    adminCustomerGraph2();
});
// #########################################################################################################################
function adminCustomerGraph1(){
    $.ajax({
        type: 'GET',
        url: "/ab_admin/adminCustomerGraph1",
        success: function (response) {
            console.log(response);
            var textTitle = 'Total No. of customers (in Hundred)';
            ShowLineGraph('#chart_1', response, textTitle, 'Customers', '#EC732F');


        }
    })
}
// #########################################################################################################################
function adminCustomerGraph2() {
    $.ajax({
        type: 'GET',
        url: "/ab_admin/adminCustomerGraph2",
        success: function (response) {
            console.log(response);
            var textTitle = 'Average amount (in Rs.)';
            ShowLineGraph('#chart_2', response, textTitle, 'Monthly average', '#1BC5BD');


        }
    })
}
// #########################################################################################################################
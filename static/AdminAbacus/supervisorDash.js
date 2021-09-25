var todaySalesData = [];
var yesterdaySalesData = [];
var weekSalesData = [];
var monthlySalesData = [];

$( document ).ready(function() {
    // ==========================================================================
    //                           AJAX CALL
    // ==========================================================================
    $.ajax({
        type: 'GET',
        url: "/getStores",
        success: function (response) {
           console.log(response['storeArray']);
           var tableString = '';
           for(var i=0;i<response['storeArray'].length;i++){
               var data = '<tr>\
                            <th scope="row">'+response['storeArray'][i]['storeID']+'</th>\
                            <th scope="row">'+response['storeArray'][i]['storeName']+'</th>\
                            <td>'+response['storeArray'][i]['todaySales']+'</td>\
                            <td>'+response['storeArray'][i]['yesterdaySales']+'</td>\
                            <td>'+response['storeArray'][i]['currentMonthSales']+'</td>\
                            <td>'+response['storeArray'][i]['weekSales']+'</td>\
                            <td>'+response['storeArray'][i]['lastMonthSales']+'</td>\
                            </tr>';
                tableString = tableString + data;
           }
           $('#salesInfoAppend').html('');
           $('#salesInfoAppend').append(tableString);
           $('#graphSection').css('display','');
        

        // ---------------------------------------------------------------------------------------------
        //                                         SALES GRAPH
        // ---------------------------------------------------------------------------------------------
        var ctx = $("#bar-chartcanvas");
        var labels = [];
        for(var i=0;i<response['storeArray'].length;i++){
            labels.push(response['storeArray'][i]['storeName']);
            todaySalesData.push(response['storeArray'][i]['todaySales']);
            yesterdaySalesData.push(response['storeArray'][i]['yesterdaySales']);
            weekSalesData.push(response['storeArray'][i]['weekSales']);
            monthlySalesData.push(response['storeArray'][i]['currentMonthSales']);
        }

            var data = {
                labels : labels,
                datasets : [
                    {
                        label : "Today Sales",
                        data : todaySalesData,
                        backgroundColor : [
                            "rgba(10, 20, 30, 0.3)",
                            "rgba(10, 20, 30, 0.3)",
                            "rgba(10, 20, 30, 0.3)",
                            "rgba(10, 20, 30, 0.3)",
                            "rgba(10, 20, 30, 0.3)"
                        ],
                        borderColor : [
                            "rgba(10, 20, 30, 1)",
                            "rgba(10, 20, 30, 1)",
                            "rgba(10, 20, 30, 1)",
                            "rgba(10, 20, 30, 1)",
                            "rgba(10, 20, 30, 1)"
                        ],
                        borderWidth : 1
                    },
                    {
                        label : "Yesterday Sales",
                        data : yesterdaySalesData,
                        backgroundColor : [
                            "rgba(243, 92, 92, 0.3)",
                            "rgba(243, 92, 92, 0.3)",
                            "rgba(243, 92, 92, 0.3)",
                            "rgba(243, 92, 92, 0.3)",
                            "rgba(243, 92, 92, 0.3)"
                        ],
                        borderColor : [
                            "rgba(243, 92, 92, 1)",
                            "rgba(243, 92, 92, 1)",
                            "rgba(243, 92, 92, 1)",
                            "rgba(243, 92, 92, 1)",
                            "rgba(243, 92, 92, 1)"
                        ],
                        borderWidth : 1
                    },
                    {
                        label : "Weekly Sales",
                        data : weekSalesData,
                        backgroundColor : [
                            "rgba(119, 232, 115, 0.3)",
                            "rgba(119, 232, 115, 0.3)",
                            "rgba(119, 232, 115, 0.3)",
                            "rgba(119, 232, 115, 0.3)",
                            "rgba(119, 232, 115, 0.3)"
                        ],
                        borderColor : [
                            "rgba(119, 232, 115, 1)",
                            "rgba(119, 232, 115, 1)",
                            "rgba(119, 232, 115, 1)",
                            "rgba(119, 232, 115, 1)",
                            "rgba(119, 232, 115, 1)"
                        ],
                        borderWidth : 1
                    },
                    {
                        label : "Monthly Sales",
                        data : monthlySalesData,
                        backgroundColor : [
                            "rgba(50, 150, 250, 0.3)",
                            "rgba(50, 150, 250, 0.3)",
                            "rgba(50, 150, 250, 0.3)",
                            "rgba(50, 150, 250, 0.3)",
                            "rgba(50, 150, 250, 0.3)"
                        ],
                        borderColor : [
                            "rgba(50, 150, 250, 1)",
                            "rgba(50, 150, 250, 1)",
                            "rgba(50, 150, 250, 1)",
                            "rgba(50, 150, 250, 1)",
                            "rgba(50, 150, 250, 1)"
                        ],
                        borderWidth : 1
                    }
                ]
            };

            var options = {
                title : {
                    display : true,
                    position : "top",
                    text : "Bar Graph",
                    fontSize : 18,
                    fontColor : "#111"
                },
                legend : {
                    display : true,
                    position : "bottom"
                },
                scales : {
                    yAxes : [{
                        ticks : {
                            min : 0
                        }
                    }]
                }
            };

            var chart = new Chart( ctx, {
                type : "bar",
                data : data,
                options : options
            });


        // ---------------------------------------------------------------------------------------------
        // ---------------------------------------------------------------------------------------------
        }
    })
    // ==========================================================================
    // ==========================================================================
    $('#spinnerSection').css('display','none');
    $('#spinnerSection').css('margin-top','5px');
    $('#spinnerSection1').css('display','none');
    $('#loadingSection').css('display','none');
    $('#salesTableSection').css('display','');
    
});
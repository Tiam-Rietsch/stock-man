document.addEventListener("DOMContentLoaded", function () {
    // Dummy Data for Charts
    const dataUrl = document.getElementById("dataUrl").value
    fetch(dataUrl, {})
        .then(response => response.json())
        .then(data => {
            populateChartData(data)
        })
        .catch(error => console.error(error))
});

function populateChartData(data) {
    const yearlyData = {
        series: [
            {
                name: "Ventes",
                // amount of money sold for each month of the current year
                data: data.yearly_sales,
            },
        ],
        categories: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
    };

    const monthlyData = {
        series: [
            {
                name: "Ventes",
                // amount of money sold for each day of the current month
                data: data.monthly_sales,
            },
        ],
        categories: Array.from({ length: 31 }, (_, i) => (i + 1).toString()),
    };

    // Chart Options
    const chartOptions = {
        chart: {
            type: "line",
            height: 350,
            toolbar: {
                show: false,
            },
            zoom: {
                enabled: false,
            },
        },
        colors: ["#007bff"],
        dataLabels: {
            enabled: false,
        },
        stroke: {
            curve: "smooth",
            width: 2,
        },
        grid: {
            row: {
                colors: ["#f5f5f5", "transparent"],
                opacity: 0.5,
            },
        },
        xaxis: {
            categories: yearlyData.categories,
        },
        yaxis: {
            title: {
                text: "Ventes (FCFA)",
            },
        },
    };

    // Initialize Sales Trends Chart
    let salesTrendsChart = new ApexCharts(document.querySelector(".line-chart"), {
        ...chartOptions,
        series: yearlyData.series,
    });
    salesTrendsChart.render();

    // Toggle Between Yearly and Monthly Trends
    const yearlyButton = document.getElementById("yearly-trend");
    const monthlyButton = document.getElementById("monthly-trend");

    yearlyButton.addEventListener("click", () => {
        salesTrendsChart.updateOptions({
            xaxis: {
                categories: yearlyData.categories,
            },
            series: yearlyData.series,
        });
        yearlyButton.classList.add("active");
        monthlyButton.classList.remove("active");
    });

    monthlyButton.addEventListener("click", () => {
        salesTrendsChart.updateOptions({
            xaxis: {
                categories: monthlyData.categories,
            },
            series: monthlyData.series,
        });
        monthlyButton.classList.add("active");
        yearlyButton.classList.remove("active");
    });

    // Initialize Top Selling Products Chart
    const topSellingProductsChart = new ApexCharts(
        document.querySelector(".bar-chart"),
        {
            ...chartOptions,
            chart: {
                ...chartOptions.chart,
                type: "bar",
            },
            colors: ["#28a745"],
            xaxis: {
                // product list
                categories: data.top_selling_products.products,
            },
            yaxis: {
                title: {
                    text: "Unite vendu",
                },
            },
            series: [
                {
                    name: "unite vendu",
                    // quantity sold for each product
                    data: data.top_selling_products.quantities,
                },
            ],
        }
    );
    topSellingProductsChart.render();

    // Initialize Inventory Overview Chart
    const inventoryOverviewChart = new ApexCharts(
        document.querySelector(".pie-chart"),
        {
            chart: {
                type: "pie",
                height: 350,
            },
            colors: [
                "#007bff", "#28a745", "#dc3545", "#ffc107",
                "#0056b3", "#1e7e34", "#a71d2a", "#e0a800",
                "#6c757d", "#17a2b8", "#f8f9fa", "#343a40",
                "#ffffff", "#000000", "#6610f2", "#fd7e14",
                "#20c997", "#ff6b6b", "#4a90e2", "#f4f4f4"
            ],
            // quantity of products left
            series: data.inventory_overview.quantities,
            // products in the inventory
            labels: data.inventory_overview.labels,
            dataLabels: {
                enabled: true,
                formatter: function (val) {
                    return val.toFixed(1) + "%";
                },
            },
            legend: {
                position: "bottom",
            },
        }
    );
    inventoryOverviewChart.render();
}

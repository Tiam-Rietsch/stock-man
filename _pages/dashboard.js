document.addEventListener("DOMContentLoaded", function () {
    // Dummy Data for Charts
    const yearlyData = {
      series: [
        {
          name: "Sales",
          // amount of money sold for each month of the current year
          data: [30, 40, 35, 50, 49, 60, 70, 91, 125, 110, 95, 80],
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
          name: "Sales",
          // amount of money sold for each day of the current month
          data: [
            5, 10, 7, 12, 15, 20, 18, 22, 25, 30, 28, 32, 35, 40, 38, 42, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110,
          ],
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
          text: "Sales ($)",
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
          categories: ["Router", "Switch", "Cable", "Adapter", "Modem", "Hub", "Patch Panel"],
        },
        yaxis: {
          title: {
            text: "Units Sold",
          },
        },
        series: [
          {
            name: "Units Sold",
            // quantity sold for each product
            data: [44, 55, 41, 67, 22, 43, 21],
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
        colors: ["#007bff", "#28a745", "#dc3545", "#ffc107"],
        // quantity of products left
        series: [44, 55, 13, 33],
        // products in the inventory
        labels: ["Routers", "Switches", "Cables", "Adapters"],
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
  });
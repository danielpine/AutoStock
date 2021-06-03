(function (root, factory) {
  if (typeof define === "function" && define.amd) {
    // AMD. Register as an anonymous module.
    define(["exports", "echarts"], factory);
  } else if (
    typeof exports === "object" &&
    typeof exports.nodeName !== "string"
  ) {
    // CommonJS
    factory(exports, require("echarts"));
  } else {
    // Browser globals
    factory({}, root.echarts);
  }
})(this, function (exports, echarts) {
  var log = function (msg) {
    if (typeof console !== "undefined") {
      console && console.error && console.error(msg);
    }
  };
  if (!echarts) {
    log("ECharts is not Loaded");
    return;
  }
  echarts.registerTheme("dark_theme", {
    backgroundColor: "#222",
    valueAxis: {
      axisLine: {
        show: true,
        lineStyle: {
          color: "#eeeeee",
        },
      },
      axisTick: {
        show: true,
        lineStyle: {
          color: "#eeeeee",
        },
      },
      axisLabel: {
        show: true,
        textStyle: {
          color: "#eeeeee",
        },
      },
      splitLine: {
        show: true,
        width: 1,
        lineStyle: {
          color: ["lightgray"],
          opacity: 0.5,
        },
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ["#222"],
        },
      },
    },
    timeAxis: {
      axisLine: {
        show: true,
        lineStyle: {
          color: "#eeeeee",
        },
      },
      axisTick: {
        show: true,
        lineStyle: {
          color: "#eeeeee",
        },
      },
      axisLabel: {
        show: true,
        textStyle: {
          color: "#eeeeee",
        },
      },
      splitLine: {
        show: true,
        width: 1,
        lineStyle: {
          color: ["lightgray"],
          opacity: 0.5,
        },
      },
    },
    toolbox: {
      iconStyle: {
        normal: {
          borderColor: "#999",
        },
        emphasis: {
          borderColor: "#666",
        },
      },
    },
    legend: {
      textStyle: {
        color: "#eeeeee",
      },
    },
    tooltip: {
      axisPointer: {
        lineStyle: {
          color: "#eeeeee",
          width: "1",
        },
        crossStyle: {
          color: "#eeeeee",
          width: "1",
        },
      },
    },
    timeline: {
      lineStyle: {
        color: "#eeeeee",
        width: 1,
      },
      itemStyle: {
        normal: {
          color: "#dd6b66",
          borderWidth: 1,
        },
        emphasis: {
          color: "#a9334c",
        },
      },
      controlStyle: {
        normal: {
          color: "#eeeeee",
          borderColor: "#eeeeee",
          borderWidth: 0.5,
        },
        emphasis: {
          color: "#eeeeee",
          borderColor: "#eeeeee",
          borderWidth: 0.5,
        },
      },
      checkpointStyle: {
        color: "#e43c59",
        borderColor: "rgba(194,53,49, 0.5)",
      },
      label: {
        normal: {
          textStyle: {
            color: "#eeeeee",
          },
        },
        emphasis: {
          textStyle: {
            color: "#eeeeee",
          },
        },
      },
    },
    visualMap: {
      color: ["#bf444c", "#d88273", "#f6efa6"],
    },
    dataZoom: {
      backgroundColor: "rgba(47,69,84,0)",
      dataBackgroundColor: "rgba(255,255,255,0.3)",
      fillerColor: "rgba(167,183,204,0.4)",
      handleColor: "#a7b7cc",
      handleSize: "100%",
      textStyle: {
        color: "#eeeeee",
      },
    },
    markPoint: {
      label: {
        color: "#eee",
      },
      emphasis: {
        label: {
          color: "#eee",
        },
      },
    },
  });
});

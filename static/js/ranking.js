function basic_horizontal_bars(data, ylabels, container) {
  Flotr.draw(
    container,
    [data],
    {
      bars: {
        show: true,
        horizontal: true,
        shadowSize: 0,
        barWidth: 0.5
      },
      mouse: {
        track: true,
        relative: true,
        trackFormatter: function(obj) { return obj.x + ' %'; },
        lineColor: '#FFFFFF'
      },
      yaxis: {
        color: '#FFFFFF',
        ticks: ylabels,
        min: 0,
        autoscaleMargin: 1
      },
      xaxis: {
        color: '#FFFFFF',
        min: 0,
        max: 100
      },
      grid: {
        horizontalLines: false,
        tickColor: '#545454'
      }
    }
  );
}

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

function basic_pie(data, container) {
  var graph;

  graph = Flotr.draw(container, data, {
    grid: {
      color: '#FFFFFF',
      verticalLines: false,
      horizontalLines: false
    },
    xaxis: {
      showLabels: false
    },
    yaxis: {
      showLabels: false
    },
    pie: {
      fontColor: '#FFFFFF',
      show: true,
      explode: 6
    },
    mouse: {
      track: true,
      relative: true,
      trackFormatter: function(obj) { return obj.series.label + ': ' + obj.y + ' 社'; },
      lineColor: '#FFFFFF'
    },
    legend: {
      position: 'se',
      backgroundColor: '#777'
    }
  });
}
/*
Flotr.addPlugin('clickHit', {
  callbacks: {
    'flotr:click': function(e) {
      this.clickHit.clickHit(e);
    }
  },
  clickHit: function(mouse) {
    console.log(mouse);
    if (mouse.index || mouse.index == 0) {
      alert('You hit ' + mouse.yaxis.ticks[mouse.index].label);
    }
  }
});
*/

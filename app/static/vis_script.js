function InitChart(wordData) {

            console.log(wordData);
            var barData = wordData[1];
            var vis = d3.select('#visualisation'),
                WIDTH = 1000,
                HEIGHT = 400,
                MARGINS = {
                    top: 20,
                    right: 20,
                    bottom: 40,
                    left: 50
                },
                xRange = d3.scale.ordinal().rangeRoundBands([MARGINS.left, WIDTH - MARGINS.right], 0.1).domain(barData.map(function(d) {
                    return d.x;
                })),


                yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0,
                    d3.max(barData, function(d) {
                        return d.y;
                    })
                ]),

                xAxis = d3.svg.axis()
                .tickFormat(function(d) {

                    if (d % 100 == 1) {
                        return Math.floor(d / 100)
                    } else {
                        return
                    }
                })
                .scale(xRange)
                .tickSize(5)
                .tickSubdivide(true)
                .ticks(10),

                yAxis = d3.svg.axis()
                .scale(yRange)
                .tickSize(5)
                .orient("left")
                .tickSubdivide(true);

            vis.append('svg:g')
                .attr('class', 'x axis')
                .attr('transform', 'translate(0,' + (HEIGHT - MARGINS.bottom) + ')')
                .call(xAxis);

            vis.append('svg:g')
                .attr('class', 'y axis')
                .attr('transform', 'translate(' + (MARGINS.left) + ',0)')
                .call(yAxis);

            vis.selectAll('rect')
                .data(barData)
                .enter()
                .append('rect')
                .attr('x', function(d) {
                    return xRange(d.x);
                })
                .attr('y', function(d) {
                    return yRange(d.y);
                })
                .attr('width', xRange.rangeBand())
                .attr('height', function(d) {
                    return ((HEIGHT - MARGINS.bottom) - yRange(d.y));
                })
                .attr({
                    ry: '3',
                    rx: '3'
                })
                .attr('fill', '#dfdfdf')
                .style("opacity", .65)
                .on('mouseover', function(d) {
                    d3.select(this)
                        .attr('fill', 'white');
                })
                .on('mouseout', function(d) {
                    d3.select(this)
                        .attr('fill', '#dfdfdf');
                });

        }
var line = d3.line();
var step = d3.line().curve(d3.curveStep);
var stepAfter = d3.line().curve(d3.curveStepAfter);
var stepBefore = d3.line().curve(d3.curveStepBefore);


// https://gist.github.com/Rokotyan/0556f8facbaf344507cdc45dc3622177
// Below are the functions that handle actual exporting:
// getSVGString ( svgNode ) and svgString2Image( svgString, width, height, format, callback )
function getSVGString( svgNode ) {
	svgNode.setAttribute('xlink', 'http://www.w3.org/1999/xlink');
	var cssStyleText = getCSSStyles();
	appendCSS( cssStyleText, svgNode );
	var serializer = new XMLSerializer();
	var svgString = serializer.serializeToString(svgNode);
	svgString = svgString.replace(/(\w+)?:?xlink=/g, 'xmlns:xlink='); // Fix root xlink without namespace
	svgString = svgString.replace(/NS\d+:href/g, 'xlink:href'); // Safari NS namespace fix
	return svgString;

	function getCSSStyles() {
		// Extract CSS Rules
		var extractedCSSText = "";
		for (var i = 0; i < document.styleSheets.length; i++) {
			var s = document.styleSheets[i];
            try {
			    if(!s.cssRules) continue;
			} catch( e ) {
                if(e.name !== 'SecurityError') throw e; // for Firefox
                continue;
		    }
			var cssRules = s.cssRules;
			for (var r = 0; r < cssRules.length; r++) {
				extractedCSSText += cssRules[r].cssText;
			}
		}
		return extractedCSSText;

	}

	function appendCSS( cssText, element ) {
		var styleElement = document.createElement("style");
		styleElement.setAttribute("type","text/css"); 
		styleElement.innerHTML = cssText;
		var refNode = element.hasChildNodes() ? element.children[0] : null;
		element.insertBefore( styleElement, refNode );
	}
}


function svgString2Image( svgString, width, height, format, callback ) {
	var format = format ? format : 'png';
	var imgsrc = 'data:image/svg+xml;base64,'+ btoa( unescape( encodeURIComponent( svgString ) ) ); // Convert SVG string to data URL
	var canvas = document.createElement("canvas");
	var context = canvas.getContext("2d");
	canvas.width = width;
	canvas.height = height;
	var image = new Image();
	image.onload = function() {
		context.clearRect ( 0, 0, width, height);
		context.drawImage(image, 0, 0, width, height);
		canvas.toBlob( function(blob) {
			var filesize = Math.round( blob.length/1024 ) + ' KB';
			if ( callback ) callback( blob, filesize );
		});
	};
	image.src = imgsrc;
}

function draw_force_diagram() {
    
    var graph = $data;
    var y_axis = $y_axis;
    var edge_styles = $edges;
    var title = "$title";

    var evenly_distributed_positions = graph.evenly_distributed_positions;

    var dashboard = d3.select("#arg_${divnum}").append("div").attr("class", "dashboard");
    
    var saving = dashboard.append("button").attr("class", "dashbutton");
    saving.append("svg") //<!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
        .attr("xmlns", "http://www.w3.org/2000/svg")
        .attr("viewBox", "0 0 512 512")
        .append("path")
        .attr("d", "M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32V274.7l-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7V32zM64 352c-35.3 0-64 28.7-64 64v32c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V416c0-35.3-28.7-64-64-64H346.5l-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352H64zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z");
    var saving_methods = saving.append("span").attr("class", "tip desc");
    var methods = saving_methods.append("div").text("Download As:").append("div").attr("class", "savemethods")
    
    methods.append("button").text("JSON")
        .on("click", function() {
            d3.selectAll("#arg_${divnum} .node").classed("fix", function(d) {
                d.fx = d.x;
            });
            var textBlob = new Blob(["${source}".replace(/'nodes': .*'links'/, "'nodes': " + JSON.stringify(graph.nodes) + ", 'links'").replaceAll("'", '"')], {type: "text/plain"});
            saveAs(textBlob, "tskit_arg_visualizer.json");
        });
    methods.append("button").text("SVG")
        .on('click', function(){
            var svgString = getSVGString(svg.node());
            var svgBlob = new Blob([svgString], {type:"image/svg+xml;charset=utf-8"});
            saveAs( svgBlob, "tskit_arg_visualizer");
        });
    methods.append("button").text("PNG")
        .on('click', function(){
            var svgString = getSVGString(svg.node());
            svgString2Image(svgString, 2*$width, 2*$height, 'png', save); // passes Blob and filesize String to the callback
        
            function save(dataBlob){
                saveAs(dataBlob, "tskit_arg_visualizer"); // FileSaver.js function
            }
        });

    var reheat = dashboard.append("button").attr("class", "dashbutton activecolor")
        .on("click", function(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();       
            var order = d3.selectAll("#arg_${divnum} .flag1").data().sort((a, b) => d3.ascending(a.x, b.x)).map(a => a.id);;
            d3.selectAll("#arg_${divnum} .node").classed("unfix", function(d) {
                if ((d.flag != 1) & (d.x_pos_reference == -1)) {
                    delete d.fx;
                } else {
                    d.fx = evenly_distributed_positions[order.indexOf(d.id)];
                }
            });
        });
    reheat.append("svg") //<!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
        .attr("xmlns", "http://www.w3.org/2000/svg")
        .attr("viewBox", "0 0 384 512")
        .append("path")
        .attr("d", "M153.6 29.9l16-21.3C173.6 3.2 180 0 186.7 0C198.4 0 208 9.6 208 21.3V43.5c0 13.1 5.4 25.7 14.9 34.7L307.6 159C356.4 205.6 384 270.2 384 337.7C384 434 306 512 209.7 512H192C86 512 0 426 0 320v-3.8c0-48.8 19.4-95.6 53.9-130.1l3.5-3.5c4.2-4.2 10-6.6 16-6.6C85.9 176 96 186.1 96 198.6V288c0 35.3 28.7 64 64 64s64-28.7 64-64v-3.9c0-18-7.2-35.3-19.9-48l-38.6-38.6c-24-24-37.5-56.7-37.5-90.7c0-27.7 9-54.8 25.6-76.9z");
    reheat.append("span").attr("class", "tip desc").text("Reheat Simulation");
    
    var evenly_distribute = dashboard.append("button").attr("class", "dashbutton activecolor")
        .on("click", function() {
            var order = d3.selectAll("#arg_${divnum} .flag1").data().sort((a, b) => d3.ascending(a.x, b.x)).map(a => a.id);;
            d3.selectAll("#arg_${divnum} .flag1").classed("distribute", function(d) {
                d.fx = evenly_distributed_positions[order.indexOf(d.id)];
            });
        });
    evenly_distribute.append("svg") //<!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
        .attr("xmlns", "http://www.w3.org/2000/svg")
        .attr("viewBox", "0 0 512 512")
        .append("path")
        .attr("d", "M504.3 273.6c4.9-4.5 7.7-10.9 7.7-17.6s-2.8-13-7.7-17.6l-112-104c-7-6.5-17.2-8.2-25.9-4.4s-14.4 12.5-14.4 22l0 56-192 0 0-56c0-9.5-5.7-18.2-14.4-22s-18.9-2.1-25.9 4.4l-112 104C2.8 243 0 249.3 0 256s2.8 13 7.7 17.6l112 104c7 6.5 17.2 8.2 25.9 4.4s14.4-12.5 14.4-22l0-56 192 0 0 56c0 9.5 5.7 18.2 14.4 22s18.9 2.1 25.9-4.4l112-104z")
    evenly_distribute.append("span").attr("class", "tip desc").text("Space Samples");

    var svg = d3.select("#arg_${divnum}").append("svg")
        .attr("width", $width)
        .attr("height", $height)
        .style("background-color", "white");

    var result = y_axis.ticks.map(function (x) { 
        return parseInt(x, 10); 
    });

    if (eval(y_axis.include_labels)) {
        var bottom = $height - 50;
        if ($tree_highlighting) {
            bottom = $height - 125;
        }
        var top = 50;
        if (title != "None") {
            top = 100
        }
        var yscale = d3.scaleLinear() 
            .domain([y_axis.max_min[0], y_axis.max_min[1]]) 
            .range([bottom, top]); 

        var y_axis_text = y_axis.text;

        var y_axis = d3.axisRight().scale(yscale)
            .tickValues(result)
            .tickFormat((d, i) => y_axis_text[i]); 

        var y_axis_labels = svg
            .append("g")
            .attr("class", "yaxis")
            .attr("transform", "translate(5,0)")
            .call(y_axis);
    }

    var simulation = d3
        .forceSimulation(graph.nodes)
        .force("link", d3.forceLink()
            .id(function(d) {
                return d.id;
            })
            .links(graph.links)
        )
        //.force("center", d3.forceCenter(275,250).strength(-10))
        .force("charge", d3.forceManyBody().strength(-100))
        .on("tick", ticked);

    var link_container = svg
        .append("g")
        .attr("class", "links")
        .selectAll("path")
        .data(graph.links)
        .enter()
        .append("g")
        .attr("bounds", function(d) {
            return d.bounds;
        });

    if ((edge_styles.type == "ortho") & eval(edge_styles.include_underlink)) {
        var underlink = link_container
            .append("path")
            .attr("class", "underlink");
    }

    var link = link_container
        .append("path")
        .attr("class", function(d) {
            return "link"
        })
        .attr("stroke", function(d) {
            return d.color;
        });
    
    if (eval(edge_styles.variable_width)) {
        link
            .style("stroke-width", function(d) {
                return d.region_fraction * 7 + 1;
            });
    }
    
    if ($tree_highlighting) {
        d3.selectAll(".link")
            .on('mouseover', function (event, d) {
                d3.select(this)
                    .style('stroke', '#1eebb1')
                    .style("cursor", "pointer");
                d3.select("#arg_${divnum} .breakpoints")
                    .selectAll(".included")
                        .filter(function(j) {
                            return d.bounds.split(" ").some(function(region) {
                                region = region.split("-");
                                return (parseFloat(region[0]) <= j.start) & (parseFloat(region[1]) >= j.stop)
                            });
                        })
                        .style('fill', '#1eebb1');
            })
            .on('mouseout', function (d, i) {
                d3.select(this)
                    .style('stroke', function(d) {
                        return d.color;
                    })
                    .style("cursor", "default")
                d3.select("#arg_${divnum} .breakpoints").selectAll(".included")
                    .style("fill", "#053e4e")
            });
    }

    var node_group = svg
        .append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(graph.nodes)
        .enter()
        .append("g");

    var missing_edges = node_group
        .filter(function(d) { return (d.not_included_parents>0) | (d.not_included_children>0); })
        .append("g")
        .attr("class", "missing");

    var missing_parents = missing_edges
        .filter(function(d) { return d.not_included_parents>0; })
        .append("g")
        .attr("class", "parents")
        .append("g");
    var missing_parents_paths = missing_parents.append("path");
    var missing_parents_texts = missing_parents
        .append("text")
            .attr("class", function(d) {
                return "label"
            })
            .style("fill", "gray")
            .text(function(d) { return d.not_included_parents;});

    var missing_children = missing_edges
        .filter(function(d) { return d.not_included_children>0; })
        .append("g")
        .attr("class", "children")
        .append("g");
    var missing_children_paths = missing_children.append("path");
    var missing_children_texts = missing_children
        .append("text")
            .attr("class", function(d) {
                return "label"
            })
            .style("fill", "gray")
            .text(function(d) { return d.not_included_children;});


    var node = node_group
        .append("path")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
        .attr("d", d3.symbol().type(function(d) { return eval(d.symbol); }).size(function(d) { return d.size; }))
        .attr("fill", function(d) { return d.fill; })
        .attr("stroke", function(d) { return d.stroke; })
        .attr("stroke-width", function(d) { return d.stroke_width; })
        .attr("id", function(d) { return String($divnum) + "_node" + d.id; })
        .attr("class", function(d) {
            return "node flag" + d.flag
        })
        .attr("parents", function(d) { return d.child_of.toString().replace(",", " "); })
        .attr("children", function(d) { return d.parent_of.toString().replace(",", " "); })
        .call(
            d3
                .drag()
                .on("start", dragstarted)
                .on("drag", dragged)
        )
        .on('mouseover', function (d, i) {
            d3.select(this)
                .style("cursor", "pointer")
        });

    var label = svg
        .append("g")
        .attr("class", "labels")
        .selectAll("text")
        .data(graph.nodes)
        .enter()
        .filter(function(d) { return eval(d.include_label); })
        .append("text")
            .attr("class", function(d) {
                return "label"
            })
            .text(function (d) { return d.label; });

    function determine_path_type(d) {
        path_type = ""
        var start_position_x = d.source.x;
        var start_position_y = d.source.y;
        var stop_position_x = d.target.x;
        var stop_position_y = d.target.y;
        var vnub = Math.min((stop_position_y-start_position_y)/2, 20);
        if ("y_axis.scale" == "time" | "y_axis.scale" == "log_time") {
            vnub = 0;
        }
        var alt_child = document.getElementById(String($divnum) + "_node" + d.alt_child);
        if (alt_child != null) {
            var alt_child_x = alt_child.getAttribute("cx");
            var alt_child_y = alt_child.getAttribute("cy");
        }
        if (d.source.flag == 131072) {
            path_type += "r0";
            start_position_y = d.source.y + vnub;
        } else {
            if (d.target.y < alt_child_y) {
                if (d.target.x < d.source.x) {
                    if (d.target.x < d.source.x - 40) {
                        path_type += "tL";
                    } else {
                        path_type += "fL";
                    }
                    start_position_x = d.source.x - 20;
                } else {
                    if (d.target.x > d.source.x + 40) {
                        path_type += "tR";
                    } else {
                        path_type += "fR";
                    }
                    start_position_x = d.source.x + 20;
                }
            } else if (d.target.y > alt_child_y) {
                if (alt_child_x < d.source.x) {
                    if (d.target.x < d.source.x + 40) {
                        path_type += "fR";
                    } else {
                        path_type += "tR";
                    }
                    start_position_x = d.source.x + 20;
                } else {
                    if (d.target.x > d.source.x - 40) {
                        path_type += "fL";
                    } else {
                        path_type += "tL";
                    }
                    start_position_x = d.source.x - 20;
                }
            } else {
                if (d.target.x < alt_child_x) {
                    if (d.target.x < d.source.x - 40) {
                        path_type += "tL";
                    } else {
                        path_type += "fL";
                    }
                    start_position_x = d.source.x - 20;
                } else if (d.target.x > alt_child_x) {
                    if (d.target.x > d.source.x + 40) {
                        path_type += "tR";
                    } else {
                        path_type += "fR";
                    }
                    start_position_x = d.source.x + 20;
                } else {
                    if (d.index % 2 == 0) {
                        path_type += "fL";
                        start_position_x = d.source.x - 20;
                    } else {
                        path_type += "fR";
                        start_position_x = d.source.x + 20;
                    }
                }
            }
        }
        var alt_parent = document.getElementById(String($divnum) + "_node" + d.alt_parent);
        if (alt_parent != null) {
            var alt_parent_x = alt_parent.getAttribute("cx");
            var alt_parent_y = alt_parent.getAttribute("cy");
        }
        if (d.target.flag == 131072) {
            if (d.source.y < alt_parent_y) {
                if (alt_parent_x < d.target.x) {
                    if (d.source.x < d.target.x + 40) {
                        path_type += "fR";
                    } else {
                        path_type += "tR";
                    }
                    stop_position_x = d.target.x + 20;
                } else {
                    if (d.source.x > d.target.x - 40) {
                        path_type += "fL";
                    } else {
                        path_type += "tL";
                    }
                    stop_position_x = d.target.x - 20;
                }
            } else if (d.source.y > alt_parent_y) {
                if (d.source.x < d.target.x) {
                    if (d.source.x < d.target.x - 40) {
                        path_type += "tL";
                    } else {
                        path_type += "fL";
                    }
                    stop_position_x = d.target.x - 20;
                } else {
                    if (d.source.x > d.target.x + 40) {
                        path_type += "tR";
                    } else {
                        path_type += "fR";
                    }
                    stop_position_x = d.target.x + 20;
                }
            } else {
                if (d.index % 2 == 0) {
                    path_type += "fL";
                    stop_position_x = d.target.x - 20;
                } else {
                    path_type += "fR";
                    stop_position_x = d.target.x + 20;
                }
            }
        } else {
            path_type += "b0";
            stop_position_y = d.target.y - vnub;
        }
        if (path_type == "fLb0" ) {
            if (start_position_x >= stop_position_x) {
                path_type = "tLb0";
            }
        } else if (path_type == "fRb0") {
            if (start_position_x <= stop_position_x) {
                path_type = "tRb0";
            }
        } else if (path_type == "r0fL") {
            if (start_position_x <= stop_position_x) {
                path_type = "r0tL";
            }
        } else if (path_type == "r0fR") {
            if (start_position_x >= stop_position_x) {
                path_type = "r0tR";
            }
        } else if (path_type == "fLfL") {
            if (start_position_x <= stop_position_x) {
                path_type = "fLtL";
            } else {
                path_type = "tLfL";
            }
        } else if (path_type == "fRfR") {
            if (start_position_x >= stop_position_x) {
                path_type = "fRtR";
            } else {
                path_type = "tRfR";
            }
        }
        return [path_type, start_position_x, start_position_y, stop_position_x, stop_position_y];
    }

    function ortho_pathing(d, path_info) {      
        const path_type = path_info[0];
        const simple_path_type = Array.from(path_type)[0] + Array.from(path_type)[2];
        const start_position_x = path_info[1];
        const start_position_y = path_info[2];
        const stop_position_x = path_info[3];
        const stop_position_y = path_info[4];

        const after_paths = ["rf", "tb", "tf"];
        const before_paths = ["rt", "fb", "ft"];
        const step_paths = ["tt"];
        const mid_paths = ["rb", "ff"];

        if (after_paths.includes(simple_path_type)) {
            return line([[d.source.x, d.source.y],[start_position_x, start_position_y]]) + stepAfter([[start_position_x, start_position_y],[stop_position_x, stop_position_y]]) + line([[stop_position_x, stop_position_y], [d.target.x, d.target.y]]);
        } else if (before_paths.includes(simple_path_type)) {
            return line([[d.source.x, d.source.y],[start_position_x, start_position_y]]) + stepBefore([[start_position_x, start_position_y],[stop_position_x, stop_position_y]]) + line([[stop_position_x, stop_position_y], [d.target.x, d.target.y]]);
        } else if (step_paths.includes(simple_path_type)) {
            return line([[d.source.x, d.source.y],[start_position_x, start_position_y]]) + step([[start_position_x, start_position_y],[stop_position_x, stop_position_y]]) + line([[stop_position_x, stop_position_y], [d.target.x, d.target.y]]);
        } else if (mid_paths.includes(simple_path_type)) {
            return line([[d.source.x, d.source.y],[start_position_x, start_position_y]]) + line([[start_position_x, start_position_y],[start_position_x, start_position_y + (stop_position_y - start_position_y)/2]]) + line([[start_position_x, start_position_y + (stop_position_y - start_position_y)/2],[stop_position_x, start_position_y + (stop_position_y - start_position_y)/2]]) + line([[stop_position_x, start_position_y + (stop_position_y - start_position_y)/2], [stop_position_x, stop_position_y]]) + line([[stop_position_x, stop_position_y], [d.target.x, d.target.y]]);
        }
    }

    function ticked() {

        node
            .attr("transform", function(d) {
                if (eval(y_axis.include_labels)) {
                    return "translate(" + Math.max(50, Math.min($width-50, d.x)) + "," + d.y + ")";
                } else {
                    return "translate(" + Math.max(100, Math.min($width-50, d.x)) + "," + d.y + ")";
                }
            })
            .attr("cx", function(d) {
                if ((edge_styles.type == "ortho") & (d.x_pos_reference != -1)) {
                    var ref = document.getElementById(String($divnum) + "_node" + d.x_pos_reference);
                    if (ref != null) {
                        d.fx = ref.getAttribute("cx");
                    }
                }
                if (eval(y_axis.include_labels)) {
                    return d.x = Math.max(50, Math.min($width-50, d.x));
                } else {
                    return d.x = Math.max(100, Math.min($width-50, d.x));
                }
            })
            .attr("cy", function(d) {
                return d.y;
            });
        
        link_container.each(function(d) {
            var path_info = determine_path_type(d);
            var path = "";
            if (edge_styles.type == "ortho") {
                path = ortho_pathing(d, path_info);
            } else if (d.source.id == d.alt_parent) {
                var leftOrRight = 20;
                if (d.index % 2 == 0) {
                    leftOrRight = -20;
                }
                path = "M " + d.source.x + " " + d.source.y + " C " + (d.source.x + leftOrRight).toString() + " " +  (d.source.y - 10).toString() + ", " + (d.target.x + leftOrRight).toString() + " " + (d.target.y + 10).toString() + ", " + d.target.x + " " + d.target.y;
            } else {
                path = line([[d.source.x, d.source.y], [d.target.x, d.target.y]]);
            }
            if ((edge_styles.type == "ortho") & eval(edge_styles.include_underlink)) {
                var u = d3.select(this).select(".underlink");
                u.attr("d", path);
            }
            var l = d3.select(this).select(".link");
            l.attr("path_type", path_info[0]);
            l.attr("d", path);
        })

        function determine_label_positioning(d) {
            if (d.flag == 131072 || d.parent_of.length == 0 || d.child_of.length == 0) {
                return "c";
            } else if (d.child_of.length == 1) {
                var parent = document.getElementById(String($divnum) + "_node" + d.child_of[0])
                if (parent != null) {
                    var parent_x = parent.getAttribute("cx");
                    if (parent_x > d.x+1) {
                        return "l";
                    } else {
                        return "r";
                    }
                } else {
                    return "r";
                }
            } else {
                return "r";
            }
        };

        label
            .each(function(d) {
                var l = d3.select(this);
                var positioning = determine_label_positioning(d);
                var x = d.x;
                var anchor = "middle";
                if (positioning == "l") {
                    x = d.x - 15;
                    anchor = "end";
                } else if (positioning == "r") {
                    x = d.x + 15;
                    anchor = "start";
                }
                l.attr("x", x);
                l.attr("text-anchor", anchor);
                l.attr("y", function(d) {
                    if (d.parent_of.length == 0) {
                        return d.y + 25;
                    } else {
                        return d.y - 15;
                    }
                });
            });

        missing_parents_paths
            .each(function(d) {
                var l = d3.select(this);
                l.style("stroke-width", "4px");
                l.style("stroke-dasharray", "5");
                l.style("stroke", "gray");
                l.attr("d", line([[d.x, d.y], [d.x, d.y-30]]));
            });
        
        missing_parents_texts
            .each(function(d) {
                var l = d3.select(this);
                l.attr("text-anchor", "middle");
                l.attr("x", d.x);
                l.attr("y", d.y-30);
            });

        missing_children_paths
            .each(function(d) {
                var l = d3.select(this);
                l.style("stroke-width", "4px");
                l.style("stroke-dasharray", "5");
                l.style("stroke", "gray");
                l.attr("d", line([[d.x, d.y], [d.x, d.y+30]]));
            });
        
        missing_children_texts
            .each(function(d) {
                var l = d3.select(this);
                l.attr("text-anchor", "middle");
                l.attr("x", d.x);
                l.attr("y", d.y+40);
            });
    }

    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d3.selectAll("#arg_${divnum} .node").classed("ref", function(j) {
            if ((edge_styles.type == "ortho") & (j.id == d.x_pos_reference)) {
                j.fx = d.x;
            }
        });
    }

    function dragged(event, d) {
        d.fx = event.x;
        d3.selectAll("#arg_${divnum} .node").classed("ref", function(j) {
            if ((edge_styles.type == "ortho") & (j.id == d.x_pos_reference)) {
                j.fx = event.x;
            }
        });
    }

    if ($tree_highlighting) {
        
        var th_group = svg.append("g").attr("class", "tree_highlighting");
        
        th_group
            .append("g")
            .attr("class", "breakpoints")
            .selectAll("rect")
            .data(graph.breakpoints)
            .enter()
            .append("rect")
            .attr("class", function(d) {
                if (eval(d.included)) {
                    return "included";
                }
            })
            .attr("start", function(d) {
                return d.start;
            })
            .attr("stop", function(d) {
                return d.stop;
            })
            .attr("x", function(d) {
                return d.x_pos;
            })
            .attr("y", $height-60)
            .attr("width", function(d) {
                return d.width;
            })
            .attr("height", 40)
            .attr("stroke", "#FFFFFF")
            .attr("stroke-width", 1)
            .attr("fill", function(d) {
                if (eval(d.included)) {
                    return "#053e4e";
                } else {
                    return "gray";
                }
            })
            .on('mouseover', function (event, d) {
                if (eval(d.included)) {
                    d3.select(this)
                        .style('fill', '#1eebb1')
                        .style("cursor", "pointer");
                    var highlight_links = d3.select("#arg_${divnum} .links")
                        .selectAll("g")
                            .filter(function(j) {
                                return j.bounds.split(" ").some(function(region) {
                                    region = region.split("-");
                                    return (parseFloat(region[1]) > d.start) & (parseFloat(region[0]) < d.stop)
                                });
                            });
                    highlight_links.raise();
                    highlight_links
                        .select(".link")
                        .style("stroke", "#1eebb1");
                }
            })
            .on('mouseout', function (event, d) {
                if (eval(d.included)) {
                    d3.select(this)
                        .style('fill', '#053e4e')
                        .style("cursor", "default");
                    d3.selectAll("#arg_${divnum} .link")
                        .style("stroke", function(d) {
                            return d.color;
                        });
                }
            });
        
        var endpoints = th_group.append("g").attr("class", "endpoints");
        
        endpoints
            .append("text")
                .attr("class", "label")
                .style("text-anchor", "start")
                .text(graph.breakpoints[0].start)
                .attr("x", graph.breakpoints[0].x_pos)
                .attr("y", $height-5);
        
        endpoints
            .append("text")
                .attr("class", "label")
                .style("text-anchor", "end")
                .text(graph.breakpoints[graph.breakpoints.length-1].stop)
                .attr("x", $width)
                .attr("y", $height-5);
    }

    if (title != "None") {
        svg.append("text")
            .attr("class", "label")
            .text(title)
            .style("font-size", "20px")
            .attr("x", $width / 2)
            .style("transform", "translate(-50%, 50%)")
            .attr("y", 30);
    }
}

draw_force_diagram()
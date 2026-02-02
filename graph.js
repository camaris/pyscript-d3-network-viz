// src/graph.js

/**
 * Renders the Force-Directed Graph using D3.js
 * @param {Object} graphData - The data object containing nodes and links.
 */
function renderGraph(graphData) {
    // Clear previous graph if any (for re-rendering)
    d3.select("#graph").selectAll("*").remove();

    const width = window.innerWidth;
    const height = window.innerHeight;

    // Create the main SVG element
    const svgObject = d3.select("#graph")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    // Define defs for markers (arrows)
    const defs = svgObject.append("defs");
    defs.append("marker")
        .attr("id", "arrow-end")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 32) // Offset for node radius + gap
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("fill", "#94a3b8");

    // Define Glow Filter
    const filter = defs.append("filter")
        .attr("id", "glow")
        .attr("x", "-100%")
        .attr("y", "-100%")
        .attr("width", "800%")
        .attr("height", "300%");

    // 1. Blur the source to create the glow
    filter.append("feGaussianBlur")
        .attr("stdDeviation", "20")
        .attr("result", "coloredBlur");

    // 2. Merge the blur (behind) and the sharp source (front)
    const feMerge = filter.append("feMerge");
    feMerge.append("feMergeNode").attr("in", "coloredBlur");
    feMerge.append("feMergeNode").attr("in", "SourceGraphic");

    // Create a container group <g> for the graph elements (zoom target)
    const container = svgObject.append("g");

    // Define Zoom Behavior
    const zoomBehavior = d3.zoom()
        .scaleExtent([0.1, 4])
        .on("zoom", (event) => {
            container.attr("transform", event.transform);
        });

    // Attach Zoom to the SVG (empty space panning works this way)
    svgObject.call(zoomBehavior);

    // Simulation setup
    const simulation = d3.forceSimulation(graphData.nodes)
        .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(150))
        .force("charge", d3.forceManyBody().strength(-400))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collide", d3.forceCollide(30)); // Avoid overlap

    // Draw Links Group (Line + Text)
    const linkGroup = container.append("g")
        .attr("class", "links")
        .selectAll("g")
        .data(graphData.links)
        .enter().append("g");

    const linkLine = linkGroup.append("line")
        .attr("class", "link")
        .style("stroke-width", d => (d.extra_style && d.extra_style.stroke_width) ? d.extra_style.stroke_width + "px" : null)
        .style("stroke", d => (d.extra_style && d.extra_style.color) ? d.extra_style.color : null)
        .style("stroke-dasharray", d => (d.extra_style && d.extra_style.dash) ? d.extra_style.dash : null)
        .style("stroke-opacity", d => (d.extra_style && d.extra_style.opacity) ? d.extra_style.opacity : null)
        .attr("marker-end", d => (d.extra_style && d.extra_style.arrow) ? "url(#arrow-end)" : null);

    // Link Labels
    const linkText = linkGroup.append("text")
        .attr("text-anchor", "middle")
        .attr("dy", -3) // Slight offset above the line
        .text(d => (d.extra_style && d.extra_style.label) ? d.extra_style.label : "")
        .style("font-size", d => (d.extra_style && d.extra_style.font_size) ? d.extra_style.font_size : "10px")
        .style("fill", d => (d.extra_style && d.extra_style.color) ? d.extra_style.color : "#94a3b8")
        .style("opacity", 0.8)
        .style("pointer-events", "none");

    // Draw Nodes
    const node = container.append("g")
        .attr("class", "nodes")
        .selectAll("g")
        .data(graphData.nodes)
        .enter().append("g")
        .attr("class", "node")
        .call(drag(simulation))
        .on("mouseover", (event, d) => {
            // Get neighbors
            const neighbors = new Set();
            graphData.links.forEach(link => {
                if (link.source.id === d.id) neighbors.add(link.target.id);
                if (link.target.id === d.id) neighbors.add(link.source.id);
            });
            neighbors.add(d.id);

            // Dim everything
            node.style("opacity", 0.1);
            linkLine.style("opacity", 0.1);
            linkText.style("opacity", 0.1);

            // Highlight neighbors and self
            node.filter(n => neighbors.has(n.id))
                .style("opacity", 1);

            // Highlight connected links
            linkLine.filter(l => l.source.id === d.id || l.target.id === d.id)
                .style("opacity", 1);

            // Highlight connected link labels
            linkText.filter(l => l.source.id === d.id || l.target.id === d.id)
                .style("opacity", 1);
        })
        .on("mouseout", (event, d) => {
            // Reset Nodes
            node.style("opacity", n => (n.extra_style && n.extra_style.opacity) ? n.extra_style.opacity : 1);

            // Reset Links
            linkLine.style("stroke-opacity", l => (l.extra_style && l.extra_style.opacity) ? l.extra_style.opacity : null)
                .style("opacity", 1); // Reset base opacity (modified by hover)

            // Reset Link Labels
            linkText.style("opacity", 0.8);
        });

    // Node Circles
    node.append("circle")
        .attr("r", d => (d.extra_style && d.extra_style.radius) ? d.extra_style.radius : 20)
        .style("fill", d => (d.extra_style && d.extra_style.color) ? d.extra_style.color : null)
        .style("stroke", d => (d.extra_style && d.extra_style.stroke_color) ? d.extra_style.stroke_color : null)
        .style("stroke-width", d => (d.extra_style && d.extra_style.stroke_width) ? d.extra_style.stroke_width : null)
        .style("stroke-dasharray", d => (d.extra_style && d.extra_style.stroke_dash) ? d.extra_style.stroke_dash : null)
        .style("opacity", d => (d.extra_style && d.extra_style.opacity) ? d.extra_style.opacity : 1)
        .style("filter", d => (d.extra_style && d.extra_style.glow) ? "url(#glow)" : null)
        .append("title")
        .text(d => {
            let tooltip = d.id;
            if (d.extra_data) {
                tooltip += `\n${JSON.stringify(d.extra_data, null, 2)}`;
            }
            return tooltip;
        });

    // Node Icons via ForeignObject (FontAwesome)
    node.append("foreignObject")
        .filter(d => d.extra_style && d.extra_style.icon)
        .attr("width", d => (d.extra_style.radius ? d.extra_style.radius * 2 : 40))
        .attr("height", d => (d.extra_style.radius ? d.extra_style.radius * 2 : 40))
        .attr("x", d => (d.extra_style.radius ? -d.extra_style.radius : -20))
        .attr("y", d => (d.extra_style.radius ? -d.extra_style.radius : -20))
        .style("pointer-events", "none")
        .append("xhtml:div")
        .style("width", "100%")
        .style("height", "100%")
        .style("display", "flex")
        .style("align-items", "center")
        .style("justify-content", "center")
        .style("color", d => (d.extra_style.icon_color) ? d.extra_style.icon_color : "#fff")
        .html(d => `<i class="${d.extra_style.icon}" style="font-size: ${d.extra_style.icon_size || '16px'};"></i>`);

    // Node Labels
    node.append("text")
        .attr("dy", d => (d.extra_style && d.extra_style.radius) ? d.extra_style.radius + 15 : 35)
        .attr("text-anchor", "middle")
        .text(d => d.id)
        .style("font-size", d => (d.extra_style && d.extra_style.font_size) ? d.extra_style.font_size : "12px")
        .style("font-weight", d => (d.extra_style && d.extra_style.font_weight) ? d.extra_style.font_weight : "normal")
        .style("fill", d => (d.extra_style && d.extra_style.text_color) ? d.extra_style.text_color : null)
        .style("paint-order", "stroke")
        .style("stroke", d => (d.extra_style && d.extra_style.text_outline) ? d.extra_style.text_outline : null)
        .style("stroke-width", d => (d.extra_style && d.extra_style.text_outline) ? "3px" : null);


    // Tick Function
    simulation.on("tick", () => {
        linkLine
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        linkText
            .attr("x", d => (d.source.x + d.target.x) / 2)
            .attr("y", d => (d.source.y + d.target.y) / 2);

        node
            .attr("transform", d => `translate(${d.x},${d.y})`);
    });

    // --- Interactive Controls ---

    // 1. Gravity (Charge)
    d3.select("#gravityRange").on("input", function () {
        const val = +this.value;
        simulation.force("charge").strength(val);
        simulation.alpha(0.5).restart(); // Re-heat simulation
    });

    // 2. Link Distance
    d3.select("#linkDistRange").on("input", function () {
        const val = +this.value;
        simulation.force("link").distance(val);
        simulation.alpha(0.5).restart();
    });

    // 3. Reset View
    d3.select("#resetBtn").on("click", () => {
        // Reset Zoom
        d3.select("#graph svg").transition().duration(750).call(zoomBehavior.transform, d3.zoomIdentity);
    });

    // --- Dynamic Filters ---
    const types = new Set();
    graphData.nodes.forEach(d => {
        // Checking extra_data for role or type, then generic group
        let type = "Unknown";
        if (d.extra_data) {
            if (d.extra_data.role) type = d.extra_data.role;
            else if (d.extra_data.type) type = d.extra_data.type;
            else if (d.extra_data.value) type = "Value";
        } else if (d.group) {
            type = "Group " + d.group;
        }
        types.add(type);
    });

    const filterContainer = d3.select("#filter-controls");
    filterContainer.html(""); // Clear existing

    // Track active filters
    const activeFilters = new Set(types);

    types.forEach(type => {
        const row = filterContainer.append("div")
            .style("display", "flex")
            .style("align-items", "center")
            .style("gap", "8px");

        const checkbox = row.append("input")
            .attr("type", "checkbox")
            .attr("checked", true)
            .attr("id", `filter-${type.replace(/\s+/g, '-')}`)
            .on("change", function () {
                if (this.checked) activeFilters.add(type);
                else activeFilters.delete(type);
                updateVisibility();
            });

        row.append("label")
            .attr("for", `filter-${type.replace(/\s+/g, '-')}`)
            .text(type)
            .style("cursor", "pointer")
            .style("font-size", "14px");
    });

    function updateVisibility() {
        // Determine visible nodes
        const isNodeVisible = (d) => {
            let type = "Unknown";
            if (d.extra_data) {
                if (d.extra_data.role) type = d.extra_data.role;
                else if (d.extra_data.type) type = d.extra_data.type;
                else if (d.extra_data.value) type = "Value";
            } else if (d.group) {
                type = "Group " + d.group;
            }
            return activeFilters.has(type);
        };

        const visibleNodeIds = new Set();

        node.style("display", d => {
            const visible = isNodeVisible(d);
            if (visible) visibleNodeIds.add(d.id);
            return visible ? null : "none";
        });

        // Link is visible ONLY if both source and target are visible
        linkGroup.style("display", d => {
            // d.source/target are objects after simulation starts, or IDs before?
            // Usually objects by the time simulation runs, but this might be called early?
            // Safer to check both.
            const s = d.source.id || d.source; // .id if object, else assume it's the ID
            const t = d.target.id || d.target;
            return (visibleNodeIds.has(s) && visibleNodeIds.has(t)) ? null : "none";
        });
    }

    // Drag Behavior
    function drag(sim) {
        return d3.drag()
            .on("start", (event, d) => {
                if (!event.active) sim.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            })
            .on("drag", (event, d) => {
                d.fx = event.x;
                d.fy = event.y;
            })
            .on("end", (event, d) => {
                if (!event.active) sim.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            });
    }
}

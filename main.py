# PyScript D3 Network Visualizer
# Copyright (C) 2026 Camaris
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# main.py
import js
import json
import traceback
from pyodide.ffi import create_proxy
from examples import (
    get_karate_club,
    get_small_world,
    get_scale_free,
    get_balanced_tree,
    get_random,
    get_school_data,
)

# Graph Builders Map
GRAPH_BUILDERS = {
    "karate": get_karate_club,
    "small_world": get_small_world,
    "scale_free": get_scale_free,
    "tree": get_balanced_tree,
    "random": get_random,
    "school": get_school_data,
}


def render_graph_by_name(graph_name):
    try:
        import networkx as nx

        # 1. Get the Graph object
        builder = GRAPH_BUILDERS.get(graph_name, get_karate_club)
        G = builder()

        # 2. Calculate Centrality Metrics (Safe check for empty graphs)
        if len(G.nodes) > 0:
            try:
                centrality = nx.betweenness_centrality(G)
            except Exception:
                # Fallback for unconnected graphs or errors
                centrality = {n: 0.1 for n in G.nodes()}

            degree = dict(G.degree())
        else:
            centrality = {}
            degree = {}

        # 3. Transform to JSON-compatible format for D3
        nodes = []
        links = []

        # Detect if "club" attribute exists (Karate Club specific)
        has_clubs = any("club" in G.nodes[n] for n in G.nodes())
        club_colors = {"Mr. Hi": "#60a5fa", "Officer": "#f472b6"}

        for node_id in G.nodes():
            node_attrs = G.nodes[node_id]

            # Use pre-defined style if available, otherwise calculate it
            if "extra_style" in node_attrs:
                style = node_attrs["extra_style"]
            else:
                # Basic defaults
                cent_val = centrality.get(node_id, 0)

                # Dynamic attributes
                radius = 6 + (
                    cent_val * 100
                )  # Base 6, grow with importance via betweenness
                if radius > 30:
                    radius = 30  # Max cap

                # Color logic
                if has_clubs:
                    club_name = node_attrs.get("club", "Unknown")
                    color = club_colors.get(club_name, "#a78bfa")
                else:
                    color = "#8b5cf6"

                style = {
                    "radius": radius,
                    "color": color,
                    "text_color": "#f8fafc",
                    "font_size": "12px",
                }

            # Merge any extra_data
            extra_data = node_attrs.get("extra_data", {})
            if "centrality" not in extra_data:
                extra_data["centrality"] = round(centrality.get(node_id, 0), 4)
            if "degree" not in extra_data:
                extra_data["degree"] = degree.get(node_id, 0)

            nodes.append(
                {
                    "id": str(node_id),
                    "group": 1,
                    "extra_style": style,
                    "extra_data": extra_data,
                }
            )

        for u, v in G.edges():
            edge_attrs = G.edges[u, v]
            link = {"source": str(u), "target": str(v), "value": 1}

            # Pass through extra_style for edges if present
            if "extra_style" in edge_attrs:
                link["extra_style"] = edge_attrs["extra_style"]

            links.append(link)

        graph_data = {"nodes": nodes, "links": links}

        # 4. Serialize and Render
        json_str = json.dumps(graph_data)
        js_graph_obj = js.JSON.parse(json_str)
        js.renderGraph(js_graph_obj)

        # Remove loading indicator
        loading = js.document.getElementById("loading-indicator")
        if loading:
            loading.remove()

    except Exception:
        error_msg = traceback.format_exc()
        js.console.error(f"Python Error: {error_msg}")
        js.alert(f"Error rendering graph: {error_msg}")


def on_select_change(event):
    """Event handler for dropdown change."""
    value = event.target.value
    render_graph_by_name(value)


# --- Initialization ---
try:
    # 1. Attach Event Listener
    select_element = js.document.getElementById("exampleSelect")
    # create_proxy is essential for passing Python functions to JS event listeners
    proxy = create_proxy(on_select_change)
    select_element.addEventListener("change", proxy)

    # 2. Render Initial Graph (Default selected value)
    initial_value = select_element.value
    render_graph_by_name(initial_value)

except Exception:
    error_msg = traceback.format_exc()
    js.console.error(f"Init Error: {error_msg}")

    err_div = js.document.createElement("div")
    err_div.style.position = "absolute"
    err_div.style.top = "50%"
    err_div.style.left = "50%"
    err_div.style.transform = "translate(-50%, -50%)"
    err_div.style.background = "rgba(220, 38, 38, 0.9)"  # Red-600
    err_div.style.color = "white"
    err_div.style.padding = "2rem"
    err_div.style.borderRadius = "12px"
    err_div.style.boxShadow = "0 10px 15px -3px rgba(0, 0, 0, 0.5)"
    err_div.style.zIndex = "9999"
    err_div.style.maxWidth = "80vw"
    err_div.style.overflow = "auto"
    err_div.innerHTML = f"<h3>Python Execution Error</h3><pre style='white-space: pre-wrap; font-family: monospace;'>{error_msg}</pre>"
    js.document.body.appendChild(err_div)

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

import networkx as nx


def get_karate_club():
    """Returns the Zachary's Karate Club graph."""
    return nx.karate_club_graph()


def get_small_world():
    """Returns a Watts-Strogatz small-world graph."""
    # n=30 nodes, k=4 nearest neighbors, p=0.1 rewiring probability
    return nx.watts_strogatz_graph(30, 4, 0.1)


def get_scale_free():
    """Returns a Barabasi-Albert preferential attachment graph."""
    # n=40 nodes, m=2 edges to attach from a new node to existing nodes
    return nx.barabasi_albert_graph(40, 2)


def get_balanced_tree():
    """Returns a perfectly balanced binary tree."""
    # r=2 branching factor, h=4 height
    return nx.balanced_tree(2, 4)


def get_random():
    """Returns a random Erdos-Renyi graph."""
    # n=30, p=0.15
    return nx.erdos_renyi_graph(30, 0.15)


def get_school_data():
    """
    Returns a graph representing a School Data Model.
    Nodes: Student, Teacher, Course, Grade.
    Demonstrates various 'extra_style' capabilities.
    """
    G = nx.DiGraph()

    # --- Nodes ---
    # Teachers (Outline style)
    G.add_node(
        "Prof. Snape",
        extra_style={
            "color": "#1f2937",
            "stroke_color": "#ef4444",
            "stroke_width": 3,
            "radius": 28,
            "text_color": "#ef4444",
            "font_size": "14px",
            "font_weight": "bold",
            "text_outline": "#ffffff",  # New: Text Halo
            "glow": True,  # New: Node Glow
            "icon": "fa-solid fa-chalkboard-user",
            "icon_size": "24px",
            "icon_color": "#ef4444",
        },
        extra_data={"role": "Teacher"},
    )
    G.add_node(
        "Prof. McGonagall",
        extra_style={
            "color": "#1f2937",
            "stroke_color": "#ef4444",
            "stroke_width": 3,
            "radius": 28,
            "text_color": "#ef4444",
            "font_size": "14px",
            "font_weight": "bold",
            "text_outline": "#ffffff",  # New: Text Halo
            "glow": True,
            "icon": "fa-solid fa-chalkboard-user",
            "icon_size": "24px",
            "icon_color": "#ef4444",
        },
        extra_data={"role": "Teacher"},
    )

    # Courses (Large, high opacity)
    G.add_node(
        "Potions",
        extra_style={
            "color": "#22c55e",
            "radius": 40,
            "text_color": "#f0fdf4",
            "font_size": "18px",
            "font_weight": "600",
            "text_outline": "#000000",  # New: Text Halo
            "glow": True,
            "icon": "fa-solid fa-flask",
            "icon_size": "32px",
            "icon_color": "#f0fdf4",
        },
        extra_data={"type": "Subject"},
    )
    G.add_node(
        "Transfiguration",
        extra_style={
            "color": "#22c55e",
            "radius": 40,
            "text_color": "#f0fdf4",
            "font_size": "18px",
            "font_weight": "600",
            "text_outline": "#000000",  # New: Text Halo
            "glow": True,
            "icon": "fa-solid fa-wand-magic-sparkles",
            "icon_size": "32px",
            "icon_color": "#f0fdf4",
        },
        extra_data={"type": "Subject"},
    )

    # Students (Standard)
    # Group styling logic can be done in Python easily
    students = [
        ("Harry", "#3b82f6"),
        ("Hermione", "#3b82f6"),
        ("Ron", "#3b82f6"),
        ("Draco", "#10b981"),
    ]
    for name, color in students:
        G.add_node(
            name,
            extra_style={
                "color": color,
                "radius": 18,
                "text_color": "#e2e8f0",
                "icon": "fa-solid fa-user-graduate",
                "icon_size": "14px",
                "icon_color": "#fff",
            },
            extra_data={"role": "Student"},
        )

    # Grades (Small, semi-transparent, DASHED STROKE)
    G.add_node(
        "Grade: O",
        extra_style={
            "color": "#eab308",
            "radius": 12,
            "opacity": 0.9,
            "stroke_color": "#fff",
            "stroke_width": 2,
            "stroke_dash": "3,3",  # New: Dashed Node Border
            "icon": "fa-solid fa-star",
            "icon_size": "10px",
            "icon_color": "#fff",
        },
        extra_data={"value": "Outstanding"},
    )
    G.add_node(
        "Grade: E",
        extra_style={
            "color": "#f59e0b",
            "radius": 12,
            "opacity": 0.9,
            "stroke_color": "#fff",
            "stroke_width": 2,
            "stroke_dash": "3,3",  # New: Dashed Node Border
            "icon": "fa-solid fa-star-half-stroke",
            "icon_size": "10px",
            "icon_color": "#fff",
        },
        extra_data={"value": "Exceeds Expectations"},
    )

    # --- Edges ---
    # Teaches (Thick Red Lines with Labels + ARROWS)
    G.add_edge(
        "Prof. Snape",
        "Potions",
        extra_style={
            "color": "#ef4444",
            "stroke_width": 4,
            "label": "teaches",
            "font_size": "11px",
            "arrow": True,  # New: Arrow
        },
    )
    G.add_edge(
        "Prof. McGonagall",
        "Transfiguration",
        extra_style={
            "color": "#ef4444",
            "stroke_width": 4,
            "label": "teaches",
            "font_size": "11px",
            "arrow": True,  # New: Arrow
        },
    )

    # Enrolled (Normal with opacity + ARROWS)
    G.add_edge(
        "Harry",
        "Potions",
        extra_style={"color": "#60a5fa", "opacity": 0.5, "arrow": True},
    )
    G.add_edge(
        "Harry",
        "Transfiguration",
        extra_style={"color": "#60a5fa", "opacity": 0.5, "arrow": True},
    )
    G.add_edge(
        "Hermione",
        "Potions",
        extra_style={"color": "#60a5fa", "opacity": 0.5, "arrow": True},
    )
    G.add_edge(
        "Hermione",
        "Transfiguration",
        extra_style={"color": "#60a5fa", "opacity": 0.5, "arrow": True},
    )
    G.add_edge(
        "Ron",
        "Transfiguration",
        extra_style={"color": "#60a5fa", "opacity": 0.5, "arrow": True},
    )
    G.add_edge(
        "Draco",
        "Potions",
        extra_style={"color": "#10b981", "opacity": 0.5, "arrow": True},
    )  # Slytherin color link

    # Grades (Dashed Gold Lines with labels + ARROWS)
    G.add_edge(
        "Hermione",
        "Grade: O",
        extra_style={
            "color": "#eab308",
            "dash": "5,5",
            "label": "achieved",
            "arrow": True,
        },
    )
    G.add_edge(
        "Grade: O",
        "Transfiguration",
        extra_style={"color": "#eab308", "dash": "5,5", "label": "in", "arrow": True},
    )

    G.add_edge(
        "Harry",
        "Grade: E",
        extra_style={
            "color": "#f59e0b",
            "dash": "5,5",
            "label": "achieved",
            "arrow": True,
        },
    )
    G.add_edge(
        "Grade: E",
        "Potions",
        extra_style={"color": "#f59e0b", "dash": "5,5", "label": "in", "arrow": True},
    )

    # --- Expanded Data ---

    # Headmaster
    G.add_node(
        "Albus Dumbledore",
        extra_style={
            "color": "#1f2937",
            "stroke_color": "#fbbf24",
            "stroke_width": 4,
            "radius": 35,
            "text_color": "#fbbf24",
            "font_size": "16px",
            "font_weight": "bold",
            "text_outline": "#000",
            "glow": True,
            "icon": "fa-solid fa-hat-wizard",
            "icon_size": "30px",
            "icon_color": "#fbbf24",
        },
        extra_data={"role": "Headmaster"},
    )
    G.add_edge(
        "Albus Dumbledore",
        "Prof. Snape",
        extra_style={"color": "#fbbf24", "arrow": True, "label": "manages"},
    )
    G.add_edge(
        "Albus Dumbledore",
        "Prof. McGonagall",
        extra_style={"color": "#fbbf24", "arrow": True, "label": "manages"},
    )

    # New Subject: Defense Against the Dark Arts
    G.add_node(
        "Defense Against the Dark Arts",
        extra_style={
            "color": "#7f1d1d",
            "radius": 40,
            "text_color": "#fca5a5",
            "font_size": "18px",
            "font_weight": "600",
            "text_outline": "#000",
            "glow": True,
            "icon": "fa-solid fa-shield-halved",
            "icon_size": "32px",
            "icon_color": "#fca5a5",
        },
        extra_data={"type": "Subject"},
    )
    G.add_edge(
        "Prof. Snape",
        "Defense Against the Dark Arts",
        extra_style={"color": "#ef4444", "arrow": True, "label": "covets"},
    )

    # Houses as Hubs
    houses = [
        ("Gryffindor", "#ef4444", "fa-solid fa-fire"),
        ("Slytherin", "#16a34a", "fa-solid fa-snake"),
        ("Ravenclaw", "#3b82f6", "fa-solid fa-crow"),
        ("Hufflepuff", "#eab308", "fa-solid fa-leaf"),
    ]
    for h_name, h_color, h_icon in houses:
        G.add_node(
            h_name,
            extra_style={
                "color": h_color,
                "radius": 25,
                "text_color": h_color,
                "font_weight": "bold",
                "text_outline": "#fff",
                "icon": h_icon,
                "icon_size": "20px",
                "icon_color": "#fff",
            },
            extra_data={"type": "House"},
        )

    # Link Students to Houses
    G.add_edge("Harry", "Gryffindor", extra_style={"color": "#ef4444", "opacity": 0.3})
    G.add_edge(
        "Hermione", "Gryffindor", extra_style={"color": "#ef4444", "opacity": 0.3}
    )
    G.add_edge("Ron", "Gryffindor", extra_style={"color": "#ef4444", "opacity": 0.3})
    G.add_edge("Draco", "Slytherin", extra_style={"color": "#16a34a", "opacity": 0.3})

    # New Student: Luna
    G.add_node(
        "Luna",
        extra_style={
            "color": "#3b82f6",
            "radius": 18,
            "text_color": "#e2e8f0",
            "icon": "fa-solid fa-user-graduate",
            "icon_size": "14px",
            "icon_color": "#fff",
        },
        extra_data={"role": "Student"},
    )
    G.add_edge("Luna", "Ravenclaw", extra_style={"color": "#3b82f6", "opacity": 0.3})
    G.add_edge(
        "Luna",
        "Transfiguration",
        extra_style={"color": "#60a5fa", "opacity": 0.5, "arrow": True},
    )

    return G

import logging
import threading
from flask import Flask
from dash import Dash, dcc, html, Input, Output
from dash.dash_table import DataTable
import plotly.graph_objs as go
import time
import re
import dash_bootstrap_components as dbc


class RealTimeDashboard:
    def __init__(self, logfile_path="path_to_your_logfile.log", port=2234):
        self.logfile_path = logfile_path
        self.port = port
        logging.getLogger("werkzeug").setLevel(logging.ERROR)
        self.cpu_usage_data = []
        self.memory_usage_data = []
        self.logs = []
        self.max_data_points = 100

        self.app = Flask(__name__)
        self.dash_app = Dash(
            __name__,
            server=self.app,
            url_base_pathname="/",
            external_stylesheets=[dbc.themes.BOOTSTRAP],
        )
        self.dash_app.layout = html.Div(
            style={
                "margin": "0",
                "backgroundColor": "#E6F2FF",  # Light blue background
                "color": "#333",
                "fontFamily": "'Segoe UI', Arial, sans-serif",
                "padding": "20px",
            },
            children=[
                html.A(
                    html.Div(
                        "⭐ Star on GitHub",
                        style={
                            "position": "absolute",
                            "top": "10px",
                            "right": "10px",
                            "backgroundColor": "#007bff",
                            "color": "#ffffff",
                            "padding": "5px 10px",
                            "borderRadius": "5px",
                            "textDecoration": "none",
                            "fontSize": "14px",
                        },
                    ),
                    href="https://github.com/SujalChoudhari/TraceBook",
                    target="_blank",
                ),
                html.H1(
                    "TraceBook Real-Time Dashboard",
                    style={
                        "textAlign": "center",
                        "color": "#0056b3",  # Darker blue
                        "marginBottom": "30px",
                        "fontSize": "36px",
                        "fontWeight": "bold",
                    },
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [dbc.CardBody([dcc.Graph(id="cpu-usage-graph")])],
                                    className="mb-4",
                                    style={
                                        "borderRadius": "15px",
                                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                    },
                                ),
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [dcc.Graph(id="memory-usage-graph")]
                                        )
                                    ],
                                    style={
                                        "borderRadius": "15px",
                                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                    },
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    id="log-window",
                                                    style={
                                                        "overflowY": "scroll",
                                                        "height": "800px",
                                                        "backgroundColor": "#FFFFFF",
                                                        "padding": "15px",
                                                        "color": "#333",
                                                        "borderRadius": "10px",
                                                    },
                                                )
                                            ]
                                        )
                                    ],
                                    style={
                                        "borderRadius": "15px",
                                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                    },
                                )
                            ],
                            width=6,
                        ),
                    ]
                ),
                dcc.Interval(id="interval-component", interval=1000, n_intervals=0),
            ],
        )

        self.dash_app.callback(
            [
                Output("cpu-usage-graph", "figure"),
                Output("memory-usage-graph", "figure"),
                Output("log-window", "children"),
            ],
            [Input("interval-component", "n_intervals")],
        )(self.update_graph)

        
        @self.dash_app.server.context_processor
        def inject_auto_scroll_script():
            return dict(
                auto_scroll_script="""
                <script>
                setInterval(function() {
                    var logWindow = document.getElementById('log-window');
                    logWindow.scrollTop = logWindow.scrollHeight;
                }, 1000);
                </script>
                """
            )

    def update_graph(self, n):
        cpu_figure = {
            "data": [
                go.Scatter(
                    x=[timestamp for timestamp, _ in self.cpu_usage_data],
                    y=[usage for _, usage in self.cpu_usage_data],
                    mode="lines",
                    line=dict(color="#007bff", width=3),  # Blue color
                    fill="tozeroy",
                    fillcolor="rgba(0, 123, 255, 0.2)",
                )
            ],
            "layout": go.Layout(
                title="CPU Usage Over Time",
                title_font=dict(color="#0056b3"),
                xaxis={
                    "title": "Time",
                    "title_font": {"color": "#0056b3"},
                    "tickfont": {"color": "#333"},
                    "gridcolor": "#cce5ff",
                },
                yaxis={
                    "title": "CPU Usage (%)",
                    "title_font": {"color": "#0056b3"},
                    "tickfont": {"color": "#333"},
                    "gridcolor": "#cce5ff",
                },
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                height=350,
                margin=dict(l=50, r=20, t=50, b=50),
            ),
        }

        memory_figure = {
            "data": [
                go.Scatter(
                    x=[timestamp for timestamp, _ in self.memory_usage_data],
                    y=[usage for _, usage in self.memory_usage_data],
                    mode="lines",
                    line=dict(color="#007bff", width=3),  # Blue color
                    fill="tozeroy",
                    fillcolor="rgba(0, 123, 255, 0.2)",
                )
            ],
            "layout": go.Layout(
                title="Memory Usage Over Time",
                title_font=dict(color="#0056b3"),
                xaxis={
                    "title": "Time",
                    "title_font": {"color": "#0056b3"},
                    "tickfont": {"color": "#333"},
                    "gridcolor": "#cce5ff",
                },
                yaxis={
                    "title": "Memory Usage (MB)",
                    "title_font": {"color": "#0056b3"},
                    "tickfont": {"color": "#333"},
                    "gridcolor": "#cce5ff",
                },
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                height=350,
                margin=dict(l=50, r=20, t=50, b=50),
            ),
        }

        log_entries = []
        indent = 1
        for log in self.logs[-100:]:
            parts = log.split(" ", 3)
            if len(parts) >= 4:
                info_tag, date, time, rest = parts

                op = rest[0]
                content = rest[2:]

                if op in (">", "<"):
                    func_name, args_kwargs = content.split(" ", 1)
                    if op == ">":
                        indent += 1
                        args, kwargs = args_kwargs.rsplit(" ", 1)
                        log_entry = html.Div(
                            [
                                html.Span(
                                    info_tag,
                                    style={"color": "#007bff", "fontWeight": "bold"},
                                ),
                                # html.Span(f" {date} ", style={"color": "#6c757d"}),
                                html.Span(time, style={"color": "#17a2b8"}),
                                html.Span(
                                    f" {op} ",
                                    style={
                                        "color": "#28a745",
                                        "fontWeight": "bold",
                                        "display": "inline-block",
                                        "padding-left": f"{indent * 20}px",
                                    },
                                ),
                                html.Span(
                                    func_name,
                                    style={"color": "#6610f2", "fontWeight": "bold"},
                                ),
                                html.Span(
                                    f" Args: {args} ", style={"color": "#fd7e14"}
                                ),
                                html.Span(
                                    f" Kwargs: {kwargs}", style={"color": "#e83e8c"}
                                ),
                            ]
                        )
                    else:
                        indent = max(1, indent - 1)
                        log_entry = html.Div(
                            [
                                html.Span(
                                    info_tag,
                                    style={"color": "#007bff", "fontWeight": "bold"},
                                ),
                                # html.Span(f" {date} ", style={"color": "#6c757d"}),
                                html.Span(time, style={"color": "#17a2b8"}),
                                html.Span(
                                    f" {op} ",
                                    style={
                                        "color": "#dc3545",
                                        "fontWeight": "bold",
                                        "display": "inline-block",
                                        "padding-left": f"{indent * 20}px",
                                    },
                                ),
                                html.Span(
                                    func_name,
                                    style={"color": "#6610f2", "fontWeight": "bold"},
                                ),
                                html.Span(
                                    f" Returns: {args_kwargs}",
                                    style={"color": "#20c997"},
                                ),
                            ]
                        )
                elif op == "*":
                    cpu, mem = content.split(" ", 1)
                    log_entry = html.Div(
                        [
                            html.Span(
                                info_tag,
                                style={"color": "#007bff", "fontWeight": "bold"},
                            ),
                            # html.Span(f" {date} ", style={"color": "#6c757d"}),
                            html.Span(time, style={"color": "#17a2b8"}),
                            html.Span(
                                f" {op} ",
                                style={
                                    "color": "#ffc107",
                                    "fontWeight": "bold",
                                    "display": "inline-block",
                                    "padding-left": f"{indent * 20}px",
                                },
                            ),
                            html.Span(cpu, style={"color": "#d63384"}),
                            html.Span(f" {mem}", style={"color": "#0dcaf0"}),
                        ]
                    )
                else:
                    log_entry = html.Div(
                        [
                            html.Span(
                                info_tag,
                                style={"color": "#007bff", "fontWeight": "bold"},
                            ),
                            html.Span(f" {date} ", style={"color": "#6c757d"}),
                            html.Span(time, style={"color": "#17a2b8"}),
                            html.Span(f" {content}", style={"color": "#333"}),
                        ],
                        style={"margin": "0", "padding-left": f"{indent * 20}px"},
                    )

                log_entries.append(log_entry)
            else:
                log_entries.append(html.Div(log, style={"color": "#333"}))

        return cpu_figure, memory_figure, log_entries

    def log_watcher(self):
        with open(self.logfile_path, "r") as f:
            f.seek(0, 2)  # Move the cursor to the end of the file
            while True:
                line = f.readline()
                if line:
                    self.logs.append(line.strip())
                    self.parse_log_line(line.strip())
                time.sleep(1)

    def parse_log_line(self, line):
        # Example log line: [INFO] 2024-08-13 14:21:50 * 7.40% 47.04 MB
        match = re.match(
            r"\[INFO\] (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \* (\d+\.\d+)% (\d+\.\d+) MB",
            line,
        )
        if match:
            timestamp_str, cpu_usage, memory_usage = match.groups()
            timestamp = time.mktime(time.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"))
            self.cpu_usage_data.append((timestamp, float(cpu_usage)))
            self.memory_usage_data.append((timestamp, float(memory_usage)))

            # Keep only the most recent data points
            if len(self.cpu_usage_data) > self.max_data_points:
                self.cpu_usage_data = self.cpu_usage_data[-self.max_data_points :]
            if len(self.memory_usage_data) > self.max_data_points:
                self.memory_usage_data = self.memory_usage_data[-self.max_data_points :]

    def start_server(self):
        self.app.run(host="localhost", port=self.port, use_reloader=False)

    def run(self):
        # Start log watcher thread
        thread = threading.Thread(target=self.log_watcher, daemon=True)
        thread.start()

        # Start the Flask server in a separate thread
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()

        # You can add any other code here that needs to run concurrently
        print(
            f"Dashboard is running in the background at http://localhost:{self.port}."
        )


# Usage:
if __name__ == "__main__":
    dashboard = RealTimeDashboard(logfile_path="path_to_your_logfile.log", port=2234)
    dashboard.run()

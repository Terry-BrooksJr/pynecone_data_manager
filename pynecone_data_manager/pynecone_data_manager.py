"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

import pynecone as pc

from pynecone_data_manager.state import State

from .pages.create_connection import CreateConnection
from .pages.dashboard import Dashboard

# Add state and page to the app.
app = pc.App(state=State)
app.add_page(route="/dashboard", component=Dashboard, title="Dashboard")
app.add_page(route="/", component=Dashboard, on_load=pc.redirect("/dashboard"))

app.add_page(route="/create", component=CreateConnection)

app.compile()

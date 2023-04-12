import pynecone as pc
import .state
from ..webhook.task_producer import msg_share


def CreateConnection():
    return pc.center(
        pc.box(
            pc.vstack(
                pc.image(
                    src="https://assets.codepen.io/6554302/chooch-logo.png",
                    width="50px",
                    float="left",
                    margin_right="15px",
                ),
                pc.heading(
                    "Chooch Data Exportation Manager - Add New Connection",
                    font_size="1.5em",
                ),
                pc.center(
                    pc.vstack(
                        pc.hstack(
                            pc.link(
                                pc.button("Back to Dashboard"),
                                button=True,
                                href="/",
                                width="100%",
                            ),
                        ),
                    ),
                ),
            ),
            pc.hstack(
                pc.text("Connection Name"),
                pc.input(
                    placeholder="Name of Connection",
                    on_blur=state.ConnectionState.save_connection_name,
                ),
            ),
            pc.hstack(
                pc.text("Webhook URL"),
                pc.input(
                    placeholder="http://<HOST>:<PORT>",
                    on_blur=state.ConnectionState.save_url,
                ),
            ),
            pc.hstack(
                pc.text("Description of Connection"),
                pc.text_area(
                    placeholder="http://<HOST>:<PORT>",
                    on_blur=state.ConnectionState.save_description,
                ),
                margin_bottom="15px",
            ),
            pc.divider(margin_bottom="15px"),
            pc.center(
                pc.hstack(
                    pc.link(
                        pc.button("Save Connection"),
                        button=True,
                        on_click=state.ConnectionState.create_destination(),
                        width="100%",
                        margin_right="13.2em",
                        background_color="green",
                    ),
                    pc.link(
                        pc.button("Cancel"),
                        button=True,
                        href="/",
                        width="100%",
                        background_color="red",
                    ),
                ),
            ),
        )
    )

"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

import pendulum
import pynecone as pc

from pynecone_data_manager.state import AlertDialogState

now = pendulum.now()


def Dashboard():
    return pc.center(
        pc.box(
            pc.vstack(
                pc.hstack(
                    pc.image(
                        src="https://assets.codepen.io/6554302/chooch-logo.png",
                        width="50px",
                        float="left",
                        margin_right="15px",
                    ),
                    pc.heading("Chooch Data Exportation Manager", size="2xl"),
                ),
                pc.hstack(
                    pc.link(
                        pc.button(
                            pc.icon(tag="add"), "Create New Connection", margin="1.5em"
                        ),
                        button=True,
                        href="/create",
                        width="50%",
                    ),
                    pc.center(
                        pc.divider(orientation="vertical", border_color="gray"),
                        height="2em",
                    ),
                    pc.link(
                        pc.button("Check Dead Letter Queue"),
                        button=True,
                        href="/create",
                        width="50%",
                    ),
                    pc.center(
                        pc.divider(orientation="vertical", border_color="gray"),
                        height="2em",
                    ),
                    pc.link(
                        pc.button("Review Transmission Logs"),
                        button=True,
                        href="/create",
                        width="50%",
                    ),
                ),
                margin_bottom="10px",
            ),
            pc.divider(),
            pc.table_container(
                pc.table(
                    headers=[
                        "ID",
                        "Name",
                        "Description",
                        "Status",
                        "URL",
                        "Created",
                        "Modify",
                        "Actions",
                    ],
                    rows=[
                        (
                            "Kafka",
                            "Going to Azure",
                            "Active",
                            "http://usernamer:password@example.com",
                            "2021-01-01",
                            "2021-01-01",
                            pc.button(
                                "Edit",
                                width="100%",
                                color="secondary",
                                border="1px solid yellow",
                                background_color="yellow",
                                padding_left="1.5em",
                                padding_right="1.5em",
                                text_align="center",
                            ),
                            pc.button(
                                "Delete",
                                width="100%",
                                color="secondary",
                                border="1px solid red",
                                background_color="red",
                                padding_left="1.5em",
                                padding_right="1.5em",
                                text_align="center",
                                on_click=AlertDialogState.change,
                            ),
                        ),
                    ],
                    variant="striped",
                ),
                pc.divider(),
                pc.table(
                    headers=[
                        "Transmission ID",
                        "Tranmisssion Date",
                        "Transmission Time",
                        "Transmission Status",
                    ],
                    rows=[("1", "foo", "bar", "Success")],
                    variant="striped",
                ),
            ),
        )
    )
    # pc.box(
    #         pc.alert_dialog(
    #             pc.alert_dialog_overlay(
    #                 pc.alert_dialog_content(
    #                     pc.alert_dialog_header("Confirmation of Connection Deletion"),
    #                     pc.alert_dialog_body(
    #                         "Please Confirm You Would Like to Delete This Connection. This Action Cannot Be Undone."
    #                     ),
    #                     pc.alert_dialog_footer(
    #                         pc.button(
    #                             "Close",
    #                             on_click=AlertDialogState.change,
    #                             margin_right="3em",
    #                         ),
    #                         pc.button(
    #                             "Confirm Deletion",
    #                             on_click=State.delete_destination(),
    #                             border="1px solid red",
    #                             background_color="red",
    #                         ),
    #                     ),
    #                 )
    #             ),
    #             is_open=AlertDialogState.show,
    #         )
    # )

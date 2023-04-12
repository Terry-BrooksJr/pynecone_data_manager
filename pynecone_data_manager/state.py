import json
import uuid

import pendulum
import pynecone as pc
import requests

now = pendulum.now()


class Transmission(pc.Model, table=True):
    message_id: int
    date: str
    time: str
    alert_id: str
    successful: bool


class Destination(pc.Model, table=True):
    name: str = ""
    unique = True
    desc: str
    active: bool = True
    url: str
    unique = True
    created: str
    modified: str

    def active_status(self):
        if self.active:
            return "Active"
        else:
            return "Inactive"


class State(pc.State):
    """The app state."""

    show: bool = False
    id

    def change(self):
        self.show = not (self.show)

    active: bool = True
    is_checked = True

    def pause_connection(self, active):
        self.active = active
        if self.active:
            self.is_checked = "Switch on!"
        else:
            self.is_checked = "Switch off!"

    def get_current(self) -> list:
        with pc.session as session:
            self.destinations = [dest for dest in session.query(Destination)]
            return self.destinations

    def get_all_transmission_records(self):
        pass
        with pc.session() as session:
            self.records = [record for record in session.query(Transmission)]
            return self.records

    def delete_destination(self, id):
        with pc.session() as session:
            session.query(Destination).filter_by(id=id).delete()
            session.commit()

    # def show_connection_on_list(self):
    #     return pc.list_item(
    #         pc.hstack(
    #                         self.dest_id,
    #                         "Going to Azure",
    #                         "Active",
    #                         "http://usernamer:password@example.com",
    #                         "2021-01-01",
    #                         "2021-01-01",
    #                         pc.button(
    #                             "Edit",
    #                             width="100%",
    #                             color="secondary",
    #                             border="1px solid yellow",
    #                             background_color="yellow",
    #                             padding_left="1.5em",
    #                             padding_right="1.5em",
    #                             text_align="center",
    #                         ),
    #                         pc.button(
    #                             "Delete",
    #                             width="100%",
    #                             color="secondary",
    #                             border="1px solid red",
    #                             background_color="red",
    #                             padding_left="1.5em",
    #                             padding_right="1.5em",
    #                             text_align="center",
    #                             on_click=AlertDialogState.change,)
    #         )
    #     )


class AlertDialogState(State):
    alert_show: bool = False

    def change(self):
        self.show = not (self.show)


class ConnectionState(State):
    new_connection_url: str = "Webhook URL"
    new_connection_name: str = "Name of Connection"
    new_connection_desc: str = "Description of Connection"

    def save_url(self, text):
        self.new_connection_url = text

    def save_connection_name(self, text):
        self.new_connection_name = text

    def save_description(self, text):
        self.new_connection_desc = text

    def get_all_destinantions_history(self):
        with pc.session() as session:
            return session.query(Destination).all()

    def create_destination(self) -> None:
        with pc.session() as session:
            session.add(
                Destination(
                    name=self.new_connection_name,
                    desc=self.new_connection_desc,
                    active=True,
                    url=self.new_connection_url,
                    created=now.to_date_string(),
                )
            )
            session.commit()

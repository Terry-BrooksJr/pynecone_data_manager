import logging
import sys
import uuid
from enum import Enum
from threading import Thread

import pendulum
import pynecone as pc
from validators import url as URLVaildator
from validators.utils import ValidationFailure

from pynecone_data_manager.webhook.task_producer import msg_share

# SECTION -  Logging Configurations
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename="error.log",
    filemode="w",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)

file_handler = logging.FileHandler("logs/runtime_logs.log")
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
#!SECTION = Logging Configurations

now = pendulum.now()


class Transmission(pc.Model, table=True):
    message_id: int
    date: str
    time: str
    alert_id: str
    successful: bool


class Destination(pc.Model, table=True):
    id = str
    name: str = ""
    desc: str
    active: bool = True
    url: str
    unique = True
    created: str
    modified: str = ""

    def active_status(self):
        if self.active:
            return "Active"
        else:
            return "Inactive"


class DeadLetter(pc.Model, table=True):
    id: int
    inital_tranmission_date: str
    inital_tranmission_time: str
    transmission_id: int


class State(pc.State):
    """The app state."""

    show: bool = False

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
    """State Related to the Connection Destinations URLs."""

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
        logger.debug(
            f"ConnectionState Create Destination Called for {self.new_connection_name}"
        )
        try:
            with pc.session() as session:
                session.add(
                    Destination(
                        name="",
                        active="",
                        state = "",
                        url="",
                        created="",
                    )
                )
                session.commit()
            pc.window_alert(f"Connection {self.new_connection_name} has been added.")
            msg_share(self.new_connection_url)
            return pc.redirect("/dashboard")
        except Exception as e:
            logger.error(str(e))
            return pc.window_alert(
                f"Connection {self.new_connection_name} could not be added."
            )


class DeadLetterQueue(State):
    """State Related to Adding Failures to the Dead Letter Queue."""

    def log_dead_letter(
        self, inital_tranmission_date, inital_tranmission_time, transmission_id
    ) -> None:
        logger.debug("Logging Failed Transmission to Dead Letter Queue")
        try:
            with pc.session() as session:
                session.add(
                    DeadLetter(
                        id=uuid.uuid4(),
                        inital_tranmission_date=inital_tranmission_date,
                        inital_tranmission_time=inital_tranmission_time,
                        transmission_id=transmission_id,
                    )
                )
                session.commit()
        except Exception as e:
            logger.error(str(e))


class ConnectionStates(Enum):
    CREATED = "Connection has been created, but data transmission to the URL has not been initiated."
    TRANSMITTING = "Connection is currently tranmitting data"
    PAUSED = "All Transmission Have Been Temporarily Stopped. Transmit must be re-initialized."
    BLOCKED = "Connection Configurations contain a critical error. Please modify Connection Properties. Connection Cannot Start In THIS STATE."
    DELETED = "Terminal End State. Connection has been deleted, cannot be re-started."

    def __repr__(self) -> str:
        return super().__repr__()

    def __str__(self) -> str:
        return super().__str__()


class Connnection():
    def __new__(cls):
        return super(Connnection, cls).__new__(cls)

    def __init__(self, name, connection_url):
        self._id = uuid.uuid4()
        self._created = now.to_datetime_string()
        self._active = True
        self._state = ConnectionStates.CREATED

    def __str__(self) -> str:
        return f"Connection {self.name} - {self.created} (self.connection_url)"
    
    def __repr__(self) -> str:
        return f"Connection({self.name},{self.connection_url},{self.created})"

    @property
    def name(self) -> str:
        return self._name


    @name.setter
    def set_connection_name(self, name: str) -> None:
        name = str(name.lower().strip())
        if len(name) >= 3:
            if name.isascii():
                self._name = name
            else:
                raise ValueError(
                    "Connection Name Must be Comprised of  ACSCII Characters Only"
                )
        else:
            raise ValueError("Connection Names Must be 3 Characters or More")

    @property
    def connection_url(self) -> str:
        return self._connection_url

    @connection_url.setter
    def set_connection_url(self, connection_string: str) -> None:
        connection_string = str(connection_string.strip())
        try:
            if URLVaildator(connection_string):
                logger.info(f"URL Updated for {self._id} - {connection_string}")
                self._connection_url = connection_string
        except ValidationFailure:
            logger.error(f"Failed URL Update: {connection_string} - MALFORMED")
            raise ValueError("URL is Malformed. Please Confirm URL") from None
        except Exception as e:
            logger.error(f"Failed URL Update: {connection_string} - {str(e)}")
            raise ValueError(str(e)) from None


        def record_connection(self):
            '''Method to record the connection to the database.'''
            try:
                ConnectionState.create_destination(
                    id = self._id,
                    name = self._name,
                    active = self._active,
                    state = self._state,
                    created = self._created
            )
                logger.info(f"Connection {self._name} has been recorded.")
            except Exception as e:
                logger.error(f"Failed to Record Connection: {str(e)}")
                raise RuntimeError(f'Unable to Record Connection - {str(e)}') from None
            
        def transmit(self) -> None:
            '''Initation Method to begin the transmission or the connection to the URL Endpoint'''
            tranmission_thread = Thread(target=msg_share, args=[self._connection_url], isDaemon=True, native_id=909090)
            logger.debug('Created Tranmission Thread')
            try:
                tranmission_thread.start()
            except RuntimeError:
                tranmission_thread.run()
            except Exception as e:
                logger.error(f"Unable top start Transmission Thread - {str(e)}")
                
            try:
                if tranmission_thread.isalive():
                    logger.info(f"Connection {self._name} has been initiated.")
                    self._state = ConnectionStates.TRANSMITTING

            except Exception as e:
                logger.error(f"Failed to Initiate Connection: {str(e)}")
                raise RuntimeError(f'Unable to Initiate Connection - {str(e)}') from None

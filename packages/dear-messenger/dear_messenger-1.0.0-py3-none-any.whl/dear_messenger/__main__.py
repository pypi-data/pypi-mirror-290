import time
from random import random

# For getting the interfaces and let the user select one
from socket import AF_INET, AF_INET6
from psutil import net_if_addrs

import dearpygui.dearpygui as dpg
import grpc_messenger

class Application(grpc_messenger.ViewUpdate):
    def __init__(self, address: str | None = None) -> None:
        self._start_with_address = address is not None
        self._address: str
        if address is not None:
            self._address = address
        self.current_connection: str | None = None
        # Current connection Viewed
        self._backend: grpc_messenger.BackendI

        self._changed_address: bool = address is not None

        self.main()

    def _themes(self):
        with dpg.theme(tag="connection_button_green"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 240, 120))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (40, 120, 80))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (35, 140, 70))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 50)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))
            with dpg.theme_component(dpg.mvButton, enabled_state=False):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 240, 120))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (60, 240, 120))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (60, 240, 120))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))

        with dpg.theme(tag="connection_button_blue"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 120, 240))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (40, 80, 120))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (35, 70, 140))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))

        with dpg.theme(tag="connection_button_yellow"):
            with dpg.theme_component(dpg.mvButton, enabled_state=False):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 220, 90))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 220, 90))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 220, 90))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))

        with dpg.theme(tag="connection_button_red"):
            with dpg.theme_component(dpg.mvButton, enabled_state=False):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 0, 0))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 50)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))

    def main(self) -> None:
        dpg.create_context()
        dpg.create_viewport(title='Custom Title', width=600, height=600, min_width=600)

        dpg.add_stage(tag="stage")

        self._themes()

        with dpg.window(label="New connection", tag="new_connection", modal=True, show=False):
            def callback():
                connection = dpg.get_value("connection")
                dpg.set_value("connection", "")
                dpg.hide_item("new_connection")
                self._backend.connect(connection)
            dpg.add_input_text(hint="Connection: '[::1]:50051' (self)", tag="connection", width=-1, on_enter=True, callback=callback)
            dpg.add_button(label="Save", callback=callback)

        with dpg.window(tag="main"):
            dpg.add_button(tag="title", width=-1, height=30, callback=lambda: dpg.set_clipboard_text(self._address))
            dpg.bind_item_theme(dpg.last_item(), "connection_button_blue")
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text("Copy address to clipboard")
            with dpg.group(horizontal=True):
                with dpg.group(width=300):
                    dpg.add_button(label="Add connection", height=30, width=-1, callback=lambda: dpg.show_item("new_connection"))
                    dpg.bind_item_theme(dpg.last_item(), "connection_button_green")
                    dpg.add_child_window(tag="connections")
                with dpg.group(tag="messages_view"):
                    def callback():
                        if self.current_connection is None:
                            return
                        message = dpg.get_value("message")
                        dpg.set_value("message", "")
                        self._backend.send_message(self.current_connection, message)
                        with dpg.table_row(parent=self.current_connection):
                            dpg.add_text("<--")
                            dpg.add_text(time.strftime("%H:%M", time.localtime()))
                            dpg.add_text(message, wrap=0)
                    dpg.add_input_text(hint="Message", tag="message", width=-1, on_enter=True, callback=callback)

        self.interface_selector()

        if self._start_with_address:
            dpg.set_item_label("title", self._address)
            dpg.show_item("main")
            dpg.set_primary_window("main", True)
            dpg.hide_item("interfaces")

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_viewport_resizable(True)
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            if not self._changed_address:
                continue
            with grpc_messenger.Backend(self._address, self) as b:
                if b is None: # Failed to initialize server
                    dpg.show_item("interfaces")
                    dpg.set_primary_window("interfaces", True) # Select another interface
                    dpg.hide_item("main")
                    self._changed_address = False
                    continue
                dpg.hide_item("interfaces")
                self._backend = b
                while dpg.is_dearpygui_running():
                    dpg.render_dearpygui_frame()
                    self._backend.render()
        dpg.destroy_context()

    def interface_selector(self):
        def select_interface(s, a, address):
            self._address = address+":"+str(dpg.get_value("port"))
            dpg.show_item("main")
            dpg.set_primary_window("main", True)
            dpg.set_item_label("title", self._address.center(48)) # type: ignore
            self._changed_address = True

        interfaces = net_if_addrs()
        ipv6: list[tuple[str, str]] = []
        ipv4: list[tuple[str, str]] = []
        for name, addresses in interfaces.items():
            for address in addresses:
                if address.family is AF_INET:
                    ipv4.append((name, address.address))
                    continue
                if address.family is AF_INET6:
                    ipv6.append((name, address.address))
                    continue
        dpg.hide_item("main")
        with dpg.window(tag="interfaces"):
            dpg.add_input_int(label="port", tag="port", default_value=50051, min_value=49152, min_clamped=True, max_value=65535, max_clamped=True, width=-50)
            with dpg.collapsing_header(label="IPV6", default_open=True):
                for name, address in ipv6:
                    address = "["+address+"]"
                    dpg.add_button(label=f"{name.center(30)}-{address.center(42)}", callback=select_interface, user_data=address, width=-1)
                    dpg.bind_item_theme(dpg.last_item(), "connection_button_blue")
            with dpg.collapsing_header(label="IPV4", default_open=True):
                for name, address in ipv4:
                    dpg.add_button(label=f"{name.center(30)}-{address.center(42)}", callback=select_interface, user_data=address, width=-1)
                    dpg.bind_item_theme(dpg.last_item(), "connection_button_blue")
        dpg.set_primary_window("interfaces", True)

#
    def connecting(self, connection: str) -> None:
        with dpg.group(horizontal=True, parent="connections", tag=f"pending_{connection}"):
            dpg.add_loading_indicator(style=1, height=50)
            dpg.add_button(label=connection, height=50, width=-1, enabled=False)
            dpg.bind_item_theme(dpg.last_item(), "connection_button_yellow")
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text(f"Connecting with: {connection}")

#
    def connected(self, connection: str) -> None:
        dpg.delete_item(f"pending_{connection}")
        with dpg.table(tag=connection, parent="stage", policy=dpg.mvTable_SizingFixedFit, row_background=True, header_row=False, no_host_extendY=True, height=-1, scrollY=True):
            dpg.add_table_column(init_width_or_weight=20)
            dpg.add_table_column(init_width_or_weight=35)
            dpg.add_table_column(width_stretch=True)
        with dpg.group(tag=f"contact_{connection}", parent="connections", horizontal=True):
            dpg.add_button(label="0", tag=f"contact_{connection}.count", enabled=False, width=30, height=30)
            dpg.bind_item_theme(dpg.last_item(), "connection_button_red")
            dpg.add_button(label=connection, tag=f"contact_{connection}.button", callback=self.change_messages_view, user_data=connection, height=50, width=-1)
            dpg.bind_item_theme(dpg.last_item(), "connection_button_blue")
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text(connection)

#
    def failed(self, connection: str) -> None:
        dpg.delete_item(f"pending_{connection}")

#
    def new_message(self, connection: str, message: str) -> None:
        with dpg.table_row(parent=connection):
            dpg.add_text("-->")
            dpg.add_text(time.strftime("%H:%M", time.localtime()))
            dpg.add_text(message, wrap=0)
        if connection != self.current_connection:
            dpg.set_item_label(f"contact_{connection}.count", str(int(dpg.get_item_label(f"contact_{connection}.count")) + 1)) # type: ignore

#
    def disconnected(self, connection: str) -> None:
        dpg.delete_item(connection)
        dpg.delete_item(f"contact_{connection}")
        if connection == self.current_connection:
            self.current_connection = None

#
    def change_messages_view(self, s, __, connection: str):
        if self.current_connection is not None:
            dpg.move_item(self.current_connection, parent="stage")
            dpg.bind_item_theme(f"contact_{self.current_connection}.button", "connection_button_blue")
            dpg.enable_item(f"contact_{self.current_connection}.button")
        self.current_connection = connection
        dpg.disable_item(s)
        dpg.set_item_label(f"contact_{connection}.count", "0")
        dpg.bind_item_theme(f"contact_{self.current_connection}.button", "connection_button_green")
        dpg.move_item(self.current_connection, parent="messages_view")

def main():
    Application()

if __name__ == "__main__":
    main()
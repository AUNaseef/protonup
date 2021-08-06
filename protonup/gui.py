"""ProtonUp GUI"""
import dearpygui.dearpygui as dpg
import dearpygui.themes

from .api import install_directory, installed_versions
from .api import get_proton, remove_proton, fetch_releases


class ProtonUpGUI:

    def __init__(self):
        with dpg.window(label='ProtonUp') as main_window:
            dpg.add_text('Install directory:')
            self.combo_install_directory = dpg.add_combo(items=[], width=344)

            dpg.add_text('Installed versions:')
            self.listbox_installed_versions = dpg.add_listbox(width=344, num_items=7)

            self.btn_add_version = dpg.add_button(label='Add version', callback=self.show_install_proton_window)
            dpg.add_same_line()
            def remove_selected():
                sel = dpg.get_value(self.listbox_installed_versions)
                remove_proton(sel.replace('Proton-', ''))
                self.update_info()
            self.btn_remove_selected = dpg.add_button(label='Remove selected', callback=remove_selected)

            dpg.add_same_line(spacing=95)
            dpg.add_button(label='Close', callback=dpg.stop_dearpygui)

        self.update_info()
        
        dpg.set_primary_window(main_window, True)
        
        dpg.set_item_theme(main_window, dearpygui.themes.create_theme_imgui_dark())

        vp = dpg.create_viewport(title='ProtonUp - Proton-GE Installer', resizable=False, width=360, height=240)
        dpg.setup_dearpygui(viewport=vp)
        dpg.show_viewport(vp)
        dpg.start_dearpygui()
    
    def show_install_proton_window(self):
        with dpg.window(label='Install Proton', width=344, height=224, pos=[8,8], no_resize=True, no_collapse=True, no_move=True) as install_proton_window:
            dpg.set_item_theme(install_proton_window, dearpygui.themes.create_theme_imgui_dark())
            listbox_releases = dpg.add_listbox(width=328, num_items=9)
            dpg.configure_item(listbox_releases, items=fetch_releases())
            def install_selected():
                ver = dpg.get_value(listbox_releases)
                dpg.delete_item(btn_install)
                dpg.delete_item(btn_close)
                dpg.configure_item(install_proton_window, no_close=True)
                dpg.configure_item(listbox_releases, items=['Installing Proton-' + ver, 'This may take a while, please wait...', '', 'You may need to restart the Steam client.'])
                get_proton(ver)
                self.update_info()
                dpg.delete_item(install_proton_window)
            btn_install = dpg.add_button(label='Install', callback=install_selected)
            dpg.add_same_line()
            btn_close = dpg.add_button(label='Close', callback=lambda: dpg.delete_item(install_proton_window))
    
    def update_info(self):
        dpg.configure_item(self.combo_install_directory, default_value=install_directory())
        dpg.configure_item(self.listbox_installed_versions, items=installed_versions())

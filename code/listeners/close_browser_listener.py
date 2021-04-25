from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary.errors import NoOpenBrowser

ROBOT_LISTENER_API_VERSION = 2

# def close_browsers_all():
#     try:
#         BuiltIn().import_library('SeleniumLibrary')
#         selenium = BuiltIn().get_library_instance('SeleniumLibrary')
#         selenium.close_all_browsers()
#     except NoOpenBrowser:
#         pass

# def close_current_browser():
#     try:
#         selenium = BuiltIn().get_library_instance('SeleniumLibrary')
#         selenium.close_browser()
#     except NoOpenBrowser:
#         pass

def start_keyword(name, attributes):
    if(attributes['kwname'] == "Login"):
        try:
            expectedBrowser = BuiltIn().get_variable_value("${browser}")
            selenium = BuiltIn().get_library_instance('SeleniumLibrary')
            currentBrowser = selenium.driver.capabilities['browserName']
            if (currentBrowser != expectedBrowser):
                close_current_browser()
        except NoOpenBrowser:
            # execfile('choose_launch.py')
            pass

# def end_suite(name, attributes):
#     if (attributes['id'] == "s1"):
#         close_browsers_all()
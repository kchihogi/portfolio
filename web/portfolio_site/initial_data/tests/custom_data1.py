"""This module deletes and inserts test data into the DB.

You might execute master_data.py first.
"""
from initial_data import custom_data_utils,master_data

master_data.add_icon_master()
custom_data_utils.add_profile()
custom_data_utils.add_acknowledgment()
custom_data_utils.add_language_skills()
custom_data_utils.add_library_skills()
custom_data_utils.add_dev_ops_skills()
custom_data_utils.add_works()

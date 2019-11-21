#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Snips-Assistant-Basic
    Copyright (C) 2019  DANBER

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import configparser
import io
import json
import os
import random

import toml
from hermes_python.hermes import Hermes
from hermes_python.ontology import MqttOptions

# ======================================================================================================================

file_path = os.path.dirname(os.path.realpath(__file__)) + "/"
toml_path = "/etc/snips.toml"

if (os.path.exists(toml_path)):
    snips_toml = toml.load(toml_path)
else:
    snips_toml = None


# ======================================================================================================================

class Assistant:
    def __init__(self):
        self.hermes = create_hermes()
        self.conf = None
        self.talks = None

        self.load_config()
        self.load_talks()

    def load_config(self):
        self.conf = read_configuration_file()

    def load_talks(self):
        path = file_path + "talks/" + self.conf["secret"]["language"].lower() + ".json"
        self.talks = read_json_file(path)

    def get_config(self):
        return self.conf

    def get_talks(self):
        return self.talks

    def get_text(self, key):
        return random.choice(self.talks[key])

    def get_hermes(self):
        return self.hermes


# ======================================================================================================================

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name: option for option_name, option in self.items(section)}
                for section in self.sections()}


# ======================================================================================================================

def read_configuration_file():
    try:
        with io.open(file_path + "config.ini", encoding="utf-8") as f:
            conf_parser = SnipsConfigParser()
            conf_parser.read_file(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        print("ConfigParserReadError:", e)
        return dict()


# ======================================================================================================================

def write_configuration_file(conf):
    try:
        with io.open(file_path + "config.ini", 'w', encoding="utf-8") as f:
            conf.write(f)
    except (IOError, configparser.Error) as e:
        print("ConfigParserWriteError:", e)


# ======================================================================================================================

def create_hermes():
    """ Create instance of hermes with mqtt options from snips toml file """

    broker_address = "localhost:1883"
    username = None
    password = None

    if (snips_toml is not None):
        if ("mqtt" in snips_toml["snips-common"].keys()):
            broker_address = snips_toml["snips-common"]["mqtt"]
        if ("mqtt_username" in snips_toml["snips-common"].keys()):
            username = snips_toml["snips-common"]["mqtt_username"]
        if ("mqtt_password" in snips_toml["snips-common"].keys()):
            password = snips_toml["snips-common"]["mqtt_password"]

    mqtt_opts = MqttOptions(username=username, password=password, broker_address=broker_address)
    hermes = Hermes(mqtt_options=mqtt_opts)
    return hermes


# ======================================================================================================================

def read_json_file(path):
    if (os.path.exists(path)):
        with open(path, encoding="utf-8") as file:
            content = json.load(file)
        return content
    else:
        return None


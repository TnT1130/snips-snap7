#! /usr/bin/env bash

# Copy config.ini.default if it exists and config.ini doesn't exist.
if [ -e config.ini.default ] && [ ! -e config.ini ]; then
    cp config.ini.default config.ini
    chmod a+w config.ini
fi

# Create or activate virtual environment
VENV=venv
if [ ! -d "$VENV" ]; then
  PYTHON=$(which python3)

  if [ ! -f $PYTHON ]; then
    echo "could not find python"
  fi
  virtualenv -p $PYTHON $VENV
fi
. $VENV/bin/activate

# Update pip
pip install --upgrade pip

# Install python requirements
pip3 install -r requirements.txt

#install snap7 libarys
./install_snap7.sh

# Download assistant.py
#curl https://gitlab.com/snippets/1893789/raw --silent --output assistant.py

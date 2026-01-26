# Untitled Monitor Assistant

![dashboard example](example.png)


A helpful dashboard.

Running on a Raspberry Pi 5 connected to a television in my home, this displays tasks/groceries from my Todoist account and updcoming events from Google calendar. Both Todoist and Google have their own classes/files which I use in `aggregator.py` to compile everything and add additional formatting. The information is updated and saved to `/site/state.json` every few minutes. There, it can be accessed by my webpage which polls every few seconds. To get this page on a local browser I am simply using python's default `http.server` functionality to serve the entire `/site/` directory. Gotta love the simplicity of not using node/some other backend/a package manager.

## Kiosk Rant

Actually running web kiosks on a device always requires more headache than one would think. Service files can be made to run on boot for the aggregator program, the python server, and running the instance of chrome/chromium. However, to get around the keyring for chrome it has to be run as the user, not root. A pretty easy way to get around this is to have a shell script that runs chrome and then have the service run the script.

Then there's hiding the mouse. On Raspberry Pi 4 and earlier the window manager was X11 so you could add one line to `/etc/lightdm/lightdm.conf` and have the mouse disappear. On RPi 5/Raspberry Pi OS you get Wayland/labwc which is not as simple. You can switch back to X11 in `raspi-config` and I certainly tried but it was never stable enough to work for more than 10 minutes. What you *can* do with this newer hardware/software that I was never able to do before is solve the problem with css. Simply adding `  cursor: none;` to the html or body of your stylesheet does actually hide the cursor with this setup. Previously, this line only worked if you interacted with the mouse after the page had loaded, something that would be quite annoying if you had to do it every time your display turned on.

## Installation & Setup

This is a pretty specific project but just in case you wanted it or something like it, this is how I did it:

1. In the project folder, create a virtual environment with `python -m venv venv`. Then activate it (on linux/Mac) with `source venv/bin/activate` 
2. You will need access to whichever APIs you intend to use. I had to create a todoist developer account, create an app, and put the key in a local `.env` file. I also had to make an app for Google calendar and create a `credentials.json` file to contain their OAuth stuff. Both of the programs I created for these APIs in this repository handle caching and refreshing tokens for continuous use but it does still require you be redirected to a specific URI at least once. This might sound like a lot but in truth it takes less than half an hour to set up.
3. Once your API clients gather the information you want, make sure they are added to the `aggregator.py` program so the infromation can be put in `state.json`.
4. Copy the directory minus the virtual environment (and pycache if it was created). This selective copy can be easily done with `rsync`: `rsync -av --exclude='venv' --exclude='__pycache__' /path/to/UMA/ martin@<target IP or hostname.local>:/home/martin/UMA/`

On the RPi5:

1. In the project directory, make the chrome script executable: `chmod +x start-chromium.sh`
2. create a venv (with the same version of python): `python -m venv venv` and activate. Then install all requirements.
3. Copy the service files: `sudo cp *.service /etc/systemd/system/`
4. Enable them: `sudo systemctl enable --now UMA-chrome UMA-aggregator UMA-server`

If it doesn't work immediately, debug with `sudo journalctl -f -u UMA-<service>` or manually run the commands of each service and see what breaks.
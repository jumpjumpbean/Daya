import os

# Import the main Flask app
from daya import app

# Get Blueprint Apps
# from notes import notes_app
from auth.views import bp_auth
from device.views import bp_device
from user.views import bp_user

# Register Blueprints
# app.register_blueprint(notes_app)

app.register_blueprint(bp_auth)
app.register_blueprint(bp_device)
app.register_blueprint(bp_user)

# start the server
if __name__ == "__main__":
    app.run()

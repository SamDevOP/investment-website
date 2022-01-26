import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
#DATABASE_URL="postgresql://localhost:62032/peakinvestors"

#app.config.from_object(os.environ['APP_SETTINGS'])
APP_SETTINGS="config.DevelopmentConfig"
app.config.from_object(APP_SETTINGS)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

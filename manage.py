from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from bucketlist.app import app, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/DIDAH/projects/Checkpoints/checkpoint2/CP2-Bucketlist-App/bucketlist/bucketlist.db'
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
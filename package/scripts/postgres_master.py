from resource_management import *
from postgres_base import PostgresBase

class PostgresServer(PostgresBase):
    postgres_packages = ['postgresql96-server']

    def install(self, env):
        import params
        env.set_params(params)
        self.install_postgres(env)
        print "Initializing Postgress DB"
        init_cmd = format("service postgresql-9.6 initdb")
        Execute(init_cmd)
        print "Configuring DRUID and SUPERSET databases"
        self.configure_databases(env)
        self.configure_postgres(env)

    def configure(self, env):
        import params
        env.set_params(params)
        self.configure_postgres(env)
        reload_cmd = format("service postgresql-9.6 reload")
        Execute(reload_cmd)

    def start(self, env):
        print "Starting postgres"
        self.configure(env)
        start_cmd = format("service postgresql-9.6 start")
        Execute(start_cmd)

    def stop(self, env):
        print "Stopping postgres"
        stop_cmd = format("service postgresql-9.6 stop")
        Execute(stop_cmd)

    def restart(self, env):
        print "Restartarting postgres"
        self.configure(env)
        Execute('service postgresql-9.6 restart')

    def status(self, env):
        print "Checking postgres status..."
        Execute('service postgresql-9.6 status')

if __name__ == "__main__":
    PostgresServer().execute()

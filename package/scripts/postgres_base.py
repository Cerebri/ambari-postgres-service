import  sys,subprocess,os
import requests
from time import sleep

import ambari_simplejson as json # simplejson is much faster comparing to Python 2.6 json module and has the same functions set.
from resource_management import *

class PostgresBase(Script):

    postgres_packages = []

    def install_postgres(self, env):
        import params
        env.set_params(params)
        Execute('yum -y -t -d 0 -e 0 remove postgresql92-server-9.2.15-1.57.amzn1.x86_64')
        Execute('yum -y -t -d 0 -e 0 remove postgresql92-9.2.15-1.57.amzn1.x86_64')
        Execute('yum -y -t -d 0 -e 0 remove postgresql92-libs-9.2.15-1.57.amzn1.x86_64')
        Execute('yum -y -t -d 0 -e 0 install https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-6-x86_64/pgdg-ami201503-96-9.6-2.noarch.rpm')
        print "Installing Postgres..."
        for pack in self.postgres_packages:
            Package(pack)

    def configure_databases(self, env):
        import params
        env.set_params(params)
        cmdfile=format("/tmp/postgres_createdb")
        File(cmdfile,
             mode=0600,
             content=InlineTemplate("create database registry;\n"
                                    "CREATE USER registry WITH PASSWORD 'registry';\n"
                                    "GRANT ALL PRIVILEGES ON DATABASE \"registry\" to registry;\n"
                                    "create database streamline;\n"
                                    "CREATE USER streamline WITH PASSWORD 'streamline';\n"
                                    "GRANT ALL PRIVILEGES ON DATABASE \"streamline\" to streamline;\n"
                                    "create database druid;\n"
                                    "CREATE USER druid WITH PASSWORD 'druid';\n"
                                    "GRANT ALL PRIVILEGES ON DATABASE  \"druid\" to druid;\n"
                                    "create database superset;\n"
                                    "CREATE USER superset WITH PASSWORD 'superset';\n"
                                    "GRANT ALL PRIVILEGES ON DATABASE \"superset\" to superset;\n")
             )
        Execute(format("su - {postgres_user} -c \"psql -d postgres -p {tcp_port} -f {cmdfile}\""))

    def configure_postgres(self, env):
        import params
        env.set_params(params)
        site_configurations = params.config['configurations']['postgres-site']
        File(format("{conf_dir}/postgresql.conf"),
             content=Template("postgresql.conf.j2", configurations = site_configurations),
             owner=params.postgres_user,
             mode=0600
             )
        hba_configurations = params.config['configurations']['postgres-hba']
        File(format("{conf_dir}/pg_hba.conf"),
             content=Template("pg_hba.conf.j2", configurations = hba_configurations),
             owner=params.postgres_user,
             mode=0600
             )
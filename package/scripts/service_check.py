#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import print_function
from resource_management import *
import  sys,subprocess,os
import requests
import time

class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
        cmdfile=format("/tmp/postgres_smoketest")
        File(cmdfile,
             mode=0600,
             content=InlineTemplate("CREATE DATABASE smoketest WITH OWNER postgres;\n"
                                    "\\c smoketest\n"
                                    "CREATE TABLE films (\n"
                                    "    code        char(5) CONSTRAINT firstkey PRIMARY KEY,\n"
                                    "    title       varchar(40) NOT NULL,\n"
                                    "    did         integer NOT NULL,\n"
                                    "    date_prod   date,\n"
                                    "    kind        varchar(10),\n"
                                    "    len         interval hour to minute\n"
                                    ");\n"
                                    "CREATE TABLE distributors (\n"
                                    "     did    integer PRIMARY KEY,\n"
                                    "     name   varchar(40) NOT NULL\n"
                                    ");\n"
                                    "INSERT INTO films VALUES\n"
                                    "    ('UA502', 'Bananas', 105, '1971-07-13', 'Comedy', '82 minutes');\n"
                                    "\c postgres\n"
                                    "DROP DATABASE smoketest;\n")
             )
        Execute(format("su - {postgres_user} -c \"psql -d postgres -p {tcp_port} -f {cmdfile}\""))

if __name__ == "__main__":
    ServiceCheck().execute()

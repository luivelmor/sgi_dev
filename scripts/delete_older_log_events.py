import datetime
from gorilla.models import Manifest, Event, EventLog

import psycopg2
from psycopg2 import Error

connection = None
cursor = None

try:
    # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                  password="m1_dj4ngu1t0_db",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="sgi_django")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")

    #############################################################################################
    ######################################    MY SQL EXECUTION    ###############################
    #############################################################################################
    manifests = Manifest.objects.all()
    for manifest in manifests:
        # Order = de mas recientes a mas antiguos. Los 20 mas nuevos me los quedo
        last_20 = EventLog.objects.filter(manifest=manifest.id).order_by("-timeWritten")[:20]
        # todos
        all = EventLog.objects.filter(manifest=manifest.id)
        # a eliminar
        count_to_delete = all.count() - last_20.count()
        # query a eliminar
        items_to_delete = EventLog.objects.filter(manifest=manifest.id).order_by("timeWritten")[:count_to_delete]
        for eventLog in items_to_delete:
            # Executing a SQL query
            sql = "DELETE FROM gorilla_eventlog WHERE id= {}".format(eventLog.id)
            cursor.execute(sql)
            connection.commit()
            print(cursor.rowcount, "record(s) deleted")


    #############################################################################################
    #############################################################################################
    #############################################################################################

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

# Open a file with access mode 'a'
date = datetime.datetime.now()
file_object = open('/var/www/sgi_django/scripts/other_logs.txt', 'a')
file_object.write('{} - Se eliminaron los ultimos 20 eventLogs de cada manifest\n'.format(date))
file_object.close()


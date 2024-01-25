import psycopg2
import sshtunnel


class SQLMirror(object):
    def __init__(
        self,
        mirror_host,
        mirror_port,
        mirror_db_name,
        mirror_username,
        mirror_password,
        ssh_username,
        ssh_password,
        ssh_port,
        ssh_host,
    ):
        self.mirror_host = mirror_host
        self.mirror_port = mirror_port
        self.mirror_db_name = mirror_db_name
        self.mirror_username = mirror_username
        self.mirror_password = mirror_password
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.ssh_port = ssh_port
        self.ssh_host = ssh_host

    def query(self, query):
        try:
            server = sshtunnel.SSHTunnelForwarder(
                (self.ssh_host, int(self.ssh_port)),
                ssh_username=self.ssh_username,
                ssh_password=self.ssh_password,
                remote_bind_address=(self.mirror_host, int(self.mirror_port)),
            )
            server.start()
            con = psycopg2.connect(
                host="localhost",
                port=server.local_bind_port,
                database=self.mirror_db_name,
                user=self.mirror_username,
                password=self.mirror_password,
            )

            print("Server connected")
        except Exception as e:
            print("Something went wrong with connecting", e)
            return None
        try:
            print("Server queried")
            cursor = con.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            print(records)
            return records
        except Exception as e:
            print("something went wrong", e)
            return None
        finally:
            if server:
                server.close()

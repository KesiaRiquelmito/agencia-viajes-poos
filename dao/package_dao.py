from exceptions.database import AlreadyExistsError, DatabaseError


class PackageDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def save(self, package, destination_ids):
        name = package.name
        start_date = package.start_date
        end_date = package.end_date
        total_price = package.total_price

        try:
            exist = self.db_connection.fetch_all(
                "SELECT id FROM package WHERE name = %s", (name,)
            )
            if exist:
                raise AlreadyExistsError
            cursor = self.db_connection.execute(
                "INSERT INTO package (name, start_date, end_date, total_price) VALUES (%s, %s, %s, %s)",
                (name, start_date, end_date, total_price),
            )
            package_id = cursor.lastrowid

            for destination_id in destination_ids:
                self.db_connection.execute(
                    "INSERT INTO package_destinations (package_id, destination_id) VALUES (%s, %s)",
                    (package_id, destination_id)
                )
        except DatabaseError:
            raise

    def get_all(self):
        try:
            return self.db_connection.fetch_all(
                "SELECT id, name, start_date, end_date, total_price FROM package"
            )
        except DatabaseError:
            raise

    def get_destinations_by_package_id(self, package_id: int):
        try:
            rows = self.db_connection.fetch_all(
                "SELECT d.name FROM package_destinations pd JOIN destinations d ON d.id = pd.destination_id WHERE pd.package_id = %s", (package_id,),
            )
            return rows
        except DatabaseError:
            raise

"""DAO for package persistence and relations."""

from exceptions.database import AlreadyExistsError, DatabaseError, DeletionNotCompleted


class PackageDAO:
    """Persist packages and link them with destinations."""

    def __init__(self, db_connection):
        """Initialize storage layer."""
        self.db_connection = db_connection

    def save(self, package, destination_ids):
        """Insert a package and create destination relationships."""
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
            return package_id
        except DatabaseError:
            raise

    def get_all(self):
        """Fetch every package row."""
        try:
            return self.db_connection.fetch_all(
                "SELECT id, name, start_date, end_date, total_price FROM package"
            )
        except DatabaseError:
            raise

    def get_destinations_by_package_id(self, package_id: int):
        """Return destination names linked to the given package."""
        try:
            rows = self.db_connection.fetch_all(
                "SELECT d.name FROM package_destinations pd JOIN destinations d ON d.id = pd.destination_id WHERE pd.package_id = %s", (package_id,),
            )
            return rows
        except DatabaseError:
            raise

    def update(self, package_id, package, destination_ids):
        """Update package basic data plus its destination links."""
        try:
            exists = self.db_connection.fetch_all("SELECT id FROM package WHERE id = %s", (package_id,))
            if not exists:
                return None

            self.db_connection.execute(
                "UPDATE package SET name = %s, start_date = %s, end_date = %s, total_price = %s WHERE id = %s",
                (package.name, package.start_date, package.end_date, package.total_price, package_id),
            )
            self.db_connection.execute("DELETE FROM package_destinations WHERE package_id = %s", (package_id,))
            for destination_id in destination_ids:
                self.db_connection.execute(
                    "INSERT INTO package_destinations (package_id, destination_id) VALUES (%s, %s)",
                    (package_id, destination_id),
                )
            return package_id
        except DatabaseError:
            raise

    def delete(self, package_id):
        """Delete a package and its destination relationships."""
        try:
            exists = self.db_connection.fetch_all("SELECT id FROM package WHERE id = %s", (package_id,))
            if not exists:
                return None

            self.db_connection.execute("DELETE FROM package_destinations WHERE package_id = %s", (package_id,))
            cursor = self.db_connection.execute("DELETE FROM package WHERE id = %s", (package_id,))
            if cursor.rowcount == 0:
                raise DeletionNotCompleted
            return package_id
        except DatabaseError:
            raise

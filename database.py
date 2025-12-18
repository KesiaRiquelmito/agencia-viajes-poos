import sys
import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.connection, self.cursor = self.get_connection()
        self._create_schema()

    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                user="root",
                password="root",
                host="localhost",
                database="travel_agency",
                auth_plugin="mysql_native_password",
            )
            cursor = connection.cursor()
            return connection, cursor
        except Error:
            print("No se pudo conectar a la base de datos. Revisa usuario/clave.")
            sys.exit(1)

    def _create_schema(self):
        stmts = [
            """
                CREATE TABLE IF NOT EXISTS users
                (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    hashed_password VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS destinations
                (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL,
                    description VARCHAR(1000) NOT NULL,
                    activities JSON NOT NULL,
                    cost DECIMAL(10, 2) NOT NULL
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS package
                (   
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    total_price DECIMAL(10, 2) NOT NULL
            )
            """,
            """
                CREATE TABLE IF NOT EXISTS package_destinations
                (
                    package_id INT,
                    destination_id INT,
                    PRIMARY KEY (package_id, destination_id),
                    FOREIGN KEY (package_id) REFERENCES package(id) ON DELETE CASCADE,
                    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS reservations
                (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    package_id INT NOT NULL,
                    reservation_date DATE NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (package_id) REFERENCES package(id) ON DELETE CASCADE
                )
                    
            """
        ]
        for stmt in stmts:
            self.cursor.execute(stmt)
        self.connection.commit()
        print("Base de datos y tablas creadas correctamente.")

if __name__ == "__main__":
    Database()

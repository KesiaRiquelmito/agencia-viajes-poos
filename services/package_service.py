"""Package service providing persistence orchestration."""

from dao.package_dao import PackageDAO
from models.tourist_package import TouristPackage


class PackageService:
    """Wrap DAO calls for tourist packages."""

    def __init__(self, db):
        """Create DAO using provided connection."""
        self.package_dao = PackageDAO(db)

    def create_package(self, package_data):
        """Persist a new package and related destinations."""
        package = TouristPackage(
            package_data["name"],
            package_data["start_date"],
            package_data["end_date"],
            package_data["total_price"]
        )
        return self.package_dao.save(package, package_data["destinations"])

    def get_packages_summary(self):
        """Return friendly data for CLI listing."""
        packages = self.package_dao.get_all()
        result = []

        for pid, name, start_date, end_date, total_price in packages:
            dest_rows = self.package_dao.get_destinations_by_package_id(pid)
            dest_names = [dname for (dname,) in dest_rows]

            result.append({
                "id": pid,
                "name": name,
                "start_date": start_date,
                "end_date": end_date,
                "destinations": dest_names,
                "total_price": total_price,
            })
        return result

    def update_package(self, package_id, package_data):
        """Update a package and its destination links."""
        package = TouristPackage(
            package_data["name"],
            package_data["start_date"],
            package_data["end_date"],
            package_data["total_price"],
        )
        return self.package_dao.update(package_id, package, package_data["destinations"])

    def delete_package(self, package_id):
        """Delete package by id."""
        return self.package_dao.delete(package_id)

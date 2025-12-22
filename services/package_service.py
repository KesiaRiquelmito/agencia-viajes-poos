from dao.package_dao import PackageDAO
from models.tourist_package import TouristPackage


class PackageService:
    def __init__(self, db):
        self.package_dao = PackageDAO(db)

    def create_package(self, package_data):
        package = TouristPackage(
            package_data["name"],
            package_data["start_date"],
            package_data["end_date"],
            package_data["total_price"]
        )
        return self.package_dao.save(package, package_data["destinations"])

    def get_packages_summary(self):
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

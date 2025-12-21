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
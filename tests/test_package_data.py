from pipfreezer import PackageData


class TestPackageData:
    """Test the PackageData class."""

    def test_package_data(self):
        package = PackageData("requests==2.25.1")
        assert package.name == "requests"
        assert package.version == "2.25.1"
        assert package.comment is None

    def test_package_data_with_comment(self):
        package = PackageData("requests==2.25.1  # HTTP library")
        assert package.name == "requests"
        assert package.version == "2.25.1"
        assert package.comment == "HTTP library"

    def test_package_with_extra_requirement(self):
        package = PackageData(
            "psycopg[c]==3.1.18  # https://github.com/psycopg/psycopg"
        )
        assert package.name == "psycopg[c]"
        assert package.version == "3.1.18"
        assert package.comment == "https://github.com/psycopg/psycopg"

    def test_freeze_package(self):
        package = PackageData("requests>=2.25.1")
        assert package.freeze() == "requests==2.25.1"

    def test_freeze_package_no_version(self):
        package = PackageData("requests  # HTTP library")
        assert package.freeze() == "requests  # HTTP library"

    def test_freeze_package_no_version_no_comment(self):
        package = PackageData("requests")
        assert package.freeze() == "requests"

    def test_str(self):
        package = PackageData("requests==2.25.1  # HTTP library")
        assert (
            str(package)
            == "PackageData(name='requests', version='2.25.1', comment='HTTP library')"
        )

    def test_repr(self):
        package = PackageData("requests==2.25.1  # HTTP library")
        assert repr(package) == "PackageData('requests==2.25.1  # HTTP library')"

    def test_as_json(self):
        package = PackageData("requests==2.25.1  # HTTP library")
        assert (
            package.as_json()
            == '{"name": "requests", "version": "2.25.1", "comment": "HTTP library"}'
        )

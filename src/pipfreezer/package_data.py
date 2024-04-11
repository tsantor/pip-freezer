import json
import re


class PackageData:
    """Data class so we can manipulate packages and versions easily."""

    def __init__(self, package: str):
        package = package.strip()
        if matches := re.search(r"[==|~=|>=|<=]{2}", package, re.IGNORECASE):
            pack_ver = package.split(matches[0])
            self.name = pack_ver[0].lower()
            # Get version and comment if any
            ver_com = [x.strip() for x in pack_ver[1].split("#")]
            self.version = ver_com.pop(0)
            self.comment = "  # ".join(ver_com) if ver_com else None
        else:
            pack_com = [x.strip() for x in package.split("#")]
            self.name = pack_com.pop(0).lower()
            self.version = None
            self.comment = "  # ".join(pack_com) if pack_com else None

    def freeze(self) -> str:
        """Return a frozen package string."""
        if self.version:
            return (
                f"{self.name}=={self.version}  # {self.comment}"
                if self.comment
                else f"{self.name}=={self.version}"
            )
        return f"{self.name}  # {self.comment}" if self.comment else self.name

    def as_json(self) -> str:
        """Return package data as JSON."""
        return json.dumps(
            {
                "name": self.name,
                "version": self.version,
                "comment": self.comment,
            }
        )

    def __str__(self) -> str:
        return (
            f"PackageData(name='{self.name}', version='{self.version}', "
            f"comment='{self.comment if self.comment else ''}')"
        )

    def __repr__(self) -> str:
        if self.comment:
            return f"PackageData('{self.name}=={self.version}  # {self.comment}')"
        return f"PackageData('{self.name}=={self.version}')"

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if not isinstance(other, PackageData):
            # don't attempt to compare against unrelated types
            return NotImplemented

        # Compare the name and version (comment is ignored)
        return self.name == other.name and self.version == other.version

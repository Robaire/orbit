# Robaire Galliath, 2024

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class TLE:
    # Title (Line 0)
    title: str

    # Line 1
    catalog_number: int
    classification: str
    launch_year: int
    launch_number: int
    launch_piece: str
    epoch_year: int
    epoch_day: float
    mean_motion_d1: float
    mean_motion_d2: float
    b_star: float
    ephemeris_type: int
    element_number: int

    # Line 2
    inclination: float  # [deg]
    right_ascension: float  # [deg]
    eccentricity: float  # [1]
    argument_perigee: float  # [deg]
    mean_anomaly: float  # [deg]
    mean_motion: float  # [rev/day]
    revolutions_epoch: int  # [1]

    @staticmethod
    def _checksum(line: str) -> int:
        """Calculate the checksum of a TLE line.

        Args:
            line: The line to calculate the checksum of.
            If validating a complete line, omit the checksum (last) character

        Returns:
            checksum: The checksum value
        """
        return sum([int(c) for c in line.replace("-", "1") if c.isdigit()]) % 10

    @classmethod
    def from_string(cls, tle_string: str) -> TLE:
        """Generate a TLE from a standard two or three line element set.

        Args:
            string: A two or three line element set

        Returns:
            TLE object
        """

        input = [x.strip() for x in tle_string.split("\n") if x.strip()]

        if len(input) != 2 and len(input) != 3:
            raise ValueError("Invalid TLE format")

        if len(input) == 2:
            title = ""
            line1 = input[0]
            line2 = input[1]
        else:
            title = input[0]
            line1 = input[1]
            line2 = input[2]

        # Extract line 1 elements
        if cls._checksum(line1[:-1]) != int(line1[-1:]):
            raise ValueError("Invalid checksum in line 1")

        line1 = [x.strip() for x in line1.split(" ") if x]
        catalog_number = int(line1[1][:5])
        classification = line1[1][5:]
        launch_year = int(line1[2][:2])
        launch_year += 1900 if launch_year <= 99 and launch_year >= 57 else 2000
        launch_number = int(line1[2][2:5])
        launch_piece = line1[2][5:]

        epoch_year = int(line1[3][:2])
        epoch_year += 1900 if epoch_year <= 99 and epoch_year >= 57 else 2000

        epoch_day = float(line1[3][2:])
        mean_motion_d1 = float(line1[4])

        mean_motion_d2 = float("." + line1[5][-7:-2] + "e" + line1[5][-2:])
        if line1[5][0] == "-":
            mean_motion_d2 *= -1

        b_star = float("." + line1[6][-7:-2] + "e" + line1[6][-2:])
        if line1[6][0] == "-":
            b_star *= -1

        ephemeris_type = int(line1[7])
        element_number = int(line1[8][:-1])

        # Extract line 2 elements
        if cls._checksum(line2[:-1]) != int(line2[-1:]):
            raise ValueError("Invalid checksum in line 2")

        line2 = [x.strip() for x in line2.split(" ") if x]
        inclination = float(line2[2])
        right_ascension = float(line2[3])
        eccentricity = float("." + line2[4])
        argument_perigee = float(line2[5])
        mean_anomaly = float(line2[6])
        mean_motion = float(line2[7][:-6])
        revolutions_epoch = int(line2[7][-6:-1])

        return cls(
            title,
            catalog_number,
            classification,
            launch_year,
            launch_number,
            launch_piece,
            epoch_year,
            epoch_day,
            mean_motion_d1,
            mean_motion_d2,
            b_star,
            ephemeris_type,
            element_number,
            inclination,
            right_ascension,
            eccentricity,
            argument_perigee,
            mean_anomaly,
            mean_motion,
            revolutions_epoch,
        )

    @classmethod
    def from_file(cls, file_path: str) -> TLE:
        """Generate a TLE from a file.

        Args:
            file_path: File path

        Returns:
            TLE object
        """

        with open(file_path, "r") as file:
            return TLE.from_string(file.read())

    @staticmethod
    def _zero_float(n: float) -> str:
        """Format a float in the scientific notation used in a TLE."""
        if n == 0:
            return " 00000-0"

        result = "" if n < 0 else " "
        result += f"{n:.4e}".split("e")[0].replace(".", "")
        result += str(int(f"{n:.0e}".split("e")[1]) + 1)
        return result

    def to_string(self) -> str:
        """Generate a TLE string."""

        title = self.title
        if title != "":
            title = title[:24] + "\n"  # limit to 24 characters

        # Line 1
        line1 = (
            f"1 {self.catalog_number:5}{self.classification[:1]} "
            + f"{self.launch_year}"[-2:]
            + f"{self.launch_number:03}{self.launch_piece:3} "
            + f"{self.epoch_year}"[-2:]
            + f"{self.epoch_day:12.8f} "
        )
        line1 += "-." if self.mean_motion_d1 < 0 else " ."
        line1 += f"{self.mean_motion_d1:.8f}".split(".")[1] + " "
        line1 += self._zero_float(self.mean_motion_d2) + " "
        line1 += self._zero_float(self.b_star) + " "
        line1 += f"{self.ephemeris_type} {self.element_number:4}"
        line1 += f"{self._checksum(line1)}\n"

        # Line 2
        line2 = (
            f"2 {self.catalog_number:5} {self.inclination:8.4f} "
            + f"{self.right_ascension:8.4f} "
            + f"{self.eccentricity:.7f}".split(".")[1]
            + f" {self.argument_perigee:8.4f} {self.mean_anomaly:8.4f} "
            + f"{self.mean_motion:11.8f}{self.revolutions_epoch:05}"
        )
        line2 += f"{self._checksum(line2)}"

        return title + line1 + line2

    def __str__(self) -> str:
        return self.to_string()

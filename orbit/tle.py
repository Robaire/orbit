# Robaire Galliath, 2024

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

    @classmethod
    def from_string(cls, tle_string: str):
        """Generate a TLE from a standard two or three line element set.

        Args:
            string: A two or three line element set

        Returns:
            TLE: TLE object
        """

        input = [x.strip() for x in tle_string.split("\n") if x.strip()]

        if len(input) != 2 and len(input) != 3:
            raise ValueError("Improperly formatted TLE")

        if len(input) == 2:
            title = ""
            line1 = input[0]
            line2 = input[1]
        else:
            title = input[0]
            line1 = input[1]
            line2 = input[2]

        # Extract line 1 elements
        line1 = [x.strip() for x in line1.split(" ") if x]
        catalog_number = int(line1[1][:5])
        classification = line1[1][5:]
        launch_year = int(line1[2][:2])
        launch_number = int(line1[2][2:5])
        launch_piece = line1[2][5:]
        epoch_year = int(line1[3][:2])
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
    def from_file(cls, file_path):
        """Generate a TLE from a file.

        Args:
            file_path: File path

        Return:
            TLE: TLE object
        """

        with open(file_path, "r") as file:
            return TLE.from_string(file.read())

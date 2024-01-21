import math
from typing import Literal, Optional

from . import constants as const
from . import qty

class Coord:
    __lat = None
    __lon = None

    def __init__(self, lat: float, lon: float, unit: Literal["deg", "rad"] = "deg"):
        self.set_lat(lat, unit)
        self.set_lon(lon, unit)

    def __hash__(self):
        if not self.__lat or not self.__lon:
            return hash(0)
        return hash(self.__lat + self.__lon)

    def __repr__(self):
        return f"lat: {self.__lat}, lon: {self.__lon}"

    def __str__(self):
        return f"Latitude: {self.__lat:.2f}°, Longitude: {self.__lon:.2f}°"

    def __eq__(self, x):
        if isinstance(x, Coord):
            return self.get_latlon() == x.get_latlon()
        else:
            return False

    def __ne__(self, x):
        if isinstance(x, Coord):
            return self.get_latlon() != x.get_latlon()
        else:
            return True

    def set_lat(self, lat: float, unit: Literal["deg", "rad"] = "deg") -> "Coord":
        """
        Sets the latitude of the coordinate
        """
        if unit.lower() not in ["deg", "rad"]:
            raise TypeError("Unit not of supported type")

        if unit.lower() == "rad":
            lat = math.degrees(lat)

        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be in range [-90, 90]")

        self.__lat = lat

        return self

    def set_lon(self, lon: float, unit: Literal["deg", "rad"] = "deg") -> "Coord":
        """
        Sets the longitude of the coordinate
        """
        if unit.lower() not in ["deg", "rad"]:
            raise TypeError("Unit not of supported type")

        if unit.lower() == "rad":
            lon = math.degrees(lon)

        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be in range [-180, 180]")

        self.__lon = lon

        return self

    def get_lat(self, unit: Literal["deg", "rad"] = "deg") -> Optional[float]:
        """
        Returns the latitude of the coordinate.

        Parameters
        ----------
        unit: "deg" or "rad", default "deg"
            Unit of measurement for latitude.

        Returns
        -------
        float

        Examples
        --------
        >>> coord = Coord(40, 50)
        >>> coord.get_lat()
        40
        >>> coord.get_lat("rad")
        0.698...
        """
        if unit.lower() not in ["deg", "rad"]:
            raise TypeError("Unit not of supported type")

        if self.__lat == None:
            return None

        if unit == "rad":
            return math.radians(self.__lat)

        return self.__lat

    def get_lon(self, unit: Literal["deg", "rad"] = "deg") -> Optional[float]:
        """
        Returns the longitude of the coordinate.

        Parameters
        ----------
        unit: "deg" or "rad", default "deg"
            Unit of measurement for longitude.

        Returns
        -------
        float

        Examples
        --------
        >>> coord = Coord(40, 50)
        >>> coord.get_lat()
        50
        >>> coord.get_lat("rad")
        0.872...
        """
        if unit.lower() not in ["deg", "rad"]:
            raise TypeError("Unit not of supported type")

        if self.__lon == None:
            return None

        if unit == "rad":
            return math.radians(self.__lon)

        return self.__lon

    def get_latlon(self, unit: Literal["deg", "rad"] = "deg") -> tuple[float, float]:
        """
        Returns the latitude and longitude of the coordinate.

        Parameters
        ----------
        unit: "deg" or "rad", default "deg"
            Unit of measurement for latitude and longitude.

        Returns
        -------
        tuple of (lat, lon)

        Examples
        --------
        >>> coord = Coord(40, 50)
        >>> coord.get_latlon()
        (40, 50)
        >>> coord.get_latlon("rad")
        (0.698..., 0.872...)
        """
        if unit.lower() not in ["deg", "rad"]:
            raise TypeError("Unit not of supported type")

        if self.__lat == None or self.__lon == None:
            raise ValueError("Latitude and Longitude must not be None")

        if unit == "rad":
            return (math.radians(self.__lat), math.radians(self.__lon))

        return (self.__lat, self.__lon)

    def isclose(self, coord: "Coord", tolerance: float = 0.5) -> bool:
        """
        Returns whether the coordinate is close the given other coordinate.

        Parameters
        ----------
        coord: Coord
            Other coordinate of which the closeness is compared to.
        tolerance: float between 0.1 and 10, default 0.5
            Tolerance of closeness in degrees of lat/lon.


        Returns
        -------
        Boolean

        Examples
        --------
        >>> coord1 = (0, 0)
        >>> coord2 = (2, 3)
        >>> coord1.isclose(coord2, tolerance=2)
        False
        >>> coord1.isclose(coord2, tolerance=3)
        True
        """
        lat, lon = coord.get_latlon()

        if tolerance < 0.1 or tolerance > 10:
            raise ValueError("Tolerance is not in range [0, 10]")

        if self.__lat == None or self.__lon == None:
            raise ValueError("lat and lon must not be None")

        if (lat - tolerance < self.__lat < lat + tolerance) and (lon - tolerance < self.__lon < lon + tolerance):
            return True
        return False

    def get_distance_bearing(
        self, coord: "Coord", method: Literal["haversine", "vincenty"] = "haversine"
    ) -> tuple[qty.Distance, float]:
        """
        Return meters of distance and bearing in degrees to the given point.

        Parameters
        ----------
        coord: Coord
            The coordinate to which the distance should be calculated.
        method: str
            The method of calculation, either haversine or vincenty. Defaults to haversine.

        Returns
        -------
        Distance
            From the qty module, represents value in meters.

        Examples
        --------
        >>> coord1 = Coord(0, 0)
        >>> coord2 = Coord(0, 90)
        >>> coord1.get_distance(coord2)
        10018754.17 meters

        Source
        ------
        https://www.movable-type.co.uk/scripts/latlong.html
        """
        lat1, lon1 = self.get_latlon("rad")
        lat2, lon2 = coord.get_latlon("rad")

        if method == "vincenty":
            distance, azimuth = self._vincenty_inverse((lat1, lon1), (lat2, lon2))
            return qty.Distance(distance), azimuth
        elif method == "haversine":
            delta_lon = lon2 - lon1

            y = math.sin(delta_lon) * math.cos(lat2)
            x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)

            distance = (
                math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(delta_lon))
                * const.Earth.radius
            )

            bearing_rad = math.atan2(y, x)
            bearing_deg = (math.degrees(bearing_rad) + 360) % 360

            return qty.Distance(distance), bearing_deg
        else:
            raise NotImplementedError("Method has to be either haversine or vincenty")

    def get_next_coord(
        self, dist: qty.Distance, bearing_deg: float, method: Literal["haversine", "vincenty"] = "haversine"
    ) -> "Coord":
        """
        Returns the a coordinate that is a given amount of meters away from that point, maintaining the given bearing.

        Parameters
        ----------
        dist: Distance
            Distance value from the qty module, represented in meters.
        bearing_deg: float
            Bearing to the next coordinate in degrees.
        method: str
            The method of calculation, either haversine or vincenty. Defaults to haversine.

        Returns
        -------
        Coord

        Examples
        --------
        >>> coord1 = Coord(0, 0)
        >>> distance = qty.Distance(10000)
        >>> bearing = 180
        >>> coord1.get_next_coord(distance, bearing)
        Latitude: -89.83°, Longitude: 0.00°

        Source
        ------
        https://www.movable-type.co.uk/scripts/latlong.html
        """

        if method == "vincenty":
            lat1, lon1 = self.get_latlon("deg")
            coord = self._vincenty_direct((lat1, lon1), dist.base, bearing_deg)
            return coord
        elif method == "haversine":
            lat1, lon1 = self.get_latlon("rad")
            bearing = math.radians(bearing_deg)
            angular_dist = dist / const.Earth.radius

            lat2 = math.asin(
                math.sin(lat1) * math.cos(angular_dist) + math.cos(lat1) * math.sin(angular_dist) * math.cos(bearing)
            )

            lon2 = lon1 + math.atan2(
                math.sin(bearing) * math.sin(angular_dist) * math.cos(lat1),
                math.cos(angular_dist) - math.sin(lat1) * math.sin(lat2),
            )

            return Coord(lat2, lon2, unit="rad")
        else:
            raise NotImplementedError

    @staticmethod
    def _vincenty_inverse(coord1: tuple[float, float], coord2: tuple[float, float]) -> tuple[float, float]:
        """
        Returns the distance and azimuth to a given coordinate using the Vincenty formalae.

        Parameters
        ----------
        coord1: tuple[float, float]
            Coordinate (lat, lon) in radians from which the distance and azimuth needs to be calculated.
        coord2: tuple[float, float]
            Coordinate (lat, lon) in radians to which the distance and azimuth needs to be calculated.

        Returns
        -------
        tuple[float, float]
            A tuple containing distance and bearing as floats.

        Source
        ------
        A slight adaptation from `vinc.py`, provided by Alejandro Murrieta, which in turn is an adaptation from a MATLAB file from RMIT Australia.
        """
        if coord1 == coord2:
            m = 0
            az12 = 0
            return m, az12

        maxIter = 200
        tol = 10**-12

        a = 6378137.0  # radius at equator in meters (WGS-84)
        f = 1 / 298.257223563  # flattening of the ellipsoid (WGS-84)
        b = (1 - f) * a

        phi_1, L_1 = coord1
        phi_2, L_2 = coord2

        u_1 = math.atan((1 - f) * math.tan(phi_1))  # u is psi
        u_2 = math.atan((1 - f) * math.tan(phi_2))

        L = L_2 - L_1

        Lambda = L  # set initial value of lambda to L

        sin_u1 = math.sin(u_1)
        cos_u1 = math.cos(u_1)
        sin_u2 = math.sin(u_2)
        cos_u2 = math.cos(u_2)

        # --- BEGIN ITERATIONS -----------------------------+
        iters = 0
        for i in range(0, maxIter):
            iters += 1

            cos_lambda = math.cos(Lambda)
            sin_lambda = math.sin(Lambda)

            sin_sigma = math.sqrt(
                (cos_u2 * math.sin(Lambda)) ** 2 + (cos_u1 * sin_u2 - sin_u1 * cos_u2 * cos_lambda) ** 2
            )
            cos_sigma = sin_u1 * sin_u2 + cos_u1 * cos_u2 * cos_lambda
            sigma = math.atan2(sin_sigma, cos_sigma)

            sin_alpha = (cos_u1 * cos_u2 * sin_lambda) / sin_sigma
            cos_sq_alpha = 1 - sin_alpha**2

            try:
                cos2_sigma_m = cos_sigma - ((2 * sin_u1 * sin_u2) / cos_sq_alpha)
            except:
                cos2_sigma_m = 0

            C = (f / 16) * cos_sq_alpha * (4 + f * (4 - 3 * cos_sq_alpha))

            Lambda_prev = Lambda
            Lambda = L + (1 - C) * f * sin_alpha * (
                sigma + C * sin_sigma * (cos2_sigma_m + C * cos_sigma * (-1 + 2 * cos2_sigma_m**2))
            )

            # successful convergence
            diff = abs(Lambda_prev - Lambda)

            if diff <= tol:
                break

        u_sq = cos_sq_alpha * ((a**2 - b**2) / b**2)
        A = 1 + (u_sq / 16384) * (4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq)))
        B = (u_sq / 1024) * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))
        delta_sig = (
            B
            * sin_sigma
            * (
                cos2_sigma_m
                + 0.25
                * B
                * (
                    cos_sigma * (-1 + 2 * cos2_sigma_m**2)
                    - (1 / 6) * B * cos2_sigma_m * (-3 + 4 * sin_sigma**2) * (-3 + 4 * cos2_sigma_m**2)
                )
            )
        )

        m = b * A * (sigma - delta_sig)  # output distance in meters     \\
        y_amm = cos_u2 * sin_lambda
        x_amm = (cos_u1 * sin_u2) - (sin_u1 * cos_u2 * cos_lambda)
        alpha1_amm = math.atan2(y_amm, x_amm)
        if alpha1_amm < 0:
            alpha1_amm = alpha1_amm + 2 * math.pi
        az12 = alpha1_amm * (180 / math.pi)

        return m, az12

    @staticmethod
    def _vincenty_direct(coord: tuple[float, float], distance: float, azimuth: float) -> "Coord":
        """
        Return a corresponding coordinate when given a distance and azimuth.

        Parameters
        ----------
        coord: tuple[float, float]
            A tuple of two floats of (lat, lon).
        distance: float
            float representing the distance in meters.
        azimuth: float
            float representing the azimuth in degrees to the new coordinate.

        Returns
        -------
        Coord
            An instance of the Coord class from the given distance and azimuth.

        Source
        ------
        A slight adaptation from `vinc.py`, provided by Alejandro Murrieta, which in turn is an adaptation from a MATLAB file from RMIT Australia.
        """

        lat1, lon1 = coord
        phi1, lambda1 = math.radians(lat1), math.radians(lon1)
        # Define some constants
        d2r = 180 / math.pi
        twopi = 2 * math.pi
        pion2 = math.pi / 2
        # Set defining ellipsoid parameters
        a = 6378137
        # GRS80
        flat = 298.257222101

        # Compute derived ellipsoid constants
        f = 1 / flat
        b = a * (1 - f)
        e2 = f * (2 - f)
        ep2 = e2 / (1 - e2)

        # ------------------------------------
        # azimuth of geodesic P1-P2 (degrees)
        # ------------------------------------
        # az12 = 1 + 43/60 + 25.876544/3600;
        # az12=294 +38/60+ 59.528610/3600;

        # azimuth of geodesic P1-P2 (radians)
        alpha1 = azimuth / d2r
        # sine and cosine of azimuth P1-P2
        sin_alpha1 = math.sin(alpha1)
        cos_alpha1 = math.cos(alpha1)
        # ------------------
        # geodesic distance
        # ------------------
        # s = 3692399.836991*0.75;
        # [1] Compute parametric latitude psi1 of P1
        psi1 = math.atan((1 - f) * math.tan(phi1))
        # [2] Compute parametric latitude of vertex
        psi0 = math.acos(math.cos(psi1) * sin_alpha1)

        # [3] Compute geodesic constant u2 (u-squared)
        u2 = ep2 * (math.sin(psi0) ** 2)
        # [4] Compute angular distance sigma1 on the auxiliary sphere from equator
        # to P1'
        sigma1 = math.atan2(math.tan(psi1), cos_alpha1)
        # [5] Compute the sine of the azimuth of the geodesic at the equator
        sin_alphaE = math.cos(psi0)
        # [6] Compute Vincenty's constants A and B
        A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
        B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
        # [7] Compute sigma by iteration
        sigma = distance / (b * A)
        iterat = 1
        while 1:
            two_sigma_m = 2 * sigma1 + sigma
            s1 = math.sin(sigma)
            s2 = s1 * s1
            c1 = math.cos(sigma)
            c1_2m = math.cos(two_sigma_m)
            c2_2m = c1_2m * c1_2m
            t1 = 2 * c2_2m - 1
            t2 = -3 + 4 * s2
            t3 = -3 + 4 * c2_2m
            delta_sigma = B * s1 * (c1_2m + B / 4 * (c1 * t1 - B / 6 * c1_2m * t2 * t3))
            sigma_new = distance / (b * A) + delta_sigma
            if abs(sigma_new - sigma) < 1e-12:
                break
            sigma = sigma_new
            iterat = iterat + 1

        s1 = math.sin(sigma)
        c1 = math.cos(sigma)
        # [8] Compute latitude of P2
        y = math.sin(psi1) * c1 + math.cos(psi1) * s1 * cos_alpha1
        x = (1 - f) * math.sqrt(sin_alphaE**2 + (math.sin(psi1) * s1 - math.cos(psi1) * c1 * cos_alpha1) ** 2)
        phi2 = math.atan2(y, x)
        lat2 = phi2 * d2r
        # [9] Compute longitude difference domega on the auxiliary sphere
        y = s1 * sin_alpha1
        x = math.cos(psi1) * c1 - math.sin(psi1) * s1 * cos_alpha1
        domega = math.atan2(y, x)
        # [10] Compute Vincenty's constant C
        x = 1 - sin_alphaE**2
        C = f / 16 * x * (4 + f * (4 - 3 * x))
        # [11] Compute longitude difference on ellipsoid
        two_sigma_m = 2 * sigma1 + sigma
        c1_2m = math.cos(two_sigma_m)
        c2_2m = c1_2m * c1_2m
        dlambda = domega - (1 - C) * f * sin_alphaE * (sigma + C * s1 * (c1_2m + C * c1 * (-1 + 2 * c2_2m)))
        dlon = dlambda * d2r
        lon2 = lon1 + dlon
        # [12] Compute azimuth alpha2
        y = sin_alphaE
        x = math.cos(psi1) * c1 * cos_alpha1 - math.sin(psi1) * s1
        alpha2 = math.atan2(y, x)
        # [13] Compute reverse azimuth az21
        az21 = alpha2 * d2r + 180
        if az21 > 360:
            az21 = az21 - 360

        return Coord(lat2, lon2)

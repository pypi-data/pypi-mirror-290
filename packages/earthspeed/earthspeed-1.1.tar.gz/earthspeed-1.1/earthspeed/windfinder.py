"""DM Windfinder: to find the Earth velocity in the galactic rest frame.

Details of the Earth's elliptical orbit around the Sun follow
    Lewin & Smith (1996), "Review of mathematics, numerical factors, and
    corrections for dark matter experiments based on elastic nuclear recoil".
with updated numerical values from 2105.00599 (D. Baxter et. al., "Recommended
conventions for reporting results from direct dark matter searches") for the
local standard of rest (LSR) and the Sun peculiar velocity

Default values: (all velocities in km/s)
- local standard of rest velocity: (0, 238., 0)
- solar peculiar velocity: (11.1, 12.2, 7.3)
- average Earth speed: 29.8
These values are used in vEt(date) to recover the instantaneous Earth
    speed in the galactic rest frame, as a function of time ('date').

* Example: recent vE(t) maximum at 2024 May 30, 05:28 UTC: vE = 266.2 km/s

This package uses the datetime format for time (e.g. '1999-12-31T12:00:00')
and astropy for conversions between galactic and ICRS coordinate systems.

Important functions:
* vEt(obstime, vCirc_kms=238., at_Sun=False): returns the Earth velocity
    vE(t) at time 'obstime' in Cartesian galactic coordinates
    vCirc_kms: sets the circular speed of the LSR
    at_Sun: if True, then sets the Earth speed relative to the Sun to zero.

* vE_AltAz(obstime, location): translates vE(t) into altitude and azimuth
    coordinates, for an observer at 'location' on Earth.
    Here obstime is a datetime object, location is an astropy.EarthLocation

* Windfinder(obstimes): a class, that finds the right ascension (RA)
    and declination (dec) of vE, also the (l, b) galactic coordinates and |vE|,
    for every observation time in the list obstimes.
    Windfinder.altAz(location) finds (alt, az) coordinates at 'location'.



"""

__all__ = ['km_s', 'vEt', 'vE_AltAz', 'Windfinder', 'vEt_sincemax', 'now']


import numpy as np
import math
import datetime as dts #for calendar functions
from astropy import units as u
from astropy.coordinates import SkyCoord, Galactic, ICRS, AltAz
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body
from astropy.coordinates import CartesianRepresentation, CartesianDifferential
from astropy.time import Time

#internal units for  velocity: (from blillard/vsdm)
VUNIT_c = (2.99792e5)**(-1) # [velocity] unit, in units of c.
# dependent quantities:
g_c = 1./VUNIT_c # The speed of light in units of [velocity]
km_s = (2.99792e5)**(-1) * g_c # 1 km/s in units of [velocity]

def vEt(obstime, vCirc_kms=238., at_Sun=False):
    """Returns the instantaneous Earth velocity in the galactic rest frame.

    obstime: a datetime object (year, month, day, hour=...)
        can be timezone-aware. If not, then obstime is assumed to be in UTC
        Recommendation: use timezone-aware obstime, especially when using
        datetime built-in functions like datetime.now().

    vCirc_kms: value to use for the speed of the LSR in the galactic rest frame
    at_Sun: can 'turn off' the annual variation by returning the Sun velocity
        rather than the Earth velocity

    returns vE in Cartesian coordinates (U, V, W):
        U: points towards the galactic center
        V: points in direction of motion of the local group standard of rest
        W: points out of the galactic plane (right handed coordinate system)
    """
    # from Lewin & Smith, 1996, Appx B
    # with updated numeric values from arXiv:2105.00599
    # date: a datetime object (year, month, day, hour=...)
    # returns vE in km_s
    uR = (0, vCirc_kms*km_s, 0) #local group velocity. 1996 value: (230)
    uS = (11.1*km_s, 12.2*km_s, 7.3*km_s) # Sun wrt local group. 1996: (9, 12, 7)

    if at_Sun:
        #turn off the annual modulation
        vE = np.array([uR[0]+uS[0], uR[1]+uS[1], uR[2]+uS[2]])
        return vE

    # time reference: noon UTC, 31 Dec 1999
    if obstime.tzinfo is None:
        datetime0 = dts.datetime.fromisoformat('1999-12-31T12:00:00') # aka J2000.0
    else:
        datetime0 = dts.datetime(1999, 12, 31, hour=12, tzinfo=dts.timezone.utc) # aka J2000.0
    difftime = obstime - datetime0
    nDays = difftime.days + difftime.seconds/(24*3600)

    # Earth velocity w.r.t. the Sun:
    uE_avg = 29.79*km_s
    els = 0.016722 # ellipticity of Earth orbit
    # angular constants (all in degrees)
    lam0 = 13. # longitude of orbit minor axis. has error +- 1 degree (1996)
    bX = -5.5303
    bY = 59.575
    bZ = 29.812
    lX = 266.141
    lY = -13.3485
    lZ = 179.3212
    L = (280.460 + 0.9856474*nDays) % 360 # (degrees)
    g = (357.528 + 0.9856003*nDays) % 360# (degrees)
    # ecliptic longitude:
    lam = L + 1.915*math.sin(g * math.pi/180) + 0.020*math.sin(2*g * math.pi/180)
    uEl = uE_avg * (1 - els*math.sin((lam - lam0)*math.pi/180))
    uEx = uEl * math.cos(bX * math.pi/180) * math.sin((lam - lX)*math.pi/180)
    uEy = uEl * math.cos(bY * math.pi/180) * math.sin((lam - lY)*math.pi/180)
    uEz = uEl * math.cos(bZ * math.pi/180) * math.sin((lam - lZ)*math.pi/180)
    vE = np.array([uR[0]+uS[0]+uEx, uR[1]+uS[1]+uEy, uR[2]+uS[2]+uEz])
    return vE

def vEt_sincemax(n_days, vCirc_kms=238.):
    """Simple method for annual variation, vE(n_days) for days since last maximum.

    Using 2024-05-30 05:28:00 as the reference point, where vE(t) is maximized.
    n_days can be float-valued.
    """
    date_ref = dts.datetime(2024, 5, 30, 5, 28, 0)
    date = date_ref + dts.timedelta(days=n_days)
    vE = vEt(date, vCirc_kms=vCirc_kms)
    return vE

def dts_to_astro(date):
    """Convert from datetime to astropy date format."""
    y_s = "{0:04d}".format(date.year)
    mo_s = "{0:02d}".format(date.month)
    d_s = "{0:02d}".format(date.day)
    h_s = "{0:02d}".format(date.hour)
    mi_s = "{0:02d}".format(date.minute)
    s_s = "{0:02d}".format(date.second)
    out_s = y_s + "-" + mo_s + "-" + d_s + " " + h_s + ":" + mi_s + ":" + s_s
    return out_s

def vE_AltAz(obstime, location, vCirc=238.*km_s):
    if obstime.tzinfo is not None:
        obstime = obstime.astimezone(dts.timezone.utc)
    vE_uvw = vEt(obstime, vCirc_kms=vCirc/km_s, at_Sun=False)
    speed = np.linalg.norm(vE_uvw)
    U_kms, V_kms, W_kms = vE_uvw/km_s
    wvec = Galactic(u=U_kms*u.pc, v=V_kms*u.pc, w=W_kms*u.pc,
                    representation_type=CartesianRepresentation)
    altaz = AltAz(obstime=dts_to_astro(obstime), location=location)
    wind = wvec.transform_to(altaz)
    alt = wind.alt.degree
    az = wind.az.degree
    return np.array([speed, alt, az])

def now(location=None, vCirc=238.*km_s, at_Sun=False, RA_hours=False):
    """Prints the vE location at the current moment. Returns Windfinder(now).

    location: if not None, then now() also prints the (alt, az) sky position.
    RA_hours: if True, returns RA in units of hours rather than degrees.
    """
    obstime = dts.datetime.now(dts.timezone.utc)
    wind = Windfinder([obstime], vCirc=vCirc, at_Sun=at_Sun)
    if RA_hours:
        radec = wind.RAdec_h[0]
        raunit = 'hour'
    else:
        radec = wind.RAdec[0]
        raunit = 'deg'
    print('DM wind location at {} (UTC):'.format(obstime))
    print('\tRA = {:.3f} [{}] \tdec = {:.3f} [deg]'.format(radec[0], raunit, radec[1]))
    if location is not None:
        lat = location.to_geodetic().lat
        lon = location.to_geodetic().lon
        alt, az = wind.altAz(location)[0]
        print('sky coordinates at Earth location (lat,lon) = ({:.3f}, {:.3f}) [deg]:'.format(lat.deg, lon.deg))
        print('\taltitude = {:.3f} [deg] \tazimuth = {:.3f} [deg]'.format(alt, az))
        #
    return wind

class Windfinder():
    """Finds the galactic frame Earth velocity at times 'obstimes'.

    All angles are returned in degrees. All speeds are in units of [velocity]
    as set above by VUNIT_c. By default, [velocity] = km/s.

    Arguments:
        obstimes: a list of datetime objects (can be timezone-aware)
        vCirc: circular speed of the LSR (default: 238 km/s)
        at_Sun: ignores the speed of the Earth relative to the Sun,
            to turn off the annual variation.

    Outputs:
        speed: value of |vE|
        vE_uvw: velocity in Cartesian galactic coordinates U, V, W
        RAdec: the right ascension and declination (RA, dec) of vE in degrees
        RAdec: RA and dec (RA, dec) of vE, with RA in hours (and dec in degrees)
        vE_RAdec: velocity (speed, RA, dec)
        lb: galactic coordinates (l, b) for velocity vector
        vE_lb: velocity (speed, l, b)
        galactic: an astropy.Galactic object (l, b, distance), with 'distance'
            set to (vE/km_s) parsec
    Method:
        vE_AltAz(location): the altitude and azimuth of vE on the sky,
            at 'location' at 'obstime'. 'location' is an EarthLocation object.
    """
    def __init__(self, obstimes, vCirc=238.*km_s, at_Sun=False):
        self.obstimes = np.zeros(len(obstimes), dtype='object')
        self.speed = np.zeros(len(obstimes))
        self.vE_uvw = np.zeros((len(obstimes), 3))
        self.RAdec = np.zeros((len(obstimes), 2))
        self.RAdec_h = np.zeros((len(obstimes), 2))
        self.vE_RAdec = np.zeros((len(obstimes), 3))
        self.lb = np.zeros((len(obstimes), 2))
        self.vE_lb = np.zeros((len(obstimes), 3))
        self.galactic = np.zeros(len(obstimes), dtype='object')

        for j,obstime in enumerate(obstimes):
            if obstime.tzinfo is not None:
                obstime = obstime.astimezone(dts.timezone.utc)
            self.obstimes[j] = obstime

            vE_uvw = vEt(obstime, vCirc_kms=vCirc/km_s, at_Sun=at_Sun)
            speed = np.linalg.norm(vE_uvw)
            self.vE_uvw[j] = vE_uvw
            self.speed[j] = speed

            U_kms, V_kms, W_kms = vE_uvw/km_s
            wvec = Galactic(u=U_kms*u.pc, v=V_kms*u.pc, w=W_kms*u.pc,
                            representation_type=CartesianRepresentation)
            # self.vE_lb = np.array([self.speed, self.wvec.l, self.wvec.b])

            icrs = wvec.transform_to(ICRS())
            RAdec = np.array([icrs.ra.deg, icrs.dec.deg])
            self.RAdec[j] = RAdec
            self.vE_RAdec[j] = np.array([speed, RAdec[0], RAdec[1]])

            RAdec_h = np.array([icrs.ra.hour, icrs.dec.deg])
            self.RAdec_h[j] = RAdec_h

            galactic = icrs.transform_to(Galactic()) # not Cartesian
            lb = np.array([galactic.l.deg, galactic.b.deg])
            self.lb[j] = lb
            self.vE_lb[j] = np.array([speed, lb[0], lb[1]])
            self.galactic[j] = galactic

    def altAz(self, location):
        """Sky position of vE vector at 'date' and 'location'.

        returns: (altitude, azimuth)

        location: an astropy.EarthLocation object, e.g.:
            EarthLocation(lat='41.8', lon='-88.3', height=0.*u.m)
        """
        altaz = np.zeros((len(self.obstimes), 2))
        for j,obstime in enumerate(self.obstimes):
            obstime = dts_to_astro(obstime)
            frame = AltAz(obstime=obstime, location=location)

            wind = self.galactic[j].transform_to(frame)
            alt = wind.alt.degree
            az = wind.az.degree
            altaz[j] = np.array([alt, az])
        return altaz

    def vE_altAz(self, location):
        """Sky position of vE vector at 'date' and 'location'.

        returns a vector: (|vE|, altitude, azimuth)

        location: an astropy.EarthLocation object, e.g.:
            EarthLocation(lat='41.8', lon='-88.3', height=0.*u.m)
        """
        vEaltaz = np.zeros((len(self.obstimes), 3))
        altaz = self.altAz(location)
        for j,aa in enumerate(altaz):
            alt, az = aa
            vEaltaz[j] = np.array([self.speed[j], alt, az])
        return vEaltaz























#

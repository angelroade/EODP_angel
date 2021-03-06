# LEVEL-1C

from l1c.src.initL1c import initL1c
from common.io.writeToa import writeToa, readToa
from common.io.readGeodetic import readGeodetic, getCorners
import mgrs
import numpy as np
from scipy.interpolate import bisplrep, bisplev
import matplotlib.pyplot as plt
from common.io.l1cProduct import writeL1c
from matplotlib import cm

class l1c(initL1c):

    def __init__(self, auxdir, indir, outdir):
        print(type(indir))
        print(indir)
        super().__init__(auxdir, indir, outdir)

    def processModule(self):

        self.logger.info("Start of the L1C Processing Module")

        for band in self.globalConfig.bands:

            self.logger.info("Start of BAND " + band)

            # Read TOA - output of the L1B in Radiances
            # -------------------------------------------------------------------------------
            toa = readToa(self.l1bdir, self.globalConfig.l1b_toa + band + '.nc')
            lat,lon = readGeodetic(self.gmdir, self.globalConfig.gm_geoloc)
            self.checkSize(lat,toa)

            # L1C reprojection onto the MGRS grid
            # -------------------------------------------------------------------------------
            lat_l1c, lon_l1c, toa_l1c = self.l1cProjtoa(lat, lon, toa, band)

            # Write output TOA
            # -------------------------------------------------------------------------------
            writeL1c(self.outdir, self.globalConfig.l1c_toa + band, lat_l1c, lon_l1c, toa_l1c)
            writeToa(self.outdir, self.globalConfig.l1c_toa + band, toa_l1c)
            self.logger.info("End of BAND " + band)

        self.logger.info("End of the L1C Module!")


    def l1cProjtoa(self, lat, lon, toa, band):
        '''
        This function reprojects the L1B radiances into the MGRS grid.
        The MGRS reference system
        https://www.bluemarblegeo.com/knowledgebase/calculator-2020/Military_Grid_Reference_System_(MGRS).htm
        MGRS: '31REQ4367374067'
        31 is the UTM zone, R is the UTM latitude band; EQ are the MGRS column and row band letters
        43673 is the MGRS Easting (5 dig); 74067 is the MGRS Northing (5dig)
        Python mgrs library documentation
        https://pypi.org/project/mgrs/
        :param lat: L1B latitudes [deg]
        :param lon: L1B longitudes [deg]
        :param toa: L1B radiances
        :param band: band
        :return: L1C radiances, L1C latitude and longitude in degrees
        '''
        # Create an interpolant with the L1B radiances and geodetic coordinates
        tck=bisplrep(lat,lon,toa)

        MGRS=mgrs.MGRS()
        MGRS_titles=set([])

        for i in range(lat.shape[0]):
            for j in range(lat.shape[1]):
                thistitle = str(MGRS.toMGRS(lat[i,j],lon[i,j],MGRSPrecision=self.l1cConfig.mgrs_tile_precision))
                MGRS_titles.add(thistitle)

        MGRS_titles = list(MGRS_titles)

        lat_l1c = np.zeros(len(MGRS_titles))
        lon_l1c = np.zeros(len(MGRS_titles))
        toa_l1c = np.zeros(len(MGRS_titles))

        for k in range(len(MGRS_titles)):
            lat_l1c[k],lon_l1c[k]=MGRS.toLatLon(MGRS_titles[k])
            toa_l1c[k]=bisplev(lat_l1c[k],lon_l1c[k],tck)

        #Plot l1c grid points. Cannot make it with panoply
        lat = getCorners(lat)
        lon = getCorners(lon)
        fig = plt.figure(figsize=(20,10))
        plt.plot(lon, lat, 'k', linewidth=2, label="L1B")
        plt.plot(lon_l1c, lat_l1c, 'r.', markersize=5, label="L1C MGRS")
        plt.title('Projection on ground for {}'.format(band), fontsize=20)
        plt.xlabel('Longitude [deg]', fontsize=16)
        plt.ylabel('Latitude [deg]', fontsize=16)
        plt.axis('equal')
        plt.grid()
        plt.legend()
        plt.savefig(self.outdir + 'gnd_proj_' + band + '.png')
        plt.close(fig)

        return lat_l1c, lon_l1c, toa_l1c

    def checkSize(self, lat,toa):
        '''
        Check the sizes of the input radiances and geodetic coordinates.
        If they don't match, exit.
        :param lat: Latitude 2D matrix
        :param toa: Radiance 2D matrix
        :return: NA
        '''
        if (lat.shape[0] != toa.shape[0]) or (lat.shape[1] != toa.shape[1]):
            raise Exception("Size of the input lat/lon matrices and the TOA doesn't match.")

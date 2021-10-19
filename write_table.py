# herpich@usp.br - 2020-11013

from astropy.io import fits,ascii
from astropy.table import Table
import numpy as np

# t = fits.open('iDR3_23J0ields_J0ornax_galaxies.fits')[1].data
t = ascii.read('STRIPE82-0001_match.csv')

fakeflag = np.zeros(t['u_petro'].size)

mags = np.array(list(zip(t['FUVmag'], t['NUVmag'],
                         t['u_petro'], t['J0378_petro'], t['J0395_petro'],
                         t['J0410_petro'], t['J0430_petro'], t['g_petro'],
                         t['J0515_petro'], t['r_petro'], t['J0660_petro'],
                         t['i_petro'], t['J0861_petro'], t['z_petro'],
                         t['Jmag'] + 0.91, t['Hmag'] + 1.39, t['Kmag'] + 1.85,
                         t['W1mag'] + 2.699, t['W2mag'] + 3.339,
                         t['W3mag'] + 5.174, t['W4mag'] + 6.620
                         )))
# Vega > AB 2MASS from http://www.astronomy.ohio-state.edu/~martini/usefuldata.html
# Vega > AB WISE from https://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec4_4h.html

mags_err = np.array(list(zip(t['e_FUVmag'], t['e_NUVmag'],
                             t['e_u_petro'], t['e_J0378_petro'], t['e_J0395_petro'],
                             t['e_J0410_petro'], t['e_J0430_petro'], t['e_g_petro'],
                             t['e_J0515_petro'], t['e_r_petro'], t['e_J0660_petro'],
                             t['e_i_petro'], t['e_J0861_petro'], t['e_z_petro'],
                             t['e_Jmag'], t['e_Hmag'], t['e_Kmag'],
                             t['e_W1mag'], t['e_W2mag'], t['e_W3mag'], t['e_W4mag']
                             )))

flags = np.array(list(zip(fakeflag, fakeflag,
                          t['PhotoFlag_u'], t['PhotoFlag_J0378'], t['PhotoFlag_J0395'],
                          t['PhotoFlag_J0410'], t['PhotoFlag_J0430'], t['PhotoFlag_g'],
                          t['PhotoFlag_J0515'], t['PhotoFlag_r'], t['PhotoFlag_J0660'],
                          t['PhotoFlag_i'], t['PhotoFlag_J0861'], t['PhotoFlag_z'],
                          fakeflag, fakeflag, fakeflag,
                          fakeflag, fakeflag, fakeflag, fakeflag
                          )))

columns = [t['ID_1'], t['RA'], t['DEC'], mags, mags_err, flags, t['zml'], t['zml_err']]
colnames = ['ID', 'RA', 'DEC', 'MAGS', 'MAGS_ERR', 'FLAGS', 'z', 'comment']

newt = Table(columns, names=colnames)
newt.write('STRIPE82-0001_SPLUS4alstar.fits', format='fits')

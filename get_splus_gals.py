from astroquery.xmatch import XMatch
from astropy import units as u
import pandas as pd
import splusdata

conn = splusdata.connect('login', 'password')
dir = '/path/to/preferred/directory'
fields = pd.read_csv('/path/to/csv/file/file.csv')

for field in fields['NAME']:
    print('Starting ' + f'{field}')
    aperture = 'petro'
    try:
        query_f = f"""SELECT det.ID, det.ra, det.dec, u.u_{aperture}, u.e_u_{aperture}, u.PhotoFlag_u, 
        j0378.j0378_{aperture}, j0378.e_j0378_{aperture}, j0378.PhotoFlag_j0378, j0395.j0395_{aperture}, 
        j0395.e_j0395_{aperture}, j0395.PhotoFlag_j0395, j0410.j0410_{aperture}, j0410.e_j0410_{aperture}, 
        j0410.PhotoFlag_j0410, j0430.j0430_{aperture}, j0430.e_j0430_{aperture}, j0430.PhotoFlag_j0430, 
        g.g_{aperture}, g.e_g_{aperture}, g.PhotoFlag_g, j0515.j0515_{aperture}, j0515.e_j0515_{aperture}, 
        j0515.PhotoFlag_j0515, r.r_{aperture}, r.e_r_{aperture}, r.PhotoFlag_r, j0660.j0660_{aperture}, 
        j0660.e_j0660_{aperture}, j0660.PhotoFlag_j0660, i.i_{aperture}, i.e_i_{aperture}, i.PhotoFlag_i, 
        j0861.j0861_{aperture}, j0861.e_j0861_{aperture}, j0861.PhotoFlag_j0861, z.z_{aperture}, z.e_z_{aperture}, 
        z.PhotoFlag_z, pz.zml, pz.zml_err
                      FROM idr3.detection_image as det                                                                                                                                         
                      JOIN idr3.u_band as u ON (u.ID = det.ID)                                                                                                                                 
                      JOIN idr3.j0378_band as j0378 ON (j0378.ID = det.ID)                                                                                                                     
                      JOIN idr3.j0395_band as j0395 ON (j0395.ID = det.ID)                                                                                                                     
                      JOIN idr3.j0410_band as j0410 ON (j0410.ID = det.ID)                                                                                                                     
                      JOIN idr3.j0430_band as j0430 ON (j0430.ID = det.ID)                                                                                                                     
                      JOIN idr3.g_band as g ON (g.ID = det.ID)                                                                                                                                 
                      JOIN idr3.j0515_band as j0515 ON (j0515.ID = det.ID)                                                                                                                     
                      JOIN idr3.r_band as r ON (r.ID = det.ID)                                                                                                                                 
                      JOIN idr3.j0660_band as j0660 ON (j0660.ID = det.ID)                                                                                                                     
                      JOIN idr3.i_band as i ON (i.ID = det.ID)                                                                                                                                 
                      JOIN idr3.j0861_band as j0861 ON (j0861.ID = det.ID)   
                      JOIN idr3.z_band as z ON (z.ID = det.ID)
                      JOIN idr3_vacs.photoz as pz ON (pz.ID = det.ID)     
                      JOIN idr3_vacs.star_galaxy_quasar as sgq ON (sgq.ID = det.ID)                                                                                                                                                                                                                     
                      WHERE det.field = '{field}' AND sgq.PROB_GAL > 0.9"""

        table = conn.query(query_f)
        print('Got the table!') #astropy.Table
        table.write(f'{dir}{field}_query.csv', overwrite=True)

        galex = XMatch.query(cat1=table, cat2='vizier:II/335/galex_ais', max_distance=2*u.arcsec, colRA1='RA', colDec1='DEC')
        tmass =  XMatch.query(cat1=galex, cat2='vizier:II/246/out', max_distance=2*u.arcsec, colRA1='RA', colDec1='DEC')
        wise = XMatch.query(cat1=tmass, cat2='vizier:II/328/allwise', max_distance=2*u.arcsec, colRA1='RA', colDec1='DEC')
        
        wise.write(f'{dir}{field}_match.csv', overwrite=True)
    except:
        print(f"Error on {field}")
        file = open('error.txt', 'a')
        file.write(f'Error on {field}\n')
        file.close()


import pandas as pd
import numpy as np
import splusdata
import os
import time

conn = splusdata.connect('user', 'pass')

fields = pd.read_csv('Sgalaxies.csv')

for field in fields['NAME']:
    print('Starting ' + f'{field}')
    aperture = 'aper_6'
    try:
        query_f = f"""SELECT det.ID, det.ra, det.dec, u.u_{aperture}, j0378.j0378_{aperture}, j0395.j0395_{aperture}, j0410.j0410_{aperture}, j0430.j0430_{aperture}, g.g_{aperture}, j0515.j0>
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
                      JOIN idr3_vacs.photoz_pdfs as pz ON (pz.ID = det.ID)                                                                                                                     
                      WHERE det.field = '{field}'"""

        table = conn.query(query_f)
        print('Got the table!')
        table.write(f'{field}.fits') ## para salvar tabela

        # ## Fazendo o cross-match com o 2MASS, GALEX e o unWISE.
        # os.system(f"""java -jar stilts.jar cdsskymatch in={value.field}.fits cdstable=II/246/out ra=RA dec=DEC radius=1 find=each blocksize=500000 ocmd='delcols "RAJ2000 DEJ2000 errHalfMaj>

        # os.system(f"""java -jar stilts.jar cdsskymatch in={value.field}_vac.fits cdstable=II/335/galex_ais ra=RA dec=DEC radius=2 find=each blocksize=500000 ocmd='delcols "RAJ2000 DEJ2000 >

        # os.system(f"""java -jar stilts.jar cdsskymatch in={value.field}_vac.fits cdstable=II/363/unwise ra=RA dec=DEC radius=1 find=each blocksize=500000 ocmd='delcols "RAdeg DEdeg XposW1 >

        # os.system(f"""rm {value.field}.fits""")

        # os.system(f"""rm {value.field}_vac.fits""")

    except:
        print(f"Error on {field}")
        file = open('error.txt', 'a')
        file.write(f'Error on {field}\n')
        file.close()
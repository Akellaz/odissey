import re
import json
import os


def gpx_to_json(gpx_file_path, json_file_path):
    
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file")
        
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            uploaded_file.save(file_path)

    file_name = os.path.splitext(os.path.basename(file_name))
    file_name_gpx = file_name[0]+'.gpx'
    file_name_json = 'static/json/'+file_name[0]+'.json'

    with open(file_name_json, 'a') as f1:
        header='{"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"coordinates": ['
        f1.write(header + '\n')
    f1.close()

    word_lat = 'lat="(.*?)"'
    word_lon = 'lon="(.*?)"'  

    fd_lat = open(file_name_gpx,"r")
    fd_lon = open(file_name_gpx,"r")  
    file_contents_lat = re.findall(word_lat, fd_lat.read())
    file_contents_lon = re.findall(word_lon, fd_lon.read())

    lon_lat=[]

    for i in file_contents_lon:
        lon_lat.append('[ '+i+', ')
        for i in file_contents_lat:
            lon_lat.append(i+' ],')
            file_contents_lat.remove(i)
            break

    last=re.sub(r'\],', ']', lon_lat[-1])
    lon_lat[-1] = last

    lon_lat_count=len(lon_lat)
      
    with open(file_name_json, 'a') as f:
        for ix in range(lon_lat_count):
            f.write(lon_lat[ix] + '\n')
            
    f.close()

    with open(file_name_json, 'a') as f2:
        footer='], "type": "LineString"}}]}'
        f2.write(footer + '\n')
    f2.close()

    fd_lat.close() 
    fd_lon.close()   

    
    
    return render_template('sup/sup.html', title='Сап-борд | Успешно', link=file_name[0])


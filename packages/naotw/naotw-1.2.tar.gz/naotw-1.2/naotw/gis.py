'GIS 工具模組'

def to_kml(gdf, k, name_column=None, folder_column=None, descs=None, folder_column2=None):
    from shapely.geometry.point import Point
    import simplekml

    gdf = gdf.to_crs(epsg=4326) # kml crs is epsg 4326
    kml = simplekml.Kml()
    if folder_column:
        if folder_column2:
            for f in gdf[folder_column].drop_duplicates():
                fol = kml.newfolder(name=f)
                gdf2 = gdf.query(f'{folder_column}==@f')
                for f2 in gdf2[folder_column2].drop_duplicates():
                    fol2 = fol.newfolder(name=f2)
                    ls = gdf2.query(f'{folder_column2}==@f2')
                    for i, l in ls.iterrows():
                        #print(l)
                        landid = l[name_column]
                        geometry = l['geometry']
                        if isinstance(geometry, Point):
                            fol2.newpoint(
                                 name=landid,
                                 coords=[(geometry.x, geometry.y)]
                                 #description=str(l[descs])
                                 )
                            continue
                        try:
                            #Polygon
                            coords = list(geometry.exterior.coords)
                        except:
                            #MultiPolygon
                            coords = [list(x.exterior.coords) for x in geometry.geoms]
                        finally:
                            fol2.newpolygon(
                                 name=landid,
                                 outerboundaryis=coords, 
                                 innerboundaryis=[], 
                                 description=str(l[descs])
                                 )
    else:
        for f in gdf[folder_column].drop_duplicates():
            fol = kml.newfolder(name=f)
            ls = gdf.query(f'{folder_column}==@f')
            #print(ls)
            for i, l in ls.iterrows():
                #print(l)
                landid = l[name_column]
                geometry = l['geometry']
                if isinstance(geometry, Point):
                    fol.newpoint(
                         name=landid,
                         coords=[(geometry.x, geometry.y)]
                         #description=str(l[descs])
                         )
                    continue
                try:
                    #Polygon
                    coords = list(geometry.exterior.coords)
                except:
                    #MultiPolygon
                    coords = [list(x.exterior.coords) for x in geometry.geoms]
                finally:
                    fol.newpolygon(
                         name=landid,
                         outerboundaryis=coords, 
                         innerboundaryis=[], 
                         description=str(l[descs])
                         )
    kml.save(k)

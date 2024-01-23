import vtk

def visualize(polygons1, polygons2, distance):
    # Crear un renderizador y una ventana de renderizado
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    # Crear un interactor de ventana de renderizado
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Establecer el estilo de interacción a TrackballCamera
    style = vtk.vtkInteractorStyleTrackballCamera()
    renderWindowInteractor.SetInteractorStyle(style)

    for polygons, z in zip([polygons1, polygons2], [0, distance]):
        for polygon_points in polygons:
            # Crear un polígono
            polygon = vtk.vtkPolygon()
            polygon.GetPointIds().SetNumberOfIds(len(polygon_points))

            # Crear un conjunto de puntos
            points = vtk.vtkPoints()

            for i, (x, y) in enumerate(polygon_points):
                points.InsertNextPoint(x, y, z)
                polygon.GetPointIds().SetId(i, i)

            # Crear una celda y añadir el polígono a la celda
            polygons = vtk.vtkCellArray()
            polygons.InsertNextCell(polygon)

            # Crear un poliData y añadir los puntos y los polígonos al poliData
            polyData = vtk.vtkPolyData()
            polyData.SetPoints(points)
            polyData.SetPolys(polygons)

            # Crear un mapeador y añadir el poliData al mapeador
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(polyData)

            # Crear un actor y añadir el mapeador al actor
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            # Añadir el actor al renderizador
            renderer.AddActor(actor)

    # Iniciar el interactor de ventana de renderizado
    renderWindowInteractor.Initialize()
    renderWindow.Render()
    renderWindowInteractor.Start()
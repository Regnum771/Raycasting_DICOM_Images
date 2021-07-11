# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 10:31:02 2021

@author: nqkha
"""
from vtk import (
    vtkDICOMImageReader, 
    vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor, 
    vtkFixedPointVolumeRayCastMapper, 
    vtkColorTransferFunction, vtkPiecewiseFunction,
    vtkVolume, vtkVolumeProperty
)

def main():
    # Create the renderer, the render window, and the interactor. 
    # The renderer draws into the render window, 
    # The interactor enables mouse and keyboard-based interaction with the scene.
    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # vtkDICOMImageReader reads all DICOM file within a directory
    reader = vtkDICOMImageReader()
    reader.SetDirectoryName("D:\\DICOM-RT-01")
    reader.Update()

    # Use a raycast mapper to create volume
    volumeMapper = vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    # The colorTransferFunction maps voxel intensities to colors.
    # In this example, it maps one color for flesh and another color for bone
    # Flesh (Red): Intensity between 500 and 1000
    # Bone (White): Intensity over 1150
    volumeColor = vtkColorTransferFunction()
    volumeColor.AddRGBPoint(0, 0.0, 0.0, 0.0)
    volumeColor.AddRGBPoint(500, 1.0, 0.5, 0.3)
    volumeColor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
    volumeColor.AddRGBPoint(1150, 1.0, 1.0, 0.9)

    #The opacityTransferFunction is used to control the opacity
    #of different tissue types.
    volumeScalarOpacity = vtkPiecewiseFunction()
    volumeScalarOpacity.AddPoint(0, 0.00)
    volumeScalarOpacity.AddPoint(500, 0.15)
    volumeScalarOpacity.AddPoint(1000, 0.15)
    volumeScalarOpacity.AddPoint(1150, 0.85)

    #The gradient opacity function is used to decrease the opacity
    #in the "flat" regions of the volume while maintaining the opacity
    #at the boundaries between tissue types.  The gradient is measured
    #as the amount by which the intensity changes over unit distance.
    #For most medical data, the unit distance is 1mm.
    volumeGradientOpacity = vtkPiecewiseFunction()
    volumeGradientOpacity.AddPoint(0, 0.0)
    volumeGradientOpacity.AddPoint(90, 0.5)
    volumeGradientOpacity.AddPoint(100, 1.0)

    # The VolumeProperty attaches the color and opacity functions to the
    # volume, and sets other volume properties. 
    
    # The interpolation should be set to linear to do a high-quality rendering.  
    
    volumeProperty = vtkVolumeProperty()
    volumeProperty.SetColor(volumeColor)
    volumeProperty.SetScalarOpacity(volumeScalarOpacity)
    volumeProperty.SetGradientOpacity(volumeGradientOpacity)
    volumeProperty.SetInterpolationTypeToLinear()
    
    # The ShadeOn option turns on directional lighting, which will usually 
    # enhance the appearance of the volume and make it look more "3D". 
    # volumeProperty.ShadeOn()
    
    # To decrease the impact of shading, increase the Ambient and 
    # decrease the Diffuse and Specular.  
    # To increase the impact of shading, decrease the Ambient and 
    # increase the Diffuse and Specular.
    volumeProperty.SetAmbient(0.4)
    volumeProperty.SetDiffuse(0.6)
    volumeProperty.SetSpecular(0.2)

    # The vtkVolume is a vtkProp3D (like a vtkActor) and controls the position
    # and orientation of the volume in world coordinates.
    volume = vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    # Add the volume to the renderer
    ren.AddViewProp(volume)

    # Set up an initial view of the volume.  The focal point will be the
    # center of the volume, and the camera position will be 400mm to the
    # patient's left
    camera = ren.GetActiveCamera()
    c = volume.GetCenter()
    camera.SetFocalPoint(c[0], c[1], c[2])
    camera.SetPosition(c[0] + 400, c[1], c[2])
    camera.SetViewUp(0, 0, -1)

    # Set the size of the renderer window
    renWin.SetSize(640, 480)

    # Enable interaction
    iren.Initialize()
    iren.Start()

if __name__ == '__main__':
    main()

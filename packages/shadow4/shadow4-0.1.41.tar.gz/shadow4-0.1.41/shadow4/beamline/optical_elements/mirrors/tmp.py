from shadow4.beamline.s4_beamline import S4Beamline

beamline = S4Beamline()

#
#
#
from shadow4.sources.source_geometrical.source_geometrical import SourceGeometrical

light_source = SourceGeometrical(name='SourceGeometrical', nrays=100, seed=5676561)
light_source.set_spatial_type_gaussian(sigma_h=0.00023026, sigma_v=0.000018)
light_source.set_depth_distribution_off()
light_source.set_angular_distribution_gaussian(sigdix=0.000037, sigdiz=0.000022)
light_source.set_energy_distribution_singleline(719.900000, unit='eV')
light_source.set_polarization(polarization_degree=1.000000, phase_diff=0.000000, coherent_beam=0)
beam = light_source.get_beam()

beamline.set_light_source(light_source)

# optical element number XX
from syned.beamline.shape import Rectangle

boundary_shape = Rectangle(x_left=-0.0025, x_right=0.0025, y_bottom=-0.0025, y_top=0.0025)

from shadow4.beamline.optical_elements.absorbers.s4_screen import S4Screen

optical_element = S4Screen(name='pupil', boundary_shape=boundary_shape,
                           i_abs=0,  # 0=No, 1=prerefl file_abs, 2=xraylib, 3=dabax
                           i_stop=0, thick=0, file_abs='<specify file name>', material='Au', density=19.3)

from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=18.151, q=0, angle_radial=0, angle_azimuthal=0, angle_radial_out=3.141592654)
from shadow4.beamline.optical_elements.absorbers.s4_screen import S4ScreenElement

beamline_element = S4ScreenElement(optical_element=optical_element, coordinates=coordinates, input_beam=beam)

beam, footprint = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# optical element number XX
from syned.beamline.shape import Rectangle

boundary_shape = Rectangle(x_left=-0.009, x_right=0.009, y_bottom=-0.1, y_top=0.1)

from shadow4.beamline.optical_elements.mirrors.s4_plane_mirror import S4PlaneMirror

optical_element = S4PlaneMirror(name='Plane Mirror', boundary_shape=boundary_shape,
                                f_reflec=0, f_refl=0, file_refl='<none>', refraction_index=0.99999 + 0.001j,
                                coating_material='Si', coating_density=2.33, coating_roughness=0)

from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=0, q=0, angle_radial=1.527163095, angle_azimuthal=4.71238898,
                                 angle_radial_out=1.527163095)
movements = None
from shadow4.beamline.optical_elements.mirrors.s4_plane_mirror import S4PlaneMirrorElement

beamline_element = S4PlaneMirrorElement(optical_element=optical_element, coordinates=coordinates, movements=movements,
                                        input_beam=beam)

beam, mirr = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# optical element number XX
from syned.beamline.shape import Rectangle

boundary_shape = Rectangle(x_left=-0.005, x_right=0.005, y_bottom=-0.06, y_top=0.06)

from shadow4.beamline.optical_elements.mirrors.s4_toroid_mirror import S4ToroidMirror

optical_element = S4ToroidMirror(name='Toroid Mirror', boundary_shape=boundary_shape,
                                 surface_calculation=1,
                                 min_radius=1.80257,  # min_radius = sagittal
                                 maj_radius=126.743,  # maj_radius = tangential
                                 f_torus=0,
                                 p_focus=0, q_focus=0, grazing_angle=0.0436332,
                                 f_reflec=0, f_refl=0, file_refl='<none>', refraction_index=0.99999 + 0.001j,
                                 coating_material='Si', coating_density=2.33, coating_roughness=0)

from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=0.470422, q=0, angle_radial=1.527163095, angle_azimuthal=3.141592654,
                                 angle_radial_out=1.527163095)
movements = None
from shadow4.beamline.optical_elements.mirrors.s4_toroid_mirror import S4ToroidMirrorElement

beamline_element = S4ToroidMirrorElement(optical_element=optical_element, coordinates=coordinates, movements=movements,
                                         input_beam=beam)

beam, mirr = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# test plot
if True:
    from srxraylib.plot.gol import plot_scatter

    plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)',
                 plot_histograms=0)
    plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')
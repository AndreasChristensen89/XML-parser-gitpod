from importlib.util import LazyLoader
from multiprocessing.sharedctypes import Value
from django import forms
from collections import Counter
from .models import Samples, Publications


IMPORT_MODE_CHOICES = (
        ("first import", "first import"),
        ("ignore", "ignore"),
        ("draft", "draft"),
        ("no change", "no change"),
        ("correction", "correction"),
)

TYPES_CHOICES = (
        ("laboratory measurement", "laboratory measurement"),
        ("numerical modeling", "numerical modeling"),
        ("theoretical modeling", "theoretical modeling"),
        ("field measurement", "field measurement"),
        ("low altitude", "low altitude"),
        ("satellite remote sensing", "satellite remote sensing"),
        ("telescopic remote sensing", "telescopic remote sensing"),
        ("other", "other"),
        ("unknown", "unknown"),
)

GEOLOCATION_TYPE = (
        ("point", "point"),
        ("line", "line"),
        ("box", "box"),
        ("polygon", "polygon"),
)

BODY_COORDINATE_SYSTEM = (
        ('', ''),
        ("WGS84", "WGS84"),
        ("Mars 2000", "Mars 2000"),
        ("Moon 2000", "Moon 2000"),
        ("Pluto 2015", "Pluto 2015"),
)

VARIABLE_PARAMETERS_TYPE = (
        ('', ''),
        ("no", "no"),
        ("sample composition", "sample composition"),
        ("sample abundance", "sample abundance"),
        ("sample size", "sample size"),
        ("sample thickness", "sample thickness"),
        ("sample texture", "sample texture"),
        ("sample grain size", "sample grain size"),
        ("sample phase", "sample phase"),
        ("constituent", "constituent"),
        ("chemical variability", "chemical variability"),
        ("formation condition", "formation condition"),
        ("temperature", "temperature"),
        ("pressure", "pressure"),
        ("mechanical stress", "mechanical stress"),
        ("reactant", "reactant"),
        ("time", "time"),
        ("irradiation type", "irradiation type"),
        ("irradiation energy", "irradiation energy"),
        ("irradiation dose", "irradiation dose"),
        ("spectrum type", "spectrum type"),
        ("spectral range", "spectral range"),
        ("illumination-observation geometry", "illumination-observation geometry"),
        ("incidence angle", "incidence angle"),
        ("emergence angle", "emergence angle"),
        ("azimuth angle", "azimuth angle"),
        ("phase angle", "phase angle"),
        ("polarization", "polarization"),
        ("observation mode", "observation mode"),
        ("other", "other"),
)

SPECTRAL_UNIT = (
        ("m-1", "m-1"),
        ("cm-1", "cm-1"),
        ("angstrom", "angstrom"),
        ("nm", "nm"),
        ("micron", "micron"),
        ("mm", "mm"),
        ("m", "m"),
        ("km", "km"),
        ("Hz", "Hz"),
        ("kHz", "kHz"),
        ("MHz", "MHz"),
        ("GHz", "GHz"),
        ("eV", "eV"),
        ("keV", "keV"),
)

SPECTRAL_STANDARD = (
        ("vacuum", "vacuum"),
        ("air", "air"),
        ("unknown", "unknown"),
)

SPECTRAL_OBERSATION_MODE = (
        ("spectrum", "spectrum"),
        ("multi wavelengths", "multi wavelengths"),
        ("single wavelength", "single wavelength"),
        ("multi spectral averages", "multi spectral averages"),
        ("single spectral average", "single spectral average"),
)

RANGE_TYPE = (
        ("gamma", "gamma"),
        ("hard X", "hard X"),
        ("soft X", "soft X"),
        ("EUV", "EUV"),
        ("VUV", "VUV"),
        ("UV", "UV"),
        ("Vis", "Vis"),
        ("NIR", "NIR"),
        ("MIR", "MIR"),
        ("FIR", "FIR"),
        ("sub-mm", "sub-mm"),
        ("mm", "mm"),
        ("cm", "cm"),
        ("UHF", "UHF"),
        ("VHF", "VHF"),
        ("HF", "HF"),
        ("MF", "MF"),
        ("LF", "LF"),
        ("VLF", "VLF"),
        ("ULF", "ULF"),
        ("SLF", "SLF"),
        ("ELF", "ELF"),
)

ANGLE_OBSERVATION_GEOMETRY = (
        ("direct", "direct"),
        ("specular", "specular"),
        ("bidirectional", "bidirectional"),
        ("directional-conical", "directional-conical"),
        ("conical-directional", "conical-directional"),
        ("biconical", "biconical"),
        ("directional-hemispherical", "directional-hemispherical"),
        ("conical-hemispherical", "conical-hemispherical"),
        ("hemispherical-directional", "hemispherical-directional"),
        ("hemispherical-conical", "hemispherical-conical"),
        ("bihemispherical", "bihemispherical"),
        ("directional", "directional"),
        ("conical", "conical"),
        ("hemispherical", "hemispherical"),
        ("other geometry", "other geometry"),
        ("various", "various"),
        ("unknown", "unknown"),
        ("N/A", "N/A"),
)

ANGLE_OBSERVATION_MODE = (
        ("fixed angles", "fixed angles"),
        ("one variable angle", "one variable angle"),
        ("two variable angles", "two variable angles"),
        ("three variable angles", "three variable angles"),
        ("fixed phase angle", "fixed phase angle"),
        ("mono-angular function", "mono-angular function"),
        ("bi-angular function", "bi-angular function"),
        ("tri-angular function", "tri-angular function"),
        ("fixed phase angle function", "fixed phase angle function"),
        ("other geometry set", "other geometry set"),
        ("unknown", "unknown"),
        ("N/A", "N/A"),
)

POLARIZATION_TYPE_ILLUMINATION = (
        ("linear", "linear"),
        ("circular", "circular"),
        ("elliptic", "elliptic"),
        ("no", "no"),
)

SPATIAL_OBSERVATION_MODE = (
        ("single spot", "single spot"),
        ("averaged", "averaged"),
        ("line", "line"),
        ("image", "image"),
        ("roi averaged", "roi averaged"),
        ("rastered", "rastered"),
        ("rastered image", "rastered image"),
)

SPATIAL_UNIT = (
        ("nm", "nm"),
        ("micron", "micron"),
        ("mm", "mm"),
        ("cm", "cm"),
)

SPECTRUM_IMPORT_MODE = (
        ("first import", "first import"),
        ("inherited", "inherited"),
        ("ignore", "ignore"),
        ("draft", "draft"),
        ("no change", "no change"),
        ("correction", "correction"),
        ("new version", "new version"),
        ("invalidate", "invalidate"),
)

SPECTRUM_EXPERIMENT_TYPE = (
        ('', ''),
        ("yes", "yes"),
        ("no", "no"),
        ("true", "true"),
        ("false", "false"),
)

SPECTRUM_TYPE = (
        ('normalized Raman scattering intensity', 'normalized Raman scattering intensity'),
        ("raw", "raw"),
        ("transmission", "transmission"),
        ("absorbance", "absorbance"),
        ("normalized absorbance", "normalized absorbance"),
        ("optical depth", "optical depth"),
        ("absorption coefficient", "absorption coefficient"),
        ("optical constants", "optical constants"),
        ("ATR transmission", "ATR transmission"),
        ( "ATR absorbance", "ATR absorbance"),
        ("corrected ATR absorbance", "corrected ATR absorbance"),
        ("complex admittance", "complex admittance"),
        ("complex impedance", "complex impedance"),
        ("relative complex permittivity", "relative complex permittivity"),
        ("dielectric loss tangent", "dielectric loss tangent"),
        ("relative complex permeability", "relative complex permeability"),
        ("magnetic loss tangent", "magnetic loss tangent"),
        ("bidirectional reflectance", "bidirectional reflectance"),
        ("bidirectional reflectance distribution function", "bidirectional reflectance distribution function"),
        ("radiance factor", "radiance factor"),
        ("reflectance factor", "reflectance factor"),
        ("albedo", "albedo"),
        ("complex reflectance ratio", "complex reflectance ratio"),
        ("Stokes parameter I", "Stokes parameter I"),
        ("Stokes parameter Q", "Stokes parameter Q"),
        ("Stokes parameter U", "Stokes parameter U"),
        ("Stokes parameter V", "Stokes parameter V"),
        ("Stokes parameters", "Stokes parameters"),
        ("polarization contrast", "polarization contrast"),
        ("degree of linear polarization", "degree of linear polarization"),
        ("polarization position angle", "polarization position angle"),
        ("degree of circular polarization", "degree of circular polarization"),
        ("polarization parameters", "polarization parameters"),
        ("thermal emission", "thermal emission"),
        ("thermal radiance", "thermal radiance"),
        ("thermal emittance", "thermal emittance"),
        ("thermal emissivity", "thermal emissivity"),
        ("scattering intensity", "scattering intensity"),
        ("differential scattering cross section", "differential scattering cross section"),
        ("normalized differential scattering cross section", "normalized differential scattering cross section"),
        ("scattering cross section", "scattering cross section"),
        ("absorption cross section", "absorption cross section"),
        ("extinction cross section", "extinction cross section"),
        ("scattering efficiency factor", "scattering efficiency factor"),
        ("absorption efficiency factor", "absorption efficiency factor"),
        ("extinction efficiency factor", "extinction efficiency factor"),
        ("single scattering albedo", "single scattering albedo"),
        ("Raman scattering intensity", "Raman scattering intensity"),
        ("normalized Raman scattering intensity", "normalized Raman scattering intensity"),
        ("Raman scattering coefficient", "Raman scattering coefficient"),
        ("Raman scattering efficiency", "Raman scattering efficiency"),
        ("fluorescence emission", "fluorescence emission"),
        ("normalized fluorescence emission", "normalized fluorescence emission"),
        ("fluorescence emission efficiency", "fluorescence emission efficiency"),
        ("radiative transfer model parameters", "radiative transfer model parameters"),
)

SPECTRUM_INTENSITY_UNIT = (
        ('AU', 'AU'),
        ("cm-1", "cm-1"),
        ("m-1", "m-1"),
        ("cm2.g-1", "cm2.g-1"),
        ("m2.kg-1", "m2.kg-1"),
        ("mL.g−1⋅cm−1", "mL.g−1⋅cm−1"),
        ("cm2⋅mol−1", "cm2⋅mol−1"),
        ("m2⋅mol−1", "m2⋅mol−1"),
        ("L⋅mol−1⋅cm−1", "L⋅mol−1⋅cm−1"),
        ("percent", "percent"),
        ("permille", "permille"),
        ("deg", "deg"),
        ("count.s-1", "count.s-1"),
        ("count.nm-1", "count.nm-1"),
        ("S", "S"),
        ("ohm", "ohm"),
        ("dB", "dB"),
        ("sr-1", "sr-1"),
        ("micron2", "micron2"),
        ("mm2", "mm2"),
        ("m2", "m2"),
        ("m-1.sr-1", "m-1.sr-1"),
        ("m2.sr-1", "m2.sr-1"),
        ("W.m-2", "W.m-2"),
        ("kW.m-2", "kW.m-2"),
        ("W.sr-1", "W.sr-1"),
        ("kW.sr-1", "kW.sr-1"),
        ("W.m-2.sr-1", "W.m-2.sr-1"),
        ("kW.m-2.sr-1", "kW.m-2.sr-1"),
        ("W.m-2.sr-1.cm-1", "W.m-2.sr-1.cm-1"),
        ("W.m-2.sr-1.micron-1", "W.m-2.sr-1.micron-1"),
        ("no unit", "no unit"),
        ("unknown", "unknown"),
)

PARAMETER_TYPE = (
        ('', ''),
        ("single spectrum", "single spectrum"),
        ("complex spectrum", "complex spectrum"),
        ("polarimetric spectrum", "polarimetric spectrum"),
        ("scattering spectrum", "scattering spectrum"),
        ("model parameters spectrum", "model parameters spectrum"),
        ("photometric data", "photometric data"),
        ("spectra of multiangle dataset", "spectra of multiangle dataset"),
        ("photometric data of multispectral dataset", "photometric data of multispectral dataset"),
        ("spectro-photometric data", "spectro-photometric data"),
        ("spectral image", "spectral image"),
        ("photometric images", "photometric images"),
        ("spectral images of multiangle dataset", "spectral images of multiangle dataset"),
        ("photometric images of multispectral dataset", "photometric images of multispectral dataset"),
        ("spectro-photometric images", "spectro-photometric images"),
)

PARAMETERS_INSTRUMENTS = (
        ('INSTRU_DILOR_XY_514_LST', 'INSTRU_DILOR_XY_514_LST'),
        ('INSTRU_LabRAM_HR800_514_LGLTPE', 'INSTRU_LabRAM_HR800_514_LGLTPE'),
        ('INSTRU_LabRAM_HR800_532_LGLTPE', 'INSTRU_LabRAM_HR800_532_LGLTPE'),
        ('INSTRU_LabRAM_HR800_evolution_532_LGLTPE', 'INSTRU_LabRAM_HR800_evolution_532_LGLTPE'),
        ('INSTRU_LabRAM_HR800_evolution_785_LGLTPE', 'INSTRU_LabRAM_HR800_evolution_785_LGLTPE'),
        ('INSTRU_LabRAM_Soleil_405_LGLTPE', 'INSTRU_LabRAM_Soleil_405_LGLTPE'),
        ('INSTRU_LabRAM_Soleil_532_LGLTPE', 'INSTRU_LabRAM_Soleil_532_LGLTPE'),
        ('INSTRU_LabRAM_Soleil_785_LGLTPE', 'INSTRU_LabRAM_Soleil_785_LGLTPE'),
        ('INSTRU_LabRAM_HR800_Deep_UV_244_LGLTPE', 'INSTRU_LabRAM_HR800_Deep_UV_244_LGLTPE'),
        ('INSTRU_LabRAM_HR800_Deep_UV_248_LGLTPE', 'INSTRU_LabRAM_HR800_Deep_UV_248_LGLTPE')
)

PARAMTER_FORMAT = (
        ('', ''),
        ("ascii-intensity", "ascii-intensity"),
        ("ascii-columns", "ascii-columns"),
        ("ascii-nicolet", "ascii-nicolet"),
        ("bin-nicolet", "bin-nicolet"),
        ("bin-spa-nicolet", "bin-spa-nicolet"),
        ("bin-spc-grams", "bin-spc-grams"),
        ("bin-opus-brucker", "bin-opus-brucker"),
        ("ascii-sbrdf-ipag", "ascii-sbrdf-ipag"),
        ("ascii-sbrdf-bern", "ascii-sbrdf-bern"),
        ("ascii-sbrdf-isep", "ascii-sbrdf-isep"),
)

VIBRATION_MODE = (
        ('', ''),
        ("stretching", "stretching"),
        ("stretching sym.", "stretching sym."),
        ("stretching antisym.", "stretching antisym."),
        ("bending", "bending"),
        ("bending in-p", "bending in-p"),
        ("bending out-p", "bending out-p"),
        ("bending sym.", "bending sym."),
        ("bending antisym.", "bending antisym."),
        ("bending sym. in-p (scissoring)", "bending sym. in-p (scissoring)"),
        ("bending antisym. in-p (rocking)", "bending antisym. in-p (rocking)"),
        ("bending sym. out-p (wagging)", "bending sym. out-p (wagging)"),
        ("bending antisym. out-p (twisting)", "bending antisym. out-p (twisting)"),
        ("deformation", "deformation"),
        ("stretching overtone", "stretching overtone"),
        ("bending overtone", "bending overtone"),
        ("combination", "combination"),
        ("other", "other"),
        ("unknown", "unknown"),
)

ROTATION_MODE = (
        ('', ''),
        ("free rotation", "free rotation"),
        ("hindered rotation", "hindered rotation"),
        ("libration", "libration"),
        ("unknown", "unknown"),
)

PHONON_MODE = (
        ('', ''),
        ("LO", "LO"),
        ("TO", "TO"),
        ("LA", "LA"),
        ("TA1", "TA1"),
        ("TA2", "TA2"),
        ("unknown", "unknown"),
)

MATERIAL_IMPORT_MODE = (
         ("first import", "first import"),
         ("inherited", "inherited"),
         ("use existing", "use existing"),
         ("ignore", "ignore"),
         ("draft", "draft"),
         ("no change", "no change"),
         ("correction", "correction")
)

SPATIAL_OBJECTIVE = (
        ("10x", "10x"),
        ("20x", "20x"),
        ("50x", "50x"),
        ("100x", "100x"),
        ("x10slwd", "x10slwd"),
        ("x20slwd", "x20slwd"),
        ("x50slwd", "x50slwd"),
        ("x80slwd", "x80slwd")
)

SPECTRUM_QUALITY_FLAG = (
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5")
)

PUBLICATION_TYPES = (
        ("journal", "journal"),
        ("book", "book"),
        ("conference proceeding", "conference proceeding"),
        ("abstract booklet", "abstract booklet"),
        ("thesis", "thesis"),
        ("report", "report"),
        ("manual", "manual"),
        ("catalog", "catalog"),
        ("database", "database"),
        ("other", "other")
)

PUBLICATION_DOCUMENT_TYPE = (
        ("article", "article"),
        ("review article", "review article"),
        ("discussion paper", "discussion paper"),
        ("discussion", "discussion"),
        ("correction", "correction"),
        ("book", "book"),
        ("book chapter", "book chapter"),
        ("conference paper", "conference paper"),
        ("conference abstract", "conference abstract"),
        ("phd thesis", "phd thesis"),
        ("master thesis", "master thesis"),
        ("scientific report", "scientific report"),
        ("technical report", "technical report"),
        ("technical documentation", "technical documentation"),
        ("catalog of data", "catalog of data"),
        ("catalog of objects", "catalog of objects"),
        ("database", "database"),
        ("numerical data set", "numerical data set"),
        ("other", "other"),
)

PUBLICATION_STATE = (
        ("published", "published"),
        ("in press", "in press"),
        ("submitted", "submitted"),
        ("internal", "internal"),
        ("unpublished", "unpublished")
)

PUBLICATION_ACCESS_RIGHT = (
        ("publisher copyright", "publisher copyright"),
        ("publisher free", "publisher free"),
        ("free", "free"),
        ("restricted", "restricted"),
)

PUBLICATION_IDENTIFIER_TYPE = (
        ("ARK", "ARK"),
        ("arXiv", "arXiv"),
        ("bibcode", "bibcode"),
        ("EISSN", "EISSN"),
        ("HAL", "HAL"),
        ("Handle", "Handle"),
        ("ISBN", "ISBN"),
        ("ISSN", "ISSN"),
        ("ISTC", "ISTC"),
        ("PMID", "PMID"),
        ("TEL", "TEL"),
        ("URL", "URL"),
        ("no", "no")
)

PUBLICATION_CONTENTS = (
        ("instrument-technique", "instrument-technique"),
        ("numerical model", "numerical model"),
        ("species", "species"),
        ("phase", "phase"),
        ("sample", "sample"),
        ("material-matter", "material-matter"),
        ("object", "object"),
        ("spectral data", "spectral data"),
        ("band list data", "band list data"),
        ("BRDF data", "BRDF data"),
        ("thermodynamic data", "thermodynamic data"),
        ("spectral data use", "spectral data use"),
        ("band list data use", "band list data use"),
        ("BRDF data use", "BRDF data use"),
        ("thermodynamic data use", "thermodynamic data use"),
        ("astrophysics", "astrophysics"),
        ("planetary sciences", "planetary sciences"),
        ("earth sciences", "earth sciences"),
        ("remote sensing", "remote sensing"),
        ("experimental physics", "experimental physics"),
        ("theoretical physics", "theoretical physics"),
        ("applied physics", "applied physics"),
        ("materials sciences", "materials sciences"),
        ("chemistry", "chemistry"),
        ("optics", "optics"),
        ("other application", "other application"),
)

SAMPLE_RELEVANCE = (
        ("main - major", "main - major"),
        ("main - minor", "main - minor"),
        ("impurity", "impurity"),
        ("product", "product"),
        ("precursor", "precursor"),
        ("unknown", "unknown")
)

SAMPLE_IS_GENERIC = (
        ("yes", "yes"),
        ("no", "no")
)

SAMPLE_TERRAIN_TYPE = (
        ("mineral surface", "mineral surface"),
        ("icy surface", "icy surface"),
        ("organic surface", "organic surface"),
        ("liquid surface", "liquid surface"),
        ("mixed surface types", "mixed surface types"),
        ("mineral subsurface", "mineral subsurface"),
        ("icy subsurface", "icy subsurface"),
        ("organic subsurface", "organic subsurface"),
        ("liquid subsurface", "liquid subsurface"),
        ("mixed subsurface types", "mixed subsurface types"),
        ("atmosphere", "atmosphere"),
        ("other", "other"),
        ("unknown", "unknown")
)

SAMPLE_GEOLOCATION_TYPE = (
        ("NULL", "NULL"),
        ("point", "point"),
        ("line", "line"),
        ("box", "box"),
        ("polygon", "polygon")
)

SAMPLE_PARAMETER_TIME_UNIT = (
        ("s", "s"),
        ("min", "min"),
        ("h", "h"),
        ("d", "d"),
)

SAMPLE_PARAMETER_UNIT = (
        ("K", "K"),
        ("C", "C"),
        ("F", "F")
)

SAMPLE_FLUID_TYPE = (
        ("atomic gas", "atomic gas"),
        ("plasma", "plasma"),
        ("molecular gas", "molecular gas"),
        ("molecular liquid", "molecular liquid"),
        ("liquid solution", "liquid solution"),
        ("ambient air", "ambient air"),
        ("purged air", "purged air"),
        ("vacuum", "vacuum"),
        ("other", "other")
)

SAMPLE_FLUID_PRESSURE_UNIT = (
        ("Pa", "Pa"),
        ("hPa", "hPa"),
        ("MPa", "MPa"),
        ("GPa", "GPa"),
        ("mbar", "mbar"),
        ("bar", "bar"),
        ("atm", "atm"),
        ("torr", "torr")
)

SAMPLE_LAYER_TYPE = (
        ("granular", "granular"),
        ("compact raw", "compact raw"),
        ("compact", "compact"),
        ("pellet", "pellet"),
        ("single grain", "single grain"),
        ("grains", "grains"),
        ("aerosols", "aerosols"),
        ("clusters", "clusters"),
        ("fluid", "fluid"),
        ("various", "various"),
        ("other", "other"),
        ("unknown", "unknown"),
)

SAMPLE_LAYER_TEXTURE = (
        ("muddy", "muddy"),
        ("earthy", "earthy"),
        ("pulverulent", "pulverulent"),
        ("loose fine grained", "loose fine grained"),
        ("loose coarse grained", "loose coarse grained"),
        ("loose granular", "loose granular"),
        ("sintered granular", "sintered granular"),
        ("cemented granular", "cemented granular"),
        ("mixed granular", "mixed granular"),
        ("compact", "compact"),
        ("compact glassy", "compact glassy"),
        ("compact poor grained", "compact poor grained"),
        ("compact fine grained", "compact fine grained"),
        ("compact coarse grained", "compact coarse grained"),
        ("compact lamellar", "compact lamellar"),
        ("compact fibrous", "compact fibrous"),
        ("compact crystal", "compact crystal"),
        ("compact mixed", "compact mixed"),
        ("single grain", "single grain"),
        ("individual grains", "individual grains"),
        ("aggregated grains", "aggregated grains"),
        ("isolated aerosols", "isolated aerosols"),
        ("aggregated aerosols", "aggregated aerosols"),
        ("clusters", "clusters"),
        ("liquid", "liquid"),
        ("gaseous", "gaseous"),
        ("other", "other"),
        ("unknown", "unknown")
)

SAMPLE_POROSITY_TYPE = (
        ("particulate", "particulate"),
        ("porous", "porous"),
        ("open pores", "open pores"),
        ("closed pores", "closed pores"),
        ("without pores", "without pores"),
        ("other", "other"),
        ("unknown", "unknown")
)

LAYER_MATERIALS_MIXING = (
        ("single material", "single material"),
        ("homogeneous mixing", "homogeneous mixing"),
        ("heterogeneous mixing", "heterogeneous mixing"),
        ("grains in fluid", "grains in fluid"),
        ("fluid in porous solid", "fluid in porous solid"),
        ("spatial distribution", "spatial distribution")
)

# Experiment forms
# -------------------------------------------------------------------

class ExperimentSpectra(forms.Form):
    spectrum_x_import_mode = forms.ChoiceField(choices=SPECTRUM_IMPORT_MODE, required=False, label="Import Mode")
    spectrum_x_uid = forms.CharField(required=False, label="UID", widget= forms.TextInput
                           (attrs={'auto_fill': 'False',
                                   'placeholder': 'SPECTRUM_AB_yyyymmdd_123'}))
    spectrum_x_experiment_type = forms.ChoiceField(choices=TYPES_CHOICES, required=False, label="Experiment Type")
    spectrum_x_chronologically_ordered = forms.ChoiceField(choices=SPECTRUM_EXPERIMENT_TYPE, required=False, label="Chronologically Ordered")
    spectrum_x_previous_spectrum_uid = forms.CharField(required=False, label="Previous Spectrum UID")
    spectrum_x_title = forms.CharField(required=False, label="Title")
    spectrum_x_type = forms.ChoiceField(choices=SPECTRUM_TYPE, required=False, label="Type")
    spectrum_x_intensity_unit = forms.ChoiceField(choices=SPECTRUM_INTENSITY_UNIT, required=False, label="Intensity Unit")
    spectrum_x_reference_position = forms.CharField(required=False, label="Reference Position")
    reference_spectra_x_spectrum_uid = forms.CharField(required=False, label="Reference spectra - Spectrum UID", widget= forms.TextInput
                           (attrs={'auto_fill': 'False',
                                   'placeholder': 'SPECTRUM_AB_yyyymmdd_123'}))
    spectrum_x_model_parameters = forms.CharField(required=False, label="Model Parameters")
    sample_x_uid = forms.CharField(required=False, label="UID")
    sample_x_changes = forms.CharField(required=False, label="Changes")
    sample_x_comments = forms.CharField(required=False, label="Comments")
    primary_constituent_x_constituent_uid = forms.CharField(required=False, label="Constituent UID", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    primary_constituent_x_constituent_comments = forms.CharField(required=False, label="Constituent Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    # spectrum_ added to this to differenciate between the two parameters instrument
    spectrum_parameters_instrument_x_instrument_uid = forms.ChoiceField(choices=PARAMETERS_INSTRUMENTS, required=False, label="Instrument UID")
    spectrum_range_x_spectrum_min = forms.CharField(required=False, label="Min")
    spectrum_range_x_spectrum_max = forms.CharField(required=False, label="Max")
    spectrum_x_date_begin = forms.CharField(required=False, label="Date Begin", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    spectrum_x_time_begin = forms.CharField(required=False, label="Time Begin")
    spectrum_x_date_end = forms.CharField(required=False, label="Date End")
    spectrum_x_time_end = forms.CharField(required=False, label="Time End")
    previous_version_x_status = forms.CharField(required=False, label="Status")
    previous_version_x_comments = forms.CharField(required=False, label="Comments")
    previous_version_x_new_spectrum_uid = forms.CharField(required=False, label="New Spectrum UID")
    spectrum_x_history = forms.CharField(required=False, label="History", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    spectrum_x_analysis = forms.CharField(required=False, label="Analysis", widget= forms.TextInput
                           (attrs={'auto_fill': 'The background is corrected with a polynomial baseline. The peak of higher intensity is normalized to 1.',
                                   'placeholder': 'The background is corrected with a polynomial baseline. The peak of higher intensity is normalized to 1.'}))
    spectrum_x_quality_flag = forms.ChoiceField(required=False, choices=SPECTRUM_QUALITY_FLAG)
    # default EXPER_Gilles_Montagnac
    spectrum_validators_x_spectrum_experimentalist_uid = forms.CharField(required=False, label="Experimentalist UID")
    spectrum_x_comments = forms.CharField(required=False, label="Comments")
    spectrum_publications_x_publication_uid = forms.CharField(required=False, label="Publication UID")
    spectrum_x_publication_comments = forms.CharField(required=False, label="Publication Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    parameter_x_type = forms.ChoiceField(choices=PARAMETER_TYPE, required=False, label="Type")
    parameter_x_format = forms.ChoiceField(choices=PARAMTER_FORMAT, required=False, label="Format")
    # default 0
    parameter_x_header_lines_number = forms.CharField(required=False, label="Header Lines Number")
    # default LGL_raman_532nm_{{name of sample}}
    file_x_filename = forms.CharField(required=False, label="Filename")
    spectrum_x_export_filename = forms.CharField(required=False, label="Export Filename")
    experiment_x_preview_flag = forms.ChoiceField(choices=SPECTRUM_EXPERIMENT_TYPE, required=False, label="Flag")

    band_x_position_min = forms.CharField(required=False, label="Position Min")
    band_x_position_peak = forms.CharField(required=False, label="Position Peak")
    band_x_position_max = forms.CharField(required=False, label="Position Max")
    band_x_peak_intensity_relative = forms.CharField(required=False, label="Peak Intensity relative")
    # placeholder ‘CONST_AB_yyyymmdd_123’
    band_x_primary_constituent_uid = forms.CharField(required=False, label="Primary Constituent UID")
    band_x_primary_specie_uid = forms.CharField(required=False, label="Primary Specie UID")
    transition_chemical_bonds_x_chemical_bond_uid = forms.CharField(required=False, label="Chemical Bond UID")
    band_x_transition_assignment = forms.CharField(required=False, label="Transition Assignment")
    band_x_vibration_mode = forms.ChoiceField(choices=VIBRATION_MODE, required=False, label="Vibration Mode")
    band_x_rotation_mode = forms.ChoiceField(choices=ROTATION_MODE, required=False, label="Rotation Mode")
    band_x_phonon_mode = forms.ChoiceField(choices=PHONON_MODE, required=False, label="Phonon Mode")
    band_x_label = forms.CharField(required=False, label="Label")
    band_x_comments = forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
        
    def __init__(self, *args, **kwargs):
        session = kwargs.pop('session', 0)
        array = []
        spectrum_section_array = []
        spectrum_uid_array = []
        primary_constituent_array = []
        spectrum_parameter_range_array = []
        spectrum_parameter_instrument_array = []
        spectrum_experimentalist_uid_array = []
        publication_uid_array = []
        chemical_bonds_array = []
        spectrum_band_array = []

        spectrum_section_counter = 0
        spectrum_uid_counter = 0
        primary_constituent_counter = 0
        spectrum_parameter_range_counter = 0
        spectrum_parameter_instrument_counter = 0
        spectrum_experimentalist_uid_counter = 0
        publication_uid_counter = 0
        chemical_bonds_counter = 0
        spectrum_band_counter = 0

        if session != 0:
                for i in session:
                        array.append(i)
                for a in array:
                        if a.count('spectrumSection') > 0:
                                spectrum_section_counter += 1
                                spectrum_section_array.append(a)
                        elif a.count('spectrum_uid') > 0:
                                spectrum_uid_counter += 1
                                spectrum_uid_array.append(a)
                        elif a.count('primaryConstituent') > 0:
                                primary_constituent_counter += 1
                                primary_constituent_array.append(a)
                        elif a.count('spectrum_parameter_range') > 0:
                                spectrum_parameter_range_counter += 1
                                spectrum_parameter_range_array.append(a)
                        elif a.count('spectrum_parameter_instrument') > 0:
                                spectrum_parameter_instrument_counter += 1
                                spectrum_parameter_instrument_array.append(a)
                        elif a.count('spectrumExperimentalistUID') > 0:
                                spectrum_experimentalist_uid_counter += 1
                                spectrum_experimentalist_uid_array.append(a)
                        elif a.count('publicationUID') > 0:
                                publication_uid_counter += 1
                                publication_uid_array.append(a)
                        elif a.count('chemicalBondsUID') > 0:
                                chemical_bonds_counter += 1
                                chemical_bonds_array.append(a)
                        elif a.count('spectrumBand') > 0:
                                spectrum_band_counter += 1
                                spectrum_band_array.append(a)
        
        super(ExperimentSpectra, self).__init__(*args, **kwargs)  
        for a in spectrum_band_array:
                index = a[12:]
                self.fields[f'band_x_position_min{index}'] = \
                        forms.CharField(required=False, label="Position Min")
                self.fields[f'band_x_position_peak{index}'] = \
                        forms.CharField(required=False, label="Position Peak")
                self.fields[f'band_x_position_max{index}'] = \
                        forms.CharField(required=False, label="Position Max")
                self.fields[f'band_x_peak_intensity_relative{index}'] = \
                        forms.CharField(required=False, label="Peak Intensity relative")
                self.fields[f'band_x_primary_constituent_uid{index}'] = \
                        forms.CharField(required=False, label="Primary Constituent UID")
                self.fields[f'band_x_primary_specie_uid{index}'] = \
                        forms.CharField(required=False, label="Primary Specie UID")
                self.fields[f'transition_chemical_bonds_x_chemical_bond_uid{index}'] = \
                        forms.CharField(required=False, label="Chemical Bond UID")
                self.fields[f'band_x_transition_assignment{index}'] = \
                        forms.CharField(required=False, label="Transition Assignment")
                self.fields[f'band_x_vibration_mode{index}'] = \
                        forms.ChoiceField(choices=VIBRATION_MODE, required=False, label="Vibration Mode")
                self.fields[f'band_x_rotation_mode{index}'] = \
                        forms.ChoiceField(choices=ROTATION_MODE, required=False, label="Rotation Mode")
                self.fields[f'band_x_phonon_mode{index}'] = \
                        forms.ChoiceField(choices=PHONON_MODE, required=False, label="Phonon Mode")
                self.fields[f'band_x_label{index}'] = \
                        forms.CharField(required=False, label="Label")
                self.fields[f'band_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))

        for a in chemical_bonds_array:
                index = a[16:]
                self.fields[f'transition_chemical_bonds_x_chemical_bond_uid{index}'] = \
                        forms.CharField(required=False, label="Chemical Bond UID")

        for a in publication_uid_array:
                index = a[14:]
                self.fields[f'spectrum_publications_x_publication_uid{index}'] = \
                        forms.CharField(required=False, label="Publication UID")

        for a in spectrum_experimentalist_uid_array:
                index = a[26:]
                self.fields[f'spectrum_validators_x_spectrum_experimentalist_uid{index}'] = \
                        forms.CharField(required=False, label="Experimentalist UID")

        for a in spectrum_parameter_instrument_array:
                index = a[29:]
                self.fields[f'spectrum_parameters_instrument_x_instrument_uid{index}'] = \
                        forms.ChoiceField(choices=PARAMETERS_INSTRUMENTS, required=False, label="Instrument UID")
                self.fields[f'spectrum_range_x_min{index}'] = \
                        forms.CharField(required=False, label="Min")
                self.fields[f'spectrum_range_x_max{index}'] = \
                        forms.CharField(required=False, label="Max")

        for a in spectrum_parameter_range_array:
                index = a[24:]
                self.fields[f'spectrum_range_x_spectrum_min{index}'] = \
                        forms.CharField(required=False, label="Min")
                self.fields[f'spectrum_range_x_spectrum_max{index}'] = \
                        forms.CharField(required=False, label="Max")

        for a in primary_constituent_array:
                index = a[18:]
                self.fields[f'primary_constituent_x_constituent_uid{index}'] = \
                        forms.CharField(required=False, label="Constituent UID", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'primary_constituent_x_constituent_comments{index}'] = \
                        forms.CharField(required=False, label="Constituent Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
        
        for a in spectrum_uid_array:
                index = a[12:]
                self.fields[f'reference_spectra_x_spectrum_uid{index}'] = \
                        forms.CharField(required=False, label="Reference spectra - Spectrum UID", widget= forms.TextInput
                           (attrs={'auto_fill': 'False',
                                   'placeholder': 'SPECTRUM_AB_yyyymmdd_123'}))

        for a in spectrum_section_array:
                index = a[15:]
                self.fields[f'spectrum_x_import_mode{index}'] = \
                        forms.ChoiceField(choices=SPECTRUM_IMPORT_MODE, required=False, label="Import Mode")
                self.fields[f'spectrum_x_uid{index}'] = \
                        forms.CharField(required=False, label="UID")
                self.fields[f'spectrum_x_experiment_type{index}'] = \
                        forms.ChoiceField(choices=TYPES_CHOICES, required=False, label="Experiment Type")
                self.fields[f'spectrum_x_chronologically_ordered{index}'] = \
                        forms.ChoiceField(choices=SPECTRUM_EXPERIMENT_TYPE, required=False, label="Chronologically Ordered")
                self.fields[f'spectrum_x_previous_spectrum_uid{index}'] = \
                        forms.CharField(required=False, label="Previous Spectrum UID")
                self.fields[f'spectrum_x_title{index}'] = \
                        forms.CharField(required=False, label="Title")
                self.fields[f'spectrum_x_type{index}'] = \
                        forms.ChoiceField(choices=SPECTRUM_TYPE, required=False, label="Type")
                self.fields[f'spectrum_x_intensity_unit{index}'] = \
                        forms.ChoiceField(choices=SPECTRUM_INTENSITY_UNIT, required=False, label="Intensity Unit")
                self.fields[f'spectrum_x_reference_position{index}'] = \
                        forms.CharField(required=False, label="Reference Position")
                self.fields[f'spectrum_x_model_parameters{index}'] = \
                        forms.CharField(required=False, label="Model Parameters")
                self.fields[f'sample_x_uid{index}'] = \
                        forms.CharField(required=False, label="UID")
                self.fields[f'sample_x_changes{index}'] = \
                        forms.CharField(required=False, label="Changes")
                self.fields[f'sample_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments")
                self.fields[f'primary_constituent_x_constituent_uid{index}'] = \
                        forms.CharField(required=False, label="Constituent UID", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'primary_constituent_x_constituent_comments{index}'] = \
                        forms.CharField(required=False, label="Constituent Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'spectrum_parameters_instrument_x_instrument_uid{index}'] = \
                        forms.CharField(required=False, label="Instrument UID", widget= forms.TextInput
                           (attrs={'placeholder': 'INSTRU_InstrumentName_Technique_LabAcronym'}))
                self.fields[f'spectrum_range_x_spectrum_min{index}'] = \
                        forms.CharField(required=False, label="Min")
                self.fields[f'spectrum_range_x_spectrum_max{index}'] = \
                        forms.CharField(required=False, label="Max")
                self.fields[f'spectrum_x_date_begin{index}'] = \
                        forms.CharField(required=False, label="Date Begin", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'spectrum_x_time_begin{index}'] = \
                        forms.CharField(required=False, label="Time Begin")
                self.fields[f'spectrum_x_date_end{index}'] = \
                        forms.CharField(required=False, label="Date End")
                self.fields[f'spectrum_x_time_end{index}'] = \
                        forms.CharField(required=False, label="Time End")
                self.fields[f'previous_version_x_status{index}'] = \
                        forms.CharField(required=False, label="Status")
                self.fields[f'previous_version_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments")
                self.fields[f'previous_version_x_new_spectrum_uid{index}'] = \
                        forms.CharField(required=False, label="New Spectrum UID")
                self.fields[f'spectrum_x_history{index}'] = \
                        forms.CharField(required=False, label="History", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'spectrum_x_analysis{index}'] = \
                        forms.CharField(required=False, label="Analysis")
                self.fields[f'spectrum_x_quality_flag{index}'] = \
                        forms.ChoiceField(required=False, choices=SPECTRUM_QUALITY_FLAG)
                self.fields[f'spectrum_validators_x_spectrum_experimentalist_uid{index}'] = \
                        forms.CharField(required=False, label="Experimentalist UID")
                self.fields[f'spectrum_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments")
                self.fields[f'spectrum_publications_x_publication_uid{index}'] = \
                        forms.CharField(required=False, label="Publication UID")
                self.fields[f'spectrum_x_publication_comments{index}'] = \
                        forms.CharField(required=False, label="Publication Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'parameter_x_type{index}'] = \
                        forms.ChoiceField(choices=PARAMETER_TYPE, required=False, label="Type")
                self.fields[f'parameter_x_format{index}'] = \
                        forms.ChoiceField(choices=PARAMTER_FORMAT, required=False, label="Format")
                self.fields[f'parameter_x_header_lines_number{index}'] = \
                        forms.CharField(required=False, label="Header Lines Number")
                self.fields[f'file_x_filename{index}'] = \
                        forms.CharField(required=False, label="Filename")
                self.fields[f'spectrum_x_export_filename{index}'] = \
                        forms.CharField(required=False, label="Export Filename")
                self.fields[f'experiment_x_preview_flag{index}'] = \
                        forms.ChoiceField(choices=SPECTRUM_EXPERIMENT_TYPE, required=False, label="Flag")
                self.fields[f'band_x_position_min{index}'] = \
                        forms.CharField(required=False, label="Position Min")
                self.fields[f'band_x_position_peak{index}'] = \
                        forms.CharField(required=False, label="Position Peak")
                self.fields[f'band_x_position_max{index}'] = \
                        forms.CharField(required=False, label="Position Max")
                self.fields[f'band_x_peak_intensity_relative{index}'] = \
                        forms.CharField(required=False, label="Peak Intensity relative")
                self.fields[f'band_x_primary_constituent_uid{index}'] = \
                        forms.CharField(required=False, label="Primary Constituent UID")
                self.fields[f'band_x_primary_specie_uid{index}'] = \
                        forms.CharField(required=False, label="Primary Specie UID")
                self.fields[f'transition_chemical_bonds_x_chemical_bond_uid{index}'] = \
                        forms.CharField(required=False, label="Chemical Bond UID")
                self.fields[f'band_x_transition_assignment{index}'] = \
                        forms.CharField(required=False, label="Transition Assignment")
                self.fields[f'band_x_vibration_mode{index}'] = \
                        forms.ChoiceField(choices=VIBRATION_MODE, required=False, label="Vibration Mode")
                self.fields[f'band_x_rotation_mode{index}'] = \
                        forms.ChoiceField(choices=ROTATION_MODE, required=False, label="Rotation Mode")
                self.fields[f'band_x_phonon_mode{index}'] = \
                        forms.ChoiceField(choices=PHONON_MODE, required=False, label="Phonon Mode")
                self.fields[f'band_x_label{index}'] = \
                        forms.CharField(required=False, label="Label")
                self.fields[f'band_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                

class ExperimentParameterInstrument(forms.Form):
        parameters_instrument_x_instrument_uid = forms.ChoiceField(choices=PARAMETERS_INSTRUMENTS, required=False, label="Instrument UID")
        parameters_instrument_x_instrument_carrier = forms.CharField(required=False, label="Instrument Carrier")
        parameters_instrument_x_instrument_sample_holder = forms.CharField(required=False, label="Instrument Sample Holder")
        parameters_instrument_x_spectrum_scan_number = forms.CharField(required=False, label="Spectrum Scan Number")
        spectral_x_unit = forms.ChoiceField(choices=SPECTRAL_UNIT, required=False, label="Unit")
        spectral_x_standard = forms.ChoiceField(choices=SPECTRAL_STANDARD, required=False, label="Standard")
        spectral_x_observation_mode = forms.ChoiceField(choices=SPECTRAL_OBERSATION_MODE, required=False, label="Observation Mode")
        spectral_x_comments = forms.CharField(required=False, label="Comments")
        angle_x_observation_geometry = forms.ChoiceField(choices=ANGLE_OBSERVATION_GEOMETRY, required=False)
        angle_x_observation_mode = forms.ChoiceField(choices=ANGLE_OBSERVATION_MODE, required=False)
        range_types_x_type = forms.ChoiceField(choices=RANGE_TYPE, required=False, label="Type")
        range_x_min = forms.CharField(required=False, label="Min")
        range_x_max = forms.CharField(required=False, label="Max")
        range_x_absorption_edge_element_uid = forms.CharField(required=False, label="Absorption Edge Element UID")
        range_x_absorption_edge_type = forms.CharField(required=False, label="Absorption Edge type")
        range_x_sampling = forms.CharField(required=False, label="Sampling")
        range_x_resolution = forms.CharField(required=False, label="Resolution")
        range_x_position_error = forms.CharField(required=False, label="Position Error")
        filter_x_type = forms.CharField(required=False, label="Type", widget= forms.TextInput
                                        (attrs={'auto_fill': 'Edge Filter',
                                                'placeholder': 'Edge Filter'}))
        filter_x_place = forms.CharField(required=False, label="Place")
        filter_x_center = forms.CharField(required=False, label="Center", widget= forms.TextInput
                                (attrs={'auto_fill': 'NULL',
                                        'placeholder': 'NULL'}))
        filter_x_width = forms.CharField(required=False, label="Width", widget= forms.TextInput
                                (attrs={'auto_fill': 'NULL',
                                        'placeholder': 'NULL'}))
        angle_x_incidence = forms.CharField(required=False, label="Incidence", widget= forms.TextInput
                                (attrs={'auto_fill': 'NULL',
                                        'placeholder': 'NULL'}))
        angle_x_emergence = forms.CharField(required=False, label="Emergence", widget= forms.TextInput
                                (attrs={'auto_fill': 'NULL',
                                        'placeholder': 'NULL'}))
        angle_x_azimuth = forms.CharField(required=False, label="Azimuth", widget= forms.TextInput
                                (attrs={'auto_fill': 'NULL',
                                        'placeholder': 'NULL'}))
        angle_x_phase = forms.CharField(required=False, label="Phase",)
        angle_x_resolution_illumination = forms.CharField(required=False, label="Resolution Illumination", widget= forms.TextInput
                                (attrs={'auto_fill': 'NULL',
                                        'placeholder': 'NULL'}))
        angle_x_resolution_observation = forms.CharField(required=False, label="Resolution Observation", widget= forms.TextInput
                                (attrs={'auto_fill': 'NULL',
                                        'placeholder': 'NULL'}))
        angle_x_comments = forms.CharField(required=False, label="Comments",)
        polarization_x_type_illumination = forms.ChoiceField(label="Type Illumination", choices=POLARIZATION_TYPE_ILLUMINATION, required=False)
        polarization_x_type_observation = forms.ChoiceField(label="Type Observation", choices=POLARIZATION_TYPE_ILLUMINATION, required=False)
        polarization_x_polarizer_illumination = forms.CharField(label="Polarizer Illumination", required=False)
        polarization_x_polarizer_observation = forms.CharField(label="Polarizer Observation", required=False)
        polarization_x_rejection_illumination = forms.CharField(label="Rejection Illumination", required=False)
        polarization_x_rejection_observation = forms.CharField(label="Rejection Observation", required=False)
        polarization_x_angle_illumination = forms.CharField(label="Angle Illumination", required=False)
        polarization_x_angle_observation = forms.CharField(label="Angle Observation", required=False)
        polarization_x_comments = forms.CharField(label="Comments", required=False)
        spatial_x_observation_mode = forms.ChoiceField(label="Observation Mode", required=False, choices=SPATIAL_OBSERVATION_MODE)
        spatial_x_unit = forms.ChoiceField(label="Unit", choices=SPATIAL_UNIT, required=False)
        spatial_x_objective = forms.ChoiceField(required=False, choices=SPATIAL_OBJECTIVE)
        spatial_x_spots_number = forms.CharField(required=False, label="Spots Number")
        spatial_x_sampling_x = forms.CharField(required=False, label="Sampling X")
        spatial_x_sampling_y = forms.CharField(required=False, label="Sampling Y")
        spatial_x_measures_x = forms.CharField(required=False, label="Measures X")
        spatial_x_measures_y = forms.CharField(required=False, label="Measures Y")
        spatial_x_extent_x = forms.CharField(required=False, label="Extent X")
        spatial_x_extent_y = forms.CharField(required=False, label="Extent Y")
        resolution_x_width = forms.CharField(required=False, label="Width", widget= forms.TextInput
                                (attrs={'auto_fill': '1',
                                        'placeholder': '1'}))
        resolution_x_width_error = forms.CharField(required=False, label="Width Error")  
        resolution_x_position = forms.CharField(required=False, label="Position")  
        spatial_x_comments = forms.CharField(required=False, label="Comments")

        def __init__(self, *args, **kwargs):
                session = kwargs.pop('session', 0)
                array = []
                p_i_type_range_array = []
                p_i_range_array = []
                p_i_filter_array = []
                p_i_resolution_array = []
                parameter_instrument_array = []

                p_i_type_range_counter = 0
                p_i_range_counter = 0
                p_i_filter_counter = 0
                p_i_resolution_counter = 0
                parameter_instrument_counter = 0

                if session != 0:
                        for i in session:
                                array.append(i)
                        for a in array:
                                if a.count('p_i_type_range') > 0:
                                        p_i_type_range_counter += 1
                                        p_i_type_range_array.append(a)
                                elif a.count('p_i_range') > 0:
                                        p_i_range_counter += 1
                                        p_i_range_array.append(a)
                                elif a.count('p_i_filter') > 0:
                                        p_i_filter_counter += 1
                                        p_i_filter_array.append(a)
                                elif a.count('p_i_resolution') > 0:
                                        p_i_resolution_counter += 1
                                        p_i_resolution_array.append(a)
                                elif a.count('parameter_instrument') > 0:
                                        parameter_instrument_counter += 1
                                        parameter_instrument_array.append(a)

                        
                super(ExperimentParameterInstrument, self).__init__(*args, **kwargs)

                for a in p_i_resolution_array:
                        index = a[14:]
                        self.fields[f'resolution_x_width{index}'] = \
                                forms.CharField(required=False, label="Width", widget= forms.TextInput
                                (attrs={'auto_fill': '1',
                                        'placeholder': '1'}))
                        self.fields[f'resolution_x_width_error{index}'] = \
                                forms.CharField(required=False, label="Width Error") 
                        self.fields[f'resolution_x_position{index}'] = \
                                forms.CharField(required=False, label="Position")

                for a in p_i_filter_array:
                        index = a[10:]
                        self.fields[f'filter_x_type{index}'] = \
                                forms.CharField(required=False, label="Type", widget= forms.TextInput
                                        (attrs={'auto_fill': 'Edge Filter',
                                                'placeholder': 'Edge Filter'}))
                        self.fields[f'filter_x_place{index}'] = \
                                forms.CharField(required=False, label="Place")
                        self.fields[f'filter_x_center{index}'] = \
                                forms.CharField(required=False, label="Center", widget= forms.TextInput
                                (attrs={'auto_fill': 'NULL',
                                        'placeholder': 'NULL'}))
                        self.fields[f'filter_x_width{index}'] = \
                                forms.CharField(required=False, label="Width", widget= forms.TextInput
                                (attrs={'auto_fill': 'NULL',
                                        'placeholder': 'NULL'}))

                for a in p_i_range_array:
                        index = a[9:]
                        self.fields[f'range_x_min{index}'] = \
                                forms.CharField(required=False, label="Min")
                        self.fields[f'range_x_max{index}'] = \
                                forms.CharField(required=False, label="Max")
                        self.fields[f'range_x_absorption_edge_element_uid{index}'] = \
                                forms.CharField(required=False, label="Absorption Edge Element UID")
                        self.fields[f'range_x_absorption_edge_type{index}'] = \
                                forms.CharField(required=False, label="Absorption Edge type")
                        self.fields[f'range_x_sampling{index}'] = \
                                forms.CharField(required=False, label="Sampling")
                        self.fields[f'range_x_resolution{index}'] = \
                                forms.CharField(required=False, label="Resolution")
                        self.fields[f'range_x_position_error{index}'] = \
                                forms.CharField(required=False, label="Position Error")

                for a in p_i_type_range_array:
                        index = a[14:]
                        self.fields[f'range_types_x_type{index}'] = \
                                forms.ChoiceField(choices=RANGE_TYPE, required=False, label="Type")
                
                # correct all to True
                for a in parameter_instrument_array:
                        index = a[20:]
                        self.fields[f'parameters_instrument_x_instrument_uid{index}'] = \
                                forms.ChoiceField(choices=PARAMETERS_INSTRUMENTS, required=False, label="Instrument UID")
                        self.fields[f'parameters_instrument_x_instrument_carrier{index}'] = \
                                forms.CharField(required=False, label="Instrument Carrier")
                        self.fields[f'parameters_instrument_x_instrument_sample_holder{index}'] = \
                                forms.CharField(required=False, label="Instrument Sample Holder")
                        self.fields[f'parameters_instrument_x_spectrum_scan_number{index}'] = \
                                forms.CharField(required=False, label="Spectrum Scan Number")
                        self.fields[f'spectral_x_unit{index}'] = \
                                forms.ChoiceField(choices=SPECTRAL_UNIT, required=False, label="Unit")
                        self.fields[f'spectral_x_standard{index}'] = \
                                forms.ChoiceField(choices=SPECTRAL_STANDARD, required=False, label="Standard")
                        self.fields[f'spectral_x_observation_mode{index}'] = \
                                forms.ChoiceField(choices=SPECTRAL_OBERSATION_MODE, required=False, label="Observation Mode")
                        self.fields[f'spectral_x_comments{index}'] = \
                                forms.CharField(required=False, label="Comments")
                        self.fields[f'angle_x_observation_geometry{index}'] = \
                                forms.ChoiceField(choices=ANGLE_OBSERVATION_GEOMETRY, required=False)
                        self.fields[f'angle_x_observation_mode{index}'] = \
                                forms.ChoiceField(choices=ANGLE_OBSERVATION_MODE, required=False)
                        self.fields[f'spectral_x_observation_mode{index}'] = \
                                forms.ChoiceField(choices=SPECTRAL_OBERSATION_MODE, required=False, label="Observation Mode")
                        self.fields[f'range_types_x_type{index}'] = \
                                forms.ChoiceField(choices=RANGE_TYPE, required=False, label="Type")
                        self.fields[f'range_x_min{index}'] = \
                                forms.CharField(required=False, label="Min")
                        self.fields[f'range_x_max{index}'] = \
                                forms.CharField(required=False, label="Max")
                        self.fields[f'range_x_absorption_edge_element_uid{index}'] = \
                                forms.CharField(required=False, label="Absorption Edge Element UID")
                        self.fields[f'range_x_absorption_edge_type{index}'] = \
                                forms.CharField(required=False, label="Absorption Edge type")
                        self.fields[f'range_x_sampling{index}'] = \
                                forms.CharField(required=False, label="Sampling")
                        self.fields[f'range_x_resolution{index}'] = \
                                forms.CharField(required=False, label="Resolution")
                        self.fields[f'range_x_position_error{index}'] = \
                                forms.CharField(required=False, label="Position Error")
                        self.fields[f'filter_x_type{index}'] = \
                                forms.CharField(required=False, label="Type", widget= forms.TextInput
                                        (attrs={'auto_fill': 'Edge Filter',
                                                'placeholder': 'Edge Filter'}))
                        self.fields[f'filter_x_place{index}'] = \
                                forms.CharField(required=False, label="Place")
                        self.fields[f'filter_x_center{index}'] = \
                                forms.CharField(required=False, label="Center")
                        self.fields[f'filter_x_width{index}'] = \
                                forms.CharField(required=False, label="Width")
                        self.fields[f'angle_x_incidence{index}'] = \
                                forms.CharField(required=False, label="Incidence", widget= forms.TextInput
                                        (attrs={'auto_fill': 'NULL',
                                                'placeholder': 'NULL'}))
                        self.fields[f'angle_x_emergence{index}'] = \
                                forms.CharField(required=False, label="Emergence", widget= forms.TextInput
                                        (attrs={'auto_fill': 'NULL',
                                                'placeholder': 'NULL'}))
                        self.fields[f'angle_x_azimuth{index}'] = \
                                forms.CharField(required=False, label="Azimuth", widget= forms.TextInput
                                        (attrs={'auto_fill': 'NULL',
                                                'placeholder': 'NULL'}))
                        self.fields[f'angle_x_phase{index}'] = \
                                forms.CharField(required=False, label="Phase",)
                        self.fields[f'angle_x_resolution_illumination{index}'] = \
                                forms.CharField(required=False, label="Resolution Illumination", widget= forms.TextInput
                                        (attrs={'auto_fill': 'NULL',
                                                'placeholder': 'NULL'}))
                        self.fields[f'angle_x_resolution_observation{index}'] = \
                                forms.CharField(required=False, label="Resolution Observation", widget= forms.TextInput
                                        (attrs={'auto_fill': 'NULL',
                                                'placeholder': 'NULL'}))
                        self.fields[f'angle_x_comments{index}'] = \
                                forms.CharField(required=False, label="Comments",)
                        self.fields[f'polarization_x_type_illumination{index}'] = \
                                forms.ChoiceField(label="Type Illumination", choices=POLARIZATION_TYPE_ILLUMINATION, required=False)
                        self.fields[f'polarization_x_type_observation{index}'] = \
                                forms.ChoiceField(label="Type Observation", choices=POLARIZATION_TYPE_ILLUMINATION, required=False)
                        self.fields[f'polarization_x_polarizer_illumination{index}'] = \
                                forms.CharField(label="Polarizer Illumination", required=False)
                        self.fields[f'polarization_x_polarizer_observation{index}'] = \
                                forms.CharField(label="Polarizer Observation", required=False)
                        self.fields[f'polarization_x_rejection_illumination{index}'] = \
                                forms.CharField(label="Rejection Illumination", required=False)
                        self.fields[f'polarization_x_rejection_observation{index}'] = \
                                forms.CharField(label="Rejection Observation", required=False)
                        self.fields[f'polarization_x_angle_illumination{index}'] = \
                                forms.CharField(label="Angle Illumination", required=False)
                        self.fields[f'polarization_x_angle_observation{index}'] = \
                                forms.CharField(label="Angle Observation", required=False)
                        self.fields[f'polarization_x_comments{index}'] = \
                                forms.CharField(label="Comments", required=False)
                        self.fields[f'spatial_x_observation_mode{index}'] = \
                                forms.ChoiceField(label="Observation Mode", required=False, choices=SPATIAL_OBSERVATION_MODE)
                        self.fields[f'spatial_x_unit{index}'] = \
                                forms.ChoiceField(label="Unit", choices=SPATIAL_UNIT, required=False)
                        self.fields[f'spatial_x_objective{index}'] = \
                                forms.ChoiceField(required=False, choices=SPATIAL_OBJECTIVE)
                        self.fields[f'spatial_x_spots_number{index}'] = \
                                forms.CharField(required=False, label="Spots Number")
                        self.fields[f'spatial_x_sampling_x{index}'] = \
                                forms.CharField(required=False, label="Sampling X")
                        self.fields[f'spatial_x_sampling_y{index}'] = \
                                forms.CharField(required=False, label="Sampling X")
                        self.fields[f'spatial_x_sampling_y{index}'] = \
                                forms.CharField(required=False, label="Sampling Y")
                        self.fields[f'spatial_x_measures_x{index}'] = \
                                forms.CharField(required=False, label="Measures X")
                        self.fields[f'spatial_x_measures_y{index}'] = \
                                forms.CharField(required=False, label="Measures Y")
                        self.fields[f'spatial_x_extent_x{index}'] = \
                                forms.CharField(required=False, label="Extent X")
                        self.fields[f'spatial_x_extent_y{index}'] = \
                                forms.CharField(required=False, label="Extent Y")
                        self.fields[f'resolution_x_width{index}'] = \
                                forms.CharField(required=False, label="Width")
                        self.fields[f'resolution_x_width_error{index}'] = \
                                forms.CharField(required=False, label="Width Error") 
                        self.fields[f'resolution_x_position{index}'] = \
                                forms.CharField(required=False, label="Position") 
                        self.fields[f'spatial_x_comments{index}'] = \
                                        forms.CharField(required=False, label="Comments")


class ExperimentIntro(forms.Form):
        experiment_x_import_mode = forms.ChoiceField(required=False, choices=IMPORT_MODE_CHOICES, label="Import Mode")
        # correct to True
        experiment_x_uid = forms.CharField(required=False, label="Experiment UID")
        # correct to True
        owner_databases_x_database_uid = forms.CharField(required=False, label="Owner Databases", widget= forms.TextInput
                                (attrs={'auto_fill': 'DB_REAP',
                                        'placeholder': 'DB_REAP'}))
        # correct to True
        experimentalists_x_experimentalist_uid = forms.CharField(required=False, label="Experimentalist UID")
        # correct to True
        types_x_type = forms.ChoiceField(required=False, choices=TYPES_CHOICES, label="Types type")
        # correct to True
        experiment_x_title = forms.CharField(required=False, label="Title")
        # correct to True
        experiment_x_description = forms.CharField(required=False, label="Description", widget= forms.TextInput
                                (attrs={'auto_fill': '<![CDATA[]]>',
                                        'placeholder': '<![CDATA[]]>'}))
        # correct to True
        experiment_x_date_begin = forms.CharField(required=False, label="Date Begin", widget= forms.TextInput
                                (attrs={'placeholder': 'YYYY-MM-DD'}))
        experiment_x_date_end = forms.CharField(required=False, label="Date End", widget= forms.TextInput
                                (attrs={'placeholder': 'YYYY-MM-DD'}))
        experiment_x_parent_experiment_uid = forms.CharField(required=False, label="Parent Experiment UID")
        experiment_x_laboratory_uid = forms.CharField(required=False, label="Laboratory UID", widget= forms.TextInput
                                (attrs={'placeholder': 'only for laboratory experiments and calculations'}))
        variable_parameters_types_x_variable_parameters_type = forms.ChoiceField(choices=VARIABLE_PARAMETERS_TYPE, label="Variable Parameter Types", required=False)
        experiment_x_variable_parameters_comments = forms.CharField(required=False, label="Parameter Comments")

        def __init__(self, *args, **kwargs):
                session = kwargs.pop('session', 0)
                array = []
                database_uid_array = []
                experimentalist_uid_array = []
                types_type_array = []
                parameter_types_parameter_type_array = []

                database_uid_counter = 0
                experimentalist_uid_counter = 0
                types_type_counter = 0
                parameter_types_parameter_type_counter = 0

                if session != 0:
                        for i in session:
                                array.append(i)
                        for a in array:
                                if a.count('database_uid') > 0:
                                        database_uid_counter += 1
                                        database_uid_array.append(a)
                                elif a.count('experimentalist_uid') > 0:
                                        experimentalist_uid_counter += 1
                                        experimentalist_uid_array.append(a)
                                elif a.count('types_type') > 0:
                                        types_type_counter += 1
                                        types_type_array.append(a)
                                elif a.count('parameter_types_parameter_type') > 0:
                                        parameter_types_parameter_type_counter += 1
                                        parameter_types_parameter_type_array.append(a)
                
                super(ExperimentIntro, self).__init__(*args, **kwargs)
                # correct all to True
                for a in database_uid_array:
                        index = a[12:]
                        self.fields[f'owner_databases_x_database_uid{index}'] = \
                        forms.CharField(required=False, label="Owner Databases", widget= forms.TextInput
                                (attrs={'auto_fill': 'DB_REAP',
                                        'placeholder': 'DB_REAP'}))
                for a in experimentalist_uid_array:
                        index = a[19:]
                        self.fields[f'experimentalists_x_experimentalist_uid{index}'] = \
                                forms.CharField(required=False, label="Experimentalist UID")
                for a in types_type_array:
                    index = a[10:]
                    self.fields[f'types_x_type{index}'] = \
                        forms.ChoiceField(
                        required=False, choices=TYPES_CHOICES, label="Types type")
                for a in parameter_types_parameter_type_array:
                        index = a[30:]
                        self.fields[f'variable_parameters_types_x_variable_parameters_type{index}'] = \
                                forms.ChoiceField(choices=VARIABLE_PARAMETERS_TYPE, label="Variable Parameter Types", required=False)


class ExperimentGeolocation(forms.Form):
    body_x_uid = forms.CharField(required=False, label="UID", widget= forms.TextInput
                                (attrs={'placeholder': 'BODY_PlanetaryFamily_PlanetaryName'}))
    body_x_coordinate_system = forms.ChoiceField(required=False, label="Coordinate System", choices=BODY_COORDINATE_SYSTEM)
    geolocation_x_place = forms.CharField(required=False, label="Place", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[NULL]]>',
                                   'placeholder': '<![CDATA[NULL]]>'}))
    geolocation_x_region = forms.CharField(required=False, label="Region", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[NULL]]>',
                                   'placeholder': '<![CDATA[NULL]]>'}))
    geolocation_x_country_code = forms.CharField(required=False, label="Country Code", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    geolocation_x_type = forms.CharField(required=False, label="Type", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    coordinate_x_latitude = forms.CharField(required=False, label="Latitude", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    coordinate_x_longitude = forms.CharField(required=False, label="Longitude", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    coordinate_x_altitude = forms.CharField(required=False, label="Altitude")

    def __init__(self, *args, **kwargs):
                session = kwargs.pop('session', 0)
                array = []
                coordinate_array = []
                geolocation_array = []
                
                coordinate_counter = 0
                geolocation_counter = 0
                # variable_parameters_type_counter = 0
                if session != 0:
                        for i in session:
                                array.append(i)
                        for a in array:
                                if a.count('coordinate') > 0:
                                        coordinate_counter += a.count('coordinate')
                                        coordinate_array.append(a)
                                elif a.count('geolocation') > 0:
                                        geolocation_counter += a.count('geolocation')
                                        geolocation_array.append(a)
                        # variable_parameters_type_counter = array.count('variable_parameters_types_x_variable_parameters_type')
                super(ExperimentGeolocation, self).__init__(*args, **kwargs)

                # correct all to True
                for a in geolocation_array:
                        index = a[11:]
                        self.fields[f'geolocation_x_place{index}'] = \
                                forms.CharField(required=False, label="Place", widget= forms.TextInput
                                        (attrs={'auto_fill': '<![CDATA[NULL]]>',
                                                'placeholder': '<![CDATA[NULL]]>'}))
                        self.fields[f'geolocation_x_region{index}'] = \
                                forms.CharField(required=False, label="Region", widget= forms.TextInput
                                        (attrs={'auto_fill': '<![CDATA[NULL]]>',
                                        'placeholder': '<![CDATA[NULL]]>'}))
                        self.fields[f'geolocation_x_country_code{index}'] = \
                                forms.CharField(required=False, label="Country Code", widget= forms.TextInput
                                        (attrs={'auto_fill': 'NULL',
                                        'placeholder': 'NULL'}))
                        self.fields[f'geolocation_x_type{index}'] = \
                                forms.CharField(required=False, label="Type", widget= forms.TextInput
                                        (attrs={'auto_fill': 'NULL',
                                        'placeholder': 'NULL'}))
                        self.fields[f'coordinate_x_latitude{index}'] = \
                                forms.CharField(required=False, label='Latitude', widget= forms.TextInput
                                        (attrs={'auto_fill': 'NULL',
                                                'placeholder': 'NULL'}))
                        self.fields[f'coordinate_x_longitude{index}'] = \
                                forms.CharField(required=False, label='Longitude', widget= forms.TextInput
                                        (attrs={'auto_fill': 'NULL',
                                                'placeholder': 'NULL'}))
                        self.fields[f'coordinate_x_altitude{index}'] = \
                                forms.CharField(required=False, label='Altitude')

                for a in coordinate_array:
                        index = a[10:]
                        self.fields[f'coordinate_x_latitude{index}'] = \
                                forms.CharField(required=False, label='Latitude', widget= forms.TextInput
                                        (attrs={'auto_fill': 'NULL',
                                                'placeholder': 'NULL'}))
                        self.fields[f'coordinate_x_longitude{index}'.format(index=index)] = \
                                forms.CharField(required=False, label='Longitude', widget= forms.TextInput
                                        (attrs={'auto_fill': 'NULL',
                                                'placeholder': 'NULL'}))
                        self.fields[f'coordinate_x_altitude{index}'.format(index=index)] = \
                                forms.CharField(required=False, label='Altitude')


class ExperimentMultipleSections(forms.Form):
    experiment_x_comments = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'parent_tag':'experiment',
                                   'name': 'comments',
                                   'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    preview_x_x = forms.CharField(required=False, label="X")
    preview_x_y = forms.CharField(required=False, label="Y")
    preview_x_y2 = forms.CharField(required=False, label="Y2")
    preview_x_filename = forms.CharField(required=False, label="Filename")
    image_x_filename = forms.CharField(required=False, label="Filename")
    image_x_caption = forms.CharField(required=False, label="Caption", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    documentation_x_name = forms.CharField(required=False, label="Name")
    documentation_x_filename = forms.CharField(required=False, label="Filename")
    publications_x_publication_uid = forms.CharField(required=False, label="Publication UID")
    experiment_x_publication_comments = forms.CharField(required=False, label="Publication Comments")
    sponsor_x_acronym = forms.CharField(required=False, label="Acronym")
    sponsor_x_name = forms.CharField(required=False, label="Name")
    sponsor_x_award = forms.CharField(required=False, label="Award", widget= forms.TextInput
                           (attrs={'auto_fill': 'False',
                                   'placeholder': "Format: 'ACRONYM: Title (award number)'"}))

    def __init__(self, *args, **kwargs):
                session = kwargs.pop('session', 0)
                array = []
                image_array = []
                documentation_array = []
                publication_array = []
                sponsor_array = []

                image_counter = 0
                documentation_counter = 0
                publication_counter = 0
                sponsor_counter = 0

                if session != 0:
                        for i in session:
                                array.append(i)
                        for a in array:
                                if a.count('image') > 0:
                                        image_counter += 1
                                        image_array.append(a)
                                elif a.count('documentation') > 0:
                                        documentation_counter += 1
                                        documentation_array.append(a)
                                elif a.count('publication_uid') > 0:
                                        publication_counter += 1
                                        publication_array.append(a)
                                elif a.count('sponsor') > 0:
                                        sponsor_counter += 1
                                        sponsor_array.append(a)
                
                super(ExperimentMultipleSections, self).__init__(*args, **kwargs)

                # correct all to True
                for a in image_array:
                        index = a[5:]
                        self.fields[f'image_x_filename{index}'] = \
                                forms.CharField(required=False, label="Filename")
                        self.fields[f'image_x_caption{index}'] = \
                                forms.CharField(required=False, label="Caption", widget= forms.TextInput
                                        (attrs={'auto_fill': '<![CDATA[]]>',
                                                'placeholder': '<![CDATA[]]>'}))

                for a in documentation_array:
                        index = a[13:]
                        self.fields[f'documentation_x_name{index}'] = \
                                forms.CharField(required=False, label="Name")
                        self.fields[f'documentation_x_filename{index}'] = \
                                forms.CharField(required=False, label="Filename")

                for a in publication_array:
                        index = a[15:]
                        self.fields[f'publications_x_publication_uid{index}'] = \
                                forms.CharField(required=False, label="Publication UID")

                for a in sponsor_array:
                        index = a[7:]
                        self.fields[f'sponsor_x_acronym{index}'] = \
                                forms.CharField(required=False, label="Acronym")
                        self.fields[f'sponsor_x_name{index}'] = \
                                forms.CharField(required=False, label="Name")
                        self.fields[f'sponsor_x_award{index}'] = \
                                forms.CharField(required=False, label="Award")
                     

class InsertSampleForm(forms.Form):
    """
    Form for inserting a sample into xml parser
    """

    # Shows the fields with placeholders that correspond to the autofill from the view code
    # Researcher is still able to put in a different value, which will override the auto_fill
    sample_x_import_mode = forms.ChoiceField(required=False, choices=IMPORT_MODE_CHOICES, label="Import Mode")
    sample_x_uid = forms.CharField(required=False, label="UID")
    owner_databases_x_database_uid = forms.CharField(required=False, label="Database UID", widget= forms.TextInput
                           (attrs={'auto_fill': 'DB_REAP',
                                   'placeholder': 'DB_REAP'}))
    experimentalists_x_experimentalist_uid = forms.CharField(required=False, label="Experimentalist UID")
    sample_x_name = forms.CharField(required=False, label="Name")
    sample_x_date = forms.CharField(required=False, label="Date", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    sample_x_provider = forms.CharField(required=False, label="Provider", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[Laboratoire de géologie de Lyon]]>',
                                   'placeholder': '<![CDATA[Laboratoire de géologie de Lyon]]>'}))
    sample_x_is_generic = forms.ChoiceField(required=False, label="Is Generic", choices=SAMPLE_IS_GENERIC)
    body_x_uid = forms.CharField(required=False, label="UID")
    body_x_terrain_type = forms.ChoiceField(required=False, label="Terrain Type", choices=SAMPLE_TERRAIN_TYPE)
    body_x_coordinate_system = forms.CharField(required=False, label="Coordinate System", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))                               
    geolocation_x_place = forms.CharField(required=False, label="Place", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[NULL]]>',
                                   'placeholder': '<![CDATA[NULL]]>'}))
    geolocation_x_region = forms.CharField(required=False, label="Region", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[NULL]]>',
                                   'placeholder': '<![CDATA[NULL]]>'}))
    geolocation_x_country_code = forms.CharField(required=False, label="Country Code", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    geolocation_x_type = forms.ChoiceField(required=False, label="Type", choices=SAMPLE_GEOLOCATION_TYPE)
    coordinate_x_latitude = forms.CharField(required=False, label="Latitude", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    coordinate_x_longitude = forms.CharField(required=False, label="Longitude", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    coordinate_x_altitude = forms.CharField(required=False, label="Altitude")
    sample_x_surface_roughness = forms.CharField(required=False, label="Surface Roughness")
    sample_x_size_unit = forms.CharField(required=False, label="Size Unit")
    sample_x_comments = forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    sample_x_substrate_material = forms.CharField(required=False, label="Substrate Material", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    sample_x_substrate_comments = forms.CharField(required=False, label="Substrate Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    parameters_environment_x_time_unit = forms.ChoiceField(required=False, label="Time Unit", choices=SAMPLE_PARAMETER_TIME_UNIT)
    temperature_x_unit = forms.ChoiceField(required=False, label="Unit", choices=SAMPLE_PARAMETER_UNIT)
    temperature_x_value = forms.CharField(required=False, label="Value")
    temperature_x_error = forms.CharField(required=False, label="Error")
    temperature_x_time = forms.CharField(required=False, label="Time")
    temperature_x_time_error = forms.CharField(required=False, label="Time Error")
    temperature_x_max = forms.CharField(required=False, label="Max")
    temperature_x_max_error = forms.CharField(required=False, label="Max Error")
    temperature_x_max_time = forms.CharField(required=False, label="Max Time", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    temperature_x_comments = forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    fluid_x_type = forms.ChoiceField(required=False, label="Type", choices=SAMPLE_FLUID_TYPE)
    fluid_x_temperature = forms.CharField(required=False, label="Temperature")
    fluid_x_temperature_error = forms.CharField(required=False, label="Temperature Error")
    fluid_x_pressure_unit = forms.ChoiceField(required=False, label="Pressure Unit", choices=SAMPLE_FLUID_PRESSURE_UNIT)
    fluid_x_pressure = forms.CharField(required=False, label="Pressure")
    fluid_x_pressure_error = forms.CharField(required=False, label="Pressure Error")
    fluid_x_ph = forms.CharField(required=False, label="PH")
    fluid_x_ph_error = forms.CharField(required=False, label="PH Error")
    fluid_x_time = forms.CharField(required=False, label="Time")
    fluid_x_time_error = forms.CharField(required=False, label="Time Error")
    fluid_x_comments = forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    layer_x_import_mode = forms.ChoiceField(required=False, label="Import Mode", choices=IMPORT_MODE_CHOICES)
    layer_x_name = forms.CharField(required=False, label="Name")
    layer_x_order = forms.CharField(required=False, label="", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    layer_x_type = forms.ChoiceField(required=False, label="Type", choices=SAMPLE_LAYER_TYPE)
    layer_x_thickness = forms.CharField(required=False, label="Thickness", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    layer_x_thickness_error = forms.CharField(required=False, label="Thickness Error", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    layer_x_mass = forms.CharField(required=False, label="Mass")
    layer_x_mass_error = forms.CharField(required=False, label="Mass Error")
    layer_x_texture = forms.ChoiceField(required=False, label="Texture", choices=SAMPLE_LAYER_TEXTURE)
    layer_x_porosity_type = forms.ChoiceField(required=False, label="Porosity Type", choices=SAMPLE_POROSITY_TYPE)
    layer_x_compacity = forms.CharField(required=False, label="Compacity")
    layer_x_compacity_error = forms.CharField(required=False, label="Compacity Error")
    layer_x_density = forms.CharField(required=False, label="Density")
    layer_x_density_error = forms.CharField(required=False, label="Density Error")
    layer_x_comments = forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    layer_x_formation_mode = forms.CharField(required=False, label="Formation Mode")
    layer_x_formation_rate = forms.CharField(required=False, label="Formation Rate")
    layer_x_formation_temperature = forms.CharField(required=False, label="Formation Temperature")
    layer_x_formation_temperature_error = forms.CharField(required=False, label="Formation Error")
    layer_x_formation_pressure = forms.CharField(required=False, label="Formation Pressure")
    layer_x_formation_pressure_error = forms.CharField(required=False, label="Formation Pressure Error")
    layer_x_formation_fluid_pressure = forms.CharField(required=False, label="Formation Fluid Pressure")
    layer_x_formation_fluid_pressure_error = forms.CharField(required=False, label="Formation Fluid Pressure Error")
    layer_x_formation_comments = forms.CharField(required=False, label="Formation Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    layer_x_materials_mixing = forms.ChoiceField(required=False, label="Materials Mixing", choices=LAYER_MATERIALS_MIXING)
    material_x_import_mode = forms.ChoiceField(choices=MATERIAL_IMPORT_MODE, required=False, label="Import Mode")
    material_x_uid = forms.CharField(required=False, label="UID")
    material_x_relevance = forms.CharField(required=False, label="Relevance")
    material_x_arrangement = forms.CharField(required=False, label="Arrangement", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    material_x_mass = forms.CharField(required=False, label="Mass")
    material_x_mass_error = forms.CharField(required=False, label="Mass Error")
    material_x_mass_fraction = forms.CharField(required=False, label="Mass Fraction")
    material_x_mass_fraction_error = forms.CharField(required=False, label="Mass Fraction Error", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    material_x_abundance_comments = forms.CharField(required=False, label="Abundance Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    material_x_name = forms.CharField(required=False, label="Name")
    material_x_family = forms.CharField(required=False, label="Family")
    material_x_local_reference_code = forms.CharField(required=False, label="Local Reference Code")
    material_x_origin = forms.CharField(required=False, label="Origin")
    material_x_comments = forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    material_x_constituents_mixing = forms.CharField(required=False, label="Constituents Mixing")
    basic_constituent_x_import_mode = forms.CharField(required=False, label="Import Mode")
    basic_constituent_x_uid = forms.CharField(required=False, label="UID")
    basic_constituent_x_relevance = forms.CharField(required=False, label="Relevance")
    basic_constituent_x_arrangement = forms.CharField(required=False, label="Arrangement")
    basic_constituent_x_mass = forms.CharField(required=False, label="Mass")
    basic_constituent_x_mass_error = forms.CharField(required=False, label="Mass Error")
    basic_constituent_x_mass_fraction = forms.CharField(required=False, label="Mass Fraction")
    basic_constituent_x_mass_fraction_error = forms.CharField(required=False, label="Mass Fraction Error")
    basic_constituent_x_mole = forms.CharField(required=False, label="Mole")
    basic_constituent_x_mole_error = forms.CharField(required=False, label="Mole Error")
    basic_constituent_x_mole_fraction = forms.CharField(required=False, label="Mole Fraction")
    basic_constituent_x_mole_fraction_error = forms.CharField(required=False, label="Mole Fraction Error")
    basic_constituent_x_abundance_comments = forms.CharField(required=False, label="Abundance Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    basic_constituent_x_name = forms.CharField(required=False, label="Name")
    basic_constituent_x_fundamental_phase_uid = forms.CharField(required=False, label="Fundamental Phase UID")
    basic_constituent_x_texture = forms.CharField(required=False, label="Texture")
    basic_constituent_x_comments = forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    
    def __init__(self, *args, **kwargs):
        session = kwargs.pop('session', 0)
        array = []
        sample_section_array = []
        sample_database_uid_array = []
        sample_experimentalist_uid_array = []
        sample_coordinate_array = []
        sample_geolocation_array = []
        sample_basic_constituent_array = []
        sample_material_array = []
        sample_layer_array = []

        sample_section_counter = 0
        sample_database_uid_counter = 0
        sample_experimentalist_uid_counter = 0
        sample_coordinate_counter = 0
        sample_geolocation_counter = 0
        sample_basic_constituent_counter = 0
        sample_material_counter = 0
        sample_layer_counter = 0

        if session != 0:
                for i in session:
                        array.append(i)
                for a in array:
                        if a.count('sample_section') > 0:
                                sample_section_counter += 1
                                sample_section_array.append(a)
                        elif a.count('sample_database_uid') > 0:
                                sample_database_uid_counter += 1
                                sample_database_uid_array.append(a)
                        elif a.count('sample_experimentalist_uid') > 0:
                                sample_experimentalist_uid_counter += 1
                                sample_experimentalist_uid_array.append(a)
                        elif a.count('sample_coordinate') > 0:
                                sample_coordinate_counter += 1
                                sample_coordinate_array.append(a)
                        elif a.count('sample_geolocation') > 0:
                                sample_geolocation_counter += 1
                                sample_geolocation_array.append(a)
                        elif a.count('sample_basic_constituent') > 0:
                                sample_basic_constituent_counter += 1
                                sample_basic_constituent_array.append(a)
                        elif a.count('sample_material') > 0:
                                sample_material_counter += 1
                                sample_material_array.append(a)
                        elif a.count('sample_layer') > 0:
                                sample_layer_counter += 1
                                sample_layer_array.append(a)
        
        super(InsertSampleForm, self).__init__(*args, **kwargs)
        for a in sample_section_array:
                index = a[-4:]
                self.fields[f'sample_x_import_mode{index}'] = \
                        forms.ChoiceField(required=False, choices=IMPORT_MODE_CHOICES, label="Import Mode")
                self.fields[f'sample_x_uid{index}'] = \
                        forms.CharField(required=False, label="UID")
                self.fields[f'owner_databases_x_database_uid{index}'] = \
                        forms.CharField(required=False, label="Database UID", widget= forms.TextInput
                           (attrs={'auto_fill': 'DB_REAP',
                                   'placeholder': 'DB_REAP'}))
                self.fields[f'experimentalists_x_experimentalist_uid{index}'] = \
                        forms.CharField(required=False, label="Experimentalist UID")
                self.fields[f'sample_x_name{index}'] = \
                        forms.CharField(required=False, label="Name")
                self.fields[f'sample_x_date{index}'] = \
                        forms.CharField(required=False, label="Date", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'sample_x_provider{index}'] = \
                        forms.CharField(required=False, label="Provider", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[Laboratoire de géologie de Lyon]]>',
                                   'placeholder': '<![CDATA[Laboratoire de géologie de Lyon]]>'}))
                self.fields[f'sample_x_is_generic{index}'] = \
                        forms.ChoiceField(required=False, label="Is Generic", choices=SAMPLE_IS_GENERIC)
                self.fields[f'body_x_uid{index}'] = \
                        forms.CharField(required=False, label="UID")
                self.fields[f'body_x_terrain_type{index}'] = \
                        forms.ChoiceField(required=False, label="Terrain Type", choices=SAMPLE_TERRAIN_TYPE)
                self.fields[f'body_x_coordinate_system{index}'] = \
                        forms.CharField(required=False, label="Coordinate System", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'sample_x_import_mode{index}'] = \
                        forms.CharField(required=False, label="Import Mode")
                self.fields[f'sample_x_import_mode{index}'] = \
                        forms.CharField(required=False, label="Import Mode")
                self.fields[f'sample_x_import_mode{index}'] = \
                        forms.CharField(required=False, label="Import Mode")
                self.fields[f'sample_x_import_mode{index}'] = \
                        forms.CharField(required=False, label="Import Mode")
                self.fields[f'sample_x_import_mode{index}'] = \
                        forms.CharField(required=False, label="Import Mode")
                self.fields[f'geolocation_x_place{index}'] = \
                        forms.CharField(required=False, label="Place", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[NULL]]>',
                                   'placeholder': '<![CDATA[NULL]]>'}))
                self.fields[f'geolocation_x_region{index}'] = \
                        forms.CharField(required=False, label="Region", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[NULL]]>',
                                   'placeholder': '<![CDATA[NULL]]>'}))
                self.fields[f'geolocation_x_country_code{index}'] = \
                        forms.CharField(required=False, label="Country Code", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'geolocation_x_type{index}'] = \
                        forms.ChoiceField(required=False, label="Type", choices=SAMPLE_GEOLOCATION_TYPE)
                self.fields[f'coordinate_x_latitude{index}'] = \
                        forms.CharField(required=False, label="Latitude", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'coordinate_x_longitude{index}'] = \
                        forms.CharField(required=False, label="Longitude", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'coordinate_x_altitude{index}'] = \
                        forms.CharField(required=False, label="Altitude")
                self.fields[f'sample_x_surface_roughness{index}'] = \
                        forms.CharField(required=False, label="Surface Roughness")
                self.fields[f'sample_x_size_unit{index}'] = \
                        forms.CharField(required=False, label="Size Unit")
                self.fields[f'sample_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'sample_x_substrate_material{index}'] = \
                        forms.CharField(required=False, label="Substrate Material", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'sample_x_substrate_comments{index}'] = \
                        forms.CharField(required=False, label="Substrate Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'parameters_environment_x_time_unit{index}'] = \
                        forms.ChoiceField(required=False, label="Time Unit", choices=SAMPLE_PARAMETER_TIME_UNIT)
                self.fields[f'temperature_x_unit{index}'] = \
                        forms.CharField(required=False, label="Unit")
                self.fields[f'temperature_x_value{index}'] = \
                        forms.CharField(required=False, label="Value")
                self.fields[f'temperature_x_error{index}'] = \
                        forms.CharField(required=False, label="Error")
                self.fields[f'temperature_x_time{index}'] = \
                        forms.CharField(required=False, label="Time")

                self.fields[f'temperature_x_time_error{index}'] = \
                        forms.CharField(required=False, label="Time Error")
                self.fields[f'temperature_x_max{index}'] = \
                        forms.CharField(required=False, label="Max")
                self.fields[f'temperature_x_max_error{index}'] = \
                        forms.CharField(required=False, label="Max Error")
                self.fields[f'temperature_x_max_time{index}'] = \
                        forms.CharField(required=False, label="Max Time", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'temperature_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))

                self.fields[f'fluid_x_type{index}'] = \
                        forms.ChoiceField(required=False, label="Type", choices=SAMPLE_FLUID_TYPE)
                self.fields[f'fluid_x_temperature{index}'] = \
                        forms.CharField(required=False, label="Temperature")
                self.fields[f'fluid_x_temperature_error{index}'] = \
                        forms.CharField(required=False, label="Temperature Error")
                self.fields[f'fluid_x_pressure_unit{index}'] = \
                        forms.ChoiceField(required=False, label="Pressure Unit", choices=SAMPLE_FLUID_PRESSURE_UNIT)
                self.fields[f'fluid_x_pressure{index}'] = \
                        forms.CharField(required=False, label="Pressure")
                self.fields[f'fluid_x_pressure_error{index}'] = \
                        forms.CharField(required=False, label="Pressure Error")
                self.fields[f'fluid_x_ph{index}'] = \
                        forms.CharField(required=False, label="PH")
                self.fields[f'fluid_x_ph_error{index}'] = \
                        forms.CharField(required=False, label="PH Error")
                self.fields[f'fluid_x_time{index}'] = \
                        forms.CharField(required=False, label="Time")
                self.fields[f'fluid_x_time_error{index}'] = \
                        forms.CharField(required=False, label="Time Error")
                self.fields[f'fluid_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))

                self.fields[f'layer_x_import_mode{index}'] = \
                        forms.ChoiceField(required=False, label="Import Mode", choices=IMPORT_MODE_CHOICES)
                self.fields[f'layer_x_name{index}'] = \
                        forms.CharField(required=False, label="Name")
                self.fields[f'layer_x_order{index}'] = \
                        forms.CharField(required=False, label="Order", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'layer_x_type{index}'] = \
                        forms.ChoiceField(required=False, label="Type", choices=SAMPLE_LAYER_TYPE)
                self.fields[f'layer_x_thickness{index}'] = \
                        forms.CharField(required=False, label="Thickness", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'layer_x_thickness_error{index}'] = \
                        forms.CharField(required=False, label="Thickness Error", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))

                self.fields[f'layer_x_mass{index}'] = \
                        forms.CharField(required=False, label="Mass")
                self.fields[f'layer_x_mass_error{index}'] = \
                        forms.CharField(required=False, label="Mass Error")
                self.fields[f'layer_x_texture{index}'] = \
                        forms.ChoiceField(required=False, label="Texture", choices=SAMPLE_LAYER_TEXTURE)
                self.fields[f'layer_x_porosity_type{index}'] = \
                        forms.ChoiceField(required=False, label="Porosity Type", choices=SAMPLE_POROSITY_TYPE)
                self.fields[f'layer_x_compacity{index}'] = \
                        forms.CharField(required=False, label="Compacity")
                self.fields[f'layer_x_compacity_error{index}'] = \
                        forms.CharField(required=False, label="Compacity Error")
                self.fields[f'layer_x_density{index}'] = \
                        forms.CharField(required=False, label="Density")
                self.fields[f'layer_x_density_error{index}'] = \
                        forms.CharField(required=False, label="Density Error")
                self.fields[f'layer_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'layer_x_formation_mode{index}'] = \
                        forms.CharField(required=False, label="Formation Mode")
                self.fields[f'layer_x_formation_rate{index}'] = \
                        forms.CharField(required=False, label="Formation Rate")
                self.fields[f'layer_x_formation_temperature{index}'] = \
                        forms.CharField(required=False, label="Formation Temperature")
                self.fields[f'layer_x_formation_temperature_error{index}'] = \
                        forms.CharField(required=False, label="Formation Error")
                self.fields[f'layer_x_formation_pressure{index}'] = \
                        forms.CharField(required=False, label="Formation Pressure")
                self.fields[f'layer_x_formation_pressure_error{index}'] = \
                        forms.CharField(required=False, label="Formation Pressure Error")
                self.fields[f'layer_x_formation_fluid_pressure{index}'] = \
                        forms.CharField(required=False, label="Formation Fluid Pressure")
                self.fields[f'layer_x_formation_fluid_pressure_error{index}'] = \
                        forms.CharField(required=False, label="Formation Fluid Pressure Error")
                self.fields[f'layer_x_formation_comments{index}'] = \
                        forms.CharField(required=False, label="Formation Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'layer_x_materials_mixing{index}'] = \
                        forms.ChoiceField(required=False, label="Materials Mixing", choices=LAYER_MATERIALS_MIXING)

                self.fields[f'material_x_import_mode{index}'] = \
                        forms.ChoiceField(choices=MATERIAL_IMPORT_MODE, required=False, label="Import Mode")
                self.fields[f'material_x_uid{index}'] = \
                        forms.CharField(required=False, label="UID")
                self.fields[f'material_x_relevance{index}'] = \
                        forms.CharField(required=False, label="Relevance")
                self.fields[f'material_x_arrangement{index}'] = \
                        forms.CharField(required=False, label="Arrangement", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'material_x_mass{index}'] = \
                        forms.CharField(required=False, label="Mass")
                self.fields[f'material_x_mass_error{index}'] = \
                        forms.CharField(required=False, label="Mass Error")
                self.fields[f'material_x_mass_fraction{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction")
                self.fields[f'material_x_mass_fraction_error{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction Error", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'material_x_abundance_comments{index}'] = \
                        forms.CharField(required=False, label="Abundance Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'material_x_name{index}'] = \
                        forms.CharField(required=False, label="Name")
                self.fields[f'material_x_family{index}'] = \
                        forms.CharField(required=False, label="Family")
                self.fields[f'material_x_local_reference_code{index}'] = \
                        forms.CharField(required=False, label="Local Reference Code")
                self.fields[f'material_x_origin{index}'] = \
                        forms.CharField(required=False, label="Origin")
                self.fields[f'material_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'material_x_constituents_mixing{index}'] = \
                        forms.CharField(required=False, label="Constituents Mixing")
                self.fields[f'basic_constituent_x_import_mode{index}'] = \
                        forms.CharField(required=False, label="Import Mode")
                self.fields[f'basic_constituent_x_uid{index}'] = \
                        forms.CharField(required=False, label="UID")
                self.fields[f'basic_constituent_x_relevance{index}'] = \
                        forms.CharField(required=False, label="Relevance")
                self.fields[f'basic_constituent_x_arrangement{index}'] = \
                        forms.CharField(required=False, label="Arrangement")
                self.fields[f'basic_constituent_x_mass{index}'] = \
                        forms.CharField(required=False, label="Mass")
                self.fields[f'basic_constituent_x_mass_error{index}'] = \
                        forms.CharField(required=False, label="Mass Error")
                self.fields[f'basic_constituent_x_mass_fraction{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction")
                self.fields[f'basic_constituent_x_mass_fraction_error{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction Error")
                self.fields[f'basic_constituent_x_mole{index}'] = \
                        forms.CharField(required=False, label="Mole")
                self.fields[f'basic_constituent_x_mole_error{index}'] = \
                        forms.CharField(required=False, label="Mole Error")
                self.fields[f'basic_constituent_x_mole_fraction{index}'] = \
                        forms.CharField(required=False, label="Mole Fraction")
                self.fields[f'basic_constituent_x_mole_fraction_error{index}'] = \
                        forms.CharField(required=False, label="Mole Fraction Error")
                self.fields[f'basic_constituent_x_abundance_comments{index}'] = \
                        forms.CharField(required=False, label="Abundance Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'basic_constituent_x_name{index}'] = \
                        forms.CharField(required=False, label="Name")
                self.fields[f'basic_constituent_x_fundamental_phase_uid{index}'] = \
                        forms.CharField(required=False, label="Fundamental Phase UID")
                self.fields[f'basic_constituent_x_texture{index}'] = \
                        forms.CharField(required=False, label="Texture")
                self.fields[f'basic_constituent_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput)
                        
        
        for a in sample_database_uid_array:
                index = a[19:]
                self.fields[f'owner_databases_x_database_uid{index}'] = \
                        forms.CharField(required=False, label="Database UID", widget= forms.TextInput
                           (attrs={'auto_fill': 'DB_REAP',
                                   'placeholder': 'DB_REAP'}))

        for a in sample_experimentalist_uid_array:
                index = a[26:]
                self.fields[f'experimentalists_x_experimentalist_uid{index}'] = \
                        forms.CharField(required=False, label="Experimentalist UID")

        for a in sample_coordinate_array:
                index = a[17:]
                self.fields[f'coordinate_x_latitude{index}'] = \
                        forms.CharField(required=False, label="Latitude", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'coordinate_x_longitude{index}'] = \
                        forms.CharField(required=False, label="Longitude", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'coordinate_x_altitude{index}'] = \
                        forms.CharField(required=False, label="Altitude")

        for a in sample_geolocation_array:
                index = a[18:]
                self.fields[f'geolocation_x_place{index}'] = \
                        forms.CharField(required=False, label="Place", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[NULL]]>',
                                   'placeholder': '<![CDATA[NULL]]>'}))
                self.fields[f'geolocation_x_region{index}'] = \
                        forms.CharField(required=False, label="Region", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[NULL]]>',
                                   'placeholder': '<![CDATA[NULL]]>'}))
                self.fields[f'geolocation_x_country_code{index}'] = \
                        forms.CharField(required=False, label="Country Code", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'geolocation_x_type{index}'] = \
                        forms.ChoiceField(required=False, label="Type", choices=SAMPLE_GEOLOCATION_TYPE)
                self.fields[f'coordinate_x_latitude{index}'] = \
                        forms.CharField(required=False, label="Latitude", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'coordinate_x_longitude{index}'] = \
                        forms.CharField(required=False, label="Longitude", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'coordinate_x_altitude{index}'] = \
                        forms.CharField(required=False, label="Altitude")

        for a in sample_basic_constituent_array:
                index = a[24:]
                self.fields[f'basic_constituent_x_import_mode{index}'] = \
                        forms.CharField(required=False, label="Import Mode")
                self.fields[f'basic_constituent_x_uid{index}'] = \
                        forms.CharField(required=False, label="UID")
                self.fields[f'basic_constituent_x_relevance{index}'] = \
                        forms.CharField(required=False, label="Relevance")
                self.fields[f'basic_constituent_x_arrangement{index}'] = \
                        forms.CharField(required=False, label="Arrangement")
                self.fields[f'basic_constituent_x_mass{index}'] = \
                        forms.CharField(required=False, label="Mass")
                self.fields[f'basic_constituent_x_mass_error{index}'] = \
                        forms.CharField(required=False, label="Mass Error")
                self.fields[f'basic_constituent_x_mass_fraction{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction")
                self.fields[f'basic_constituent_x_mass_fraction_error{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction Error")
                self.fields[f'basic_constituent_x_mole{index}'] = \
                        forms.CharField(required=False, label="Mole")
                self.fields[f'basic_constituent_x_mole_error{index}'] = \
                        forms.CharField(required=False, label="Mole Error")
                self.fields[f'basic_constituent_x_mole_fraction{index}'] = \
                        forms.CharField(required=False, label="Mole Fraction")
                self.fields[f'basic_constituent_x_mole_fraction_error{index}'] = \
                        forms.CharField(required=False, label="Mole Fraction Error")
                self.fields[f'basic_constituent_x_abundance_comments{index}'] = \
                        forms.CharField(required=False, label="Abundance Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'basic_constituent_x_name{index}'] = \
                        forms.CharField(required=False, label="Name")
                self.fields[f'basic_constituent_x_fundamental_phase_uid{index}'] = \
                        forms.CharField(required=False, label="Fundamental Phase UID")
                self.fields[f'basic_constituent_x_texture{index}'] = \
                        forms.CharField(required=False, label="Texture")
                self.fields[f'basic_constituent_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput)

        for a in sample_material_array:
                index = a[15:]
                self.fields[f'material_x_import_mode{index}'] = \
                        forms.ChoiceField(choices=MATERIAL_IMPORT_MODE, required=False, label="Import Mode")
                self.fields[f'material_x_uid{index}'] = \
                        forms.CharField(required=False, label="UID")
                self.fields[f'material_x_relevance{index}'] = \
                        forms.CharField(required=False, label="Relevance")
                self.fields[f'material_x_arrangement{index}'] = \
                        forms.CharField(required=False, label="Arrangement", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'material_x_mass{index}'] = \
                        forms.CharField(required=False, label="Mass")
                self.fields[f'material_x_mass_error{index}'] = \
                        forms.CharField(required=False, label="Mass Error")
                self.fields[f'material_x_mass_fraction{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction")
                self.fields[f'material_x_mass_fraction_error{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction Error", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'material_x_abundance_comments{index}'] = \
                        forms.CharField(required=False, label="Abundance Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'material_x_name{index}'] = \
                        forms.CharField(required=False, label="Name")
                self.fields[f'material_x_family{index}'] = \
                        forms.CharField(required=False, label="Family")
                self.fields[f'material_x_local_reference_code{index}'] = \
                        forms.CharField(required=False, label="Local Reference Code")
                self.fields[f'material_x_origin{index}'] = \
                        forms.CharField(required=False, label="Origin")
                self.fields[f'material_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'material_x_constituents_mixing{index}'] = \
                        forms.CharField(required=False, label="Constituents Mixing")
                self.fields[f'basic_constituent_x_import_mode{index}'] = \
                        forms.CharField(required=False, label="Import Mode")
                self.fields[f'basic_constituent_x_uid{index}'] = \
                        forms.CharField(required=False, label="UID")
                self.fields[f'basic_constituent_x_relevance{index}'] = \
                        forms.CharField(required=False, label="Relevance")
                self.fields[f'basic_constituent_x_arrangement{index}'] = \
                        forms.CharField(required=False, label="Arrangement")
                self.fields[f'basic_constituent_x_mass{index}'] = \
                        forms.CharField(required=False, label="Mass")
                self.fields[f'basic_constituent_x_mass_error{index}'] = \
                        forms.CharField(required=False, label="Mass Error")
                self.fields[f'basic_constituent_x_mass_fraction{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction")
                self.fields[f'basic_constituent_x_mass_fraction_error{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction Error")
                self.fields[f'basic_constituent_x_mole{index}'] = \
                        forms.CharField(required=False, label="Mole")
                self.fields[f'basic_constituent_x_mole_error{index}'] = \
                        forms.CharField(required=False, label="Mole Error")
                self.fields[f'basic_constituent_x_mole_fraction{index}'] = \
                        forms.CharField(required=False, label="Mole Fraction")
                self.fields[f'basic_constituent_x_mole_fraction_error{index}'] = \
                        forms.CharField(required=False, label="Mole Fraction Error")
                self.fields[f'basic_constituent_x_abundance_comments{index}'] = \
                        forms.CharField(required=False, label="Abundance Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'basic_constituent_x_name{index}'] = \
                        forms.CharField(required=False, label="Name")
                self.fields[f'basic_constituent_x_fundamental_phase_uid{index}'] = \
                        forms.CharField(required=False, label="Fundamental Phase UID")
                self.fields[f'basic_constituent_x_texture{index}'] = \
                        forms.CharField(required=False, label="Texture")
                self.fields[f'basic_constituent_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput)


        for a in sample_layer_array:
                index = a[12:]
                self.fields[f'layer_x_import_mode{index}'] = \
                        forms.ChoiceField(required=False, label="Import Mode", choices=IMPORT_MODE_CHOICES)
                self.fields[f'layer_x_name{index}'] = \
                        forms.CharField(required=False, label="Name")
                self.fields[f'layer_x_order{index}'] = \
                        forms.CharField(required=False, label="", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'layer_x_type{index}'] = \
                        forms.ChoiceField(required=False, label="Type", choices=SAMPLE_LAYER_TYPE)
                self.fields[f'layer_x_thickness{index}'] = \
                        forms.CharField(required=False, label="Thickness", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'layer_x_thickness_error{index}'] = \
                        forms.CharField(required=False, label="Thickness Error", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'layer_x_mass{index}'] = \
                        forms.CharField(required=False, label="Mass")
                self.fields[f'layer_x_mass_error{index}'] = \
                        forms.CharField(required=False, label="Mass Error")
                self.fields[f'layer_x_texture{index}'] = \
                        forms.ChoiceField(required=False, label="Texture", choices=SAMPLE_LAYER_TEXTURE)
                self.fields[f'layer_x_porosity_type{index}'] = \
                        forms.ChoiceField(required=False, label="Porosity Type", choices=SAMPLE_POROSITY_TYPE)
                self.fields[f'layer_x_compacity{index}'] = \
                        forms.CharField(required=False, label="Compacity")
                self.fields[f'layer_x_compacity_error{index}'] = \
                        forms.CharField(required=False, label="Compacity Error")
                self.fields[f'layer_x_density{index}'] = \
                        forms.CharField(required=False, label="Density")
                self.fields[f'layer_x_density_error{index}'] = \
                        forms.CharField(required=False, label="Density Error")
                self.fields[f'layer_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'layer_x_formation_mode{index}'] = \
                        forms.CharField(required=False, label="Formation Mode")
                self.fields[f'layer_x_formation_rate{index}'] = \
                        forms.CharField(required=False, label="Formation Rate")
                self.fields[f'layer_x_formation_temperature{index}'] = \
                        forms.CharField(required=False, label="Formation Temperature")
                self.fields[f'layer_x_formation_temperature_error{index}'] = \
                        forms.CharField(required=False, label="Formation Error")
                self.fields[f'layer_x_formation_pressure{index}'] = \
                        forms.CharField(required=False, label="Formation Pressure")
                self.fields[f'layer_x_formation_pressure_error{index}'] = \
                        forms.CharField(required=False, label="Formation Pressure Error")
                self.fields[f'layer_x_formation_fluid_pressure{index}'] = \
                        forms.CharField(required=False, label="Formation Fluid Pressure")
                self.fields[f'layer_x_formation_fluid_pressure_error{index}'] = \
                        forms.CharField(required=False, label="Formation Fluid Pressure Error")
                self.fields[f'layer_x_formation_comments{index}'] = \
                        forms.CharField(required=False, label="Formation Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'layer_x_materials_mixing{index}'] = \
                        forms.ChoiceField(required=False, label="Materials Mixing", choices=LAYER_MATERIALS_MIXING)
                self.fields[f'material_x_import_mode{index}'] = \
                        forms.ChoiceField(choices=MATERIAL_IMPORT_MODE, required=False, label="Import Mode")
                self.fields[f'material_x_uid{index}'] = \
                        forms.CharField(required=False, label="UID")
                self.fields[f'material_x_relevance{index}'] = \
                        forms.CharField(required=False, label="Relevance")
                self.fields[f'material_x_arrangement{index}'] = \
                        forms.CharField(required=False, label="Arrangement", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'material_x_mass{index}'] = \
                        forms.CharField(required=False, label="Mass")
                self.fields[f'material_x_mass_error{index}'] = \
                        forms.CharField(required=False, label="Mass Error")
                self.fields[f'material_x_mass_fraction{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction")
                self.fields[f'material_x_mass_fraction_error{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction Error", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
                self.fields[f'material_x_abundance_comments{index}'] = \
                        forms.CharField(required=False, label="Abundance Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'material_x_name{index}'] = \
                        forms.CharField(required=False, label="Name")
                self.fields[f'material_x_family{index}'] = \
                        forms.CharField(required=False, label="Family")
                self.fields[f'material_x_local_reference_code{index}'] = \
                        forms.CharField(required=False, label="Local Reference Code")
                self.fields[f'material_x_origin{index}'] = \
                        forms.CharField(required=False, label="Origin")
                self.fields[f'material_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'material_x_constituents_mixing{index}'] = \
                        forms.CharField(required=False, label="Constituents Mixing")
                self.fields[f'basic_constituent_x_import_mode{index}'] = \
                        forms.CharField(required=False, label="Import Mode")
                self.fields[f'basic_constituent_x_uid{index}'] = \
                        forms.CharField(required=False, label="UID")
                self.fields[f'basic_constituent_x_relevance{index}'] = \
                        forms.CharField(required=False, label="Relevance")
                self.fields[f'basic_constituent_x_arrangement{index}'] = \
                        forms.CharField(required=False, label="Arrangement")
                self.fields[f'basic_constituent_x_mass{index}'] = \
                        forms.CharField(required=False, label="Mass")
                self.fields[f'basic_constituent_x_mass_error{index}'] = \
                        forms.CharField(required=False, label="Mass Error")
                self.fields[f'basic_constituent_x_mass_fraction{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction")
                self.fields[f'basic_constituent_x_mass_fraction_error{index}'] = \
                        forms.CharField(required=False, label="Mass Fraction Error")
                self.fields[f'basic_constituent_x_mole{index}'] = \
                        forms.CharField(required=False, label="Mole")
                self.fields[f'basic_constituent_x_mole_error{index}'] = \
                        forms.CharField(required=False, label="Mole Error")
                self.fields[f'basic_constituent_x_mole_fraction{index}'] = \
                        forms.CharField(required=False, label="Mole Fraction")
                self.fields[f'basic_constituent_x_mole_fraction_error{index}'] = \
                        forms.CharField(required=False, label="Mole Fraction Error")
                self.fields[f'basic_constituent_x_abundance_comments{index}'] = \
                        forms.CharField(required=False, label="Abundance Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
                self.fields[f'basic_constituent_x_name{index}'] = \
                        forms.CharField(required=False, label="Name")
                self.fields[f'basic_constituent_x_fundamental_phase_uid{index}'] = \
                        forms.CharField(required=False, label="Fundamental Phase UID")
                self.fields[f'basic_constituent_x_texture{index}'] = \
                        forms.CharField(required=False, label="Texture")
                self.fields[f'basic_constituent_x_comments{index}'] = \
                        forms.CharField(required=False, label="Comments", widget= forms.TextInput)
                

class InsertPublicationForm(forms.Form):
    """
    Form for inserting a sample into xml parser
    """

    # Shows the fields with placeholders that correspond to the autofill from the view code
    # Researcher is still able to put in a different value, which will override the auto_fill
    publication_x_import_mode = forms.ChoiceField(required=False, choices=IMPORT_MODE_CHOICES)
    publication_x_uid = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "Should be of the style ‘PUBLI_FirstAuthorName_Year(Letter)’"}))
    publication_x_type = forms.ChoiceField(required=False, choices=PUBLICATION_TYPES)
    publication_x_document_type = forms.ChoiceField(required=False, choices=PUBLICATION_DOCUMENT_TYPE)
    publication_x_state = forms.ChoiceField(required=False, choices=PUBLICATION_STATE)
    publication_x_access_right = forms.ChoiceField(required=False, choices=PUBLICATION_ACCESS_RIGHT)
    publication_x_access_free_date = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "Format: 'YYYY-MM-DD'"}))
    author_x_first_name = forms.CharField(required=False)
    author_x_family_name = forms.CharField(required=False)
    publication_x_year = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "Format: 'YYYY'"}))
    publication_x_title = forms.CharField(required=False)
    publication_x_journal = forms.CharField(required=False)
    publication_x_volume = forms.CharField(required=False)
    publication_x_number = forms.CharField(required=False)
    publication_x_first_page = forms.CharField(required=False)
    publication_x_last_page = forms.CharField(required=False)
    publication_x_pages_number = forms.CharField(required=False)
    publication_x_abstract = forms.CharField(required=False)
    keywords_x_keyword = forms.CharField(required=False)
    conference_x_name = forms.CharField(required=False)
    conference_x_location = forms.CharField(required=False)
    conference_x_date = forms.CharField(required=False)
    book_x_chapter_number = forms.CharField(required=False)
    book_x_title = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    book_x_series = forms.CharField(required=False)
    book_x_edition_number = forms.CharField(required=False)
    publication_x_editor = forms.CharField(required=False)
    publication_x_publisher = forms.CharField(required=False)
    publication_x_publisher_city = forms.CharField(required=False)
    dataset_x_database_name = forms.CharField(required=False)
    dataset_x_database_url = forms.CharField(required=False)
    publication_x_doi = forms.CharField(required=False)
    identifier_x_type = forms.ChoiceField(required=False, choices=PUBLICATION_IDENTIFIER_TYPE)
    identifier_x_code = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "MANDATORY, except for type={URL, no}"}))
    identifier_x_url = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "MANDATORY only for 'ARK, EISSN, ISBN, ISSN, ISTC, URL"}))
    publication_x_filename = forms.CharField(required=False)
    contents_x_content = forms.ChoiceField(required=False, choices=PUBLICATION_CONTENTS)
    cited_publications_x_publication_uid = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "‘PUBLI_FirstAuthorName_Year(Letter)’"}))
    used_experiments_x_experiment_uid = forms.CharField(required=False)
    used_bandlists_x_bandlist_uid = forms.CharField(required=False)
    publication_x_comments = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))

    def __init__(self, *args, **kwargs):
        session = kwargs.pop('session', 0)
        array = []
        publication_section_array = []
        publication_author_array = []
        publication_keyword_array = []
        publication_identifier_array = []
        publication_content_array = []
        publication_cited_publication_array = []
        publication_used_experiment_array = []
        publication_used_bandlist_array = []

        publication_section_counter = 0
        publication_author_counter = 0
        publication_keyword_counter = 0
        publication_identifier_counter = 0
        publication_content_counter = 0
        publication_cited_publication_counter = 0
        publication_used_experiment_counter = 0
        publication_used_bandlist_counter = 0

        if session != 0:
                for i in session:
                        array.append(i)
                for a in array:
                        if a.count('publication_section') > 0:
                                publication_section_counter += 1
                                publication_section_array.append(a)
                        elif a.count('publication_author') > 0:
                                publication_author_counter += 1
                                publication_author_array.append(a)
                        elif a.count('publication_keyword') > 0:
                                publication_keyword_counter += 1
                                publication_keyword_array.append(a)
                        elif a.count('publication_identifier') > 0:
                                publication_identifier_counter += 1
                                publication_identifier_array.append(a)
                        elif a.count('publication_content') > 0:
                                publication_content_counter += 1
                                publication_content_array.append(a)
                        elif a.count('publication_cited_publication') > 0:
                                publication_cited_publication_counter += 1
                                publication_cited_publication_array.append(a)
                        elif a.count('publication_used_experiment') > 0:
                                publication_used_experiment_counter += 1
                                publication_used_experiment_array.append(a)
                        elif a.count('publication_used_bandlist') > 0:
                                publication_used_bandlist_counter += 1
                                publication_used_bandlist_array.append(a)
        
        super(InsertPublicationForm, self).__init__(*args, **kwargs)
        for a in publication_section_array:
                index = a[19:]
                self.fields[f'publication_x_import_mode{index}'] = \
                        forms.ChoiceField(required=False, choices=IMPORT_MODE_CHOICES)
                self.fields[f'publication_x_uid{index}'] = \
                        forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "Should be of the style ‘PUBLI_FirstAuthorName_Year(Letter)’"}))
                self.fields[f'publication_x_type{index}'] = \
                        forms.ChoiceField(required=False, choices=PUBLICATION_TYPES)
                self.fields[f'publication_x_document_type{index}'] = \
                        forms.ChoiceField(required=False, choices=PUBLICATION_DOCUMENT_TYPE)
                self.fields[f'publication_x_state{index}'] = \
                        forms.ChoiceField(required=False, choices=PUBLICATION_STATE)
                self.fields[f'publication_x_access_right{index}'] = \
                        forms.ChoiceField(required=False, choices=PUBLICATION_ACCESS_RIGHT)
                self.fields[f'publication_x_access_free_date{index}'] = \
                        forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "Format: 'YYYY-MM-DD'"}))
                self.fields[f'author_x_first_name{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'author_x_family_name{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_year{index}'] = \
                        forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "Format: 'YYYY'"}))
                self.fields[f'publication_x_title{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_journal{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_volume{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_number{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_first_page{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_last_page{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_pages_number{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_abstract{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'keywords_x_keyword{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'conference_x_name{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'conference_x_location{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'conference_x_date{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'book_x_chapter_number{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'book_x_title{index}'] = \
                        forms.CharField(required=False, widget= forms.TextInput
                                        (attrs={'auto_fill': '<![CDATA[]]>',
                                                'placeholder': '<![CDATA[]]>'}))
                self.fields[f'book_x_series{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'book_x_edition_number{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_editor{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_x_publisher{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_publisher_city{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'dataset_x_x_database_name{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'dataset_x_database_url{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_doi{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'identifier_x_type{index}'] = \
                        forms.ChoiceField(required=False, choices=PUBLICATION_IDENTIFIER_TYPE)
                self.fields[f'identifier_x_code{index}'] = \
                        forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "MANDATORY, except for type={URL, no}"}))
                self.fields[f'identifier_x_url{index}'] = \
                        forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "MANDATORY only for 'ARK, EISSN, ISBN, ISSN, ISTC, URL"}))
                self.fields[f'publication_x_filename{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'contents_x_content{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'cited_publications_x_publication_uid{index}'] = \
                        forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "‘PUBLI_FirstAuthorName_Year(Letter)’"}))
                self.fields[f'used_experiments_x_experiment_uid{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'used_bandlists_x_bandlist_uid{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'publication_x_comments{index}'] = \
                        forms.CharField(required=False)

        for a in publication_author_array:
                index = a[18:]
                self.fields[f'author_x_first_name{index}'] = \
                        forms.CharField(required=False)
                self.fields[f'author_x_family_name{index}'] = \
                        forms.CharField(required=False)
        
        for a in publication_keyword_array:
                index = a[19:]
                self.fields[f'keywords_x_keyword{index}'] = \
                        forms.CharField(required=False)

        for a in publication_identifier_array:
                index = a[22:]
                self.fields[f'identifier_x_type{index}'] = \
                        forms.ChoiceField(required=False, choices=PUBLICATION_IDENTIFIER_TYPE)
                self.fields[f'identifier_x_code{index}'] = \
                        forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "MANDATORY, except for type={URL, no}"}))
                self.fields[f'identifier_x_url{index}'] = \
                        forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "MANDATORY only for 'ARK, EISSN, ISBN, ISSN, ISTC, URL"}))

        for a in publication_content_array:
                index = a[19:]
                self.fields[f'contents_x_content{index}'] = \
                        forms.ChoiceField(required=False, choices=PUBLICATION_CONTENTS)

        for a in publication_cited_publication_array:
                index = a[29:]
                self.fields[f'cited_publications_x_publication_uid{index}'] = \
                        forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'placeholder': "‘PUBLI_FirstAuthorName_Year(Letter)’"}))

        for a in publication_used_experiment_array:
                index = a[27:]
                self.fields[f'used_experiments_x_experiment_uid{index}'] = \
                        forms.CharField(required=False)

        for a in publication_used_bandlist_array:
                index = a[25:]
                self.fields[f'used_bandlists_x_bandlist_uid{index}'] = \
                        forms.CharField(required=False)


# ad hoc
class InsertExperimentForm(forms.Form):
    """
    Form for inserting a sample into xml parser
    """

    # Shows the fields with placeholders that correspond to the autofill from the view code
    # Researcher is still able to put in a different value, which will override the auto_fill
    experiment_x_import_mode = forms.ChoiceField(choices=IMPORT_MODE_CHOICES, label="Import Mode")
    experimentalists_x_uid = forms.CharField(required=False, label="Experiment UID")
    owner_databases_x_database_uid = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'auto_fill': 'DB_REAP',
                                   'placeholder': 'DB_REAP'}))
    experimentalists_x_experimentalist_uid = forms.CharField(required=False, label="Experimentalist UID")
    types_x_type = forms.ChoiceField(required=False, choices=TYPES_CHOICES, label="Types type")
    experiment_x_title = forms.CharField(required=False, label="Title")
    experiment_x_description = forms.CharField(required=False, label="Description", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    experiment_x_date_begin = forms.CharField(required=False, label="Date Begin", widget= forms.TextInput
                           (attrs={'placeholder': 'YYYY-MM-DD'}))
    experiment_x_date_end = forms.CharField(required=False, label="Date End", widget= forms.TextInput
                           (attrs={'placeholder': 'YYYY-MM-DD'}))
    experiment_x_parent_experiment_uid = forms.CharField(required=False, label="Parent Experiment UID")
    experiment_x_laboratory_uid = forms.CharField(required=False, label="Laboratory UID", widget= forms.TextInput
                           (attrs={'placeholder': 'only for laboratory experiments and calculations'}))
    body_x_uid = forms.CharField(required=False, label="UID", widget= forms.TextInput
                           (attrs={'placeholder': 'BODY_PlanetaryFamily_PlanetaryName'}))
    body_x_coordinate_system = forms.ChoiceField(required=False, label="Coordinate System", choices=BODY_COORDINATE_SYSTEM)
    geolocation_x_place = forms.CharField(required=False, label="Place", widget= forms.TextInput
                           (attrs={'placeholder': '**MANDATORY, recommended for DOI**'}))
    geolocation_x_region = forms.CharField(required=False, label="Region", widget= forms.TextInput
                           (attrs={'placeholder': '**MANDATORY and only for Earth**'}))
    geolocation_x_country_code = forms.CharField(required=False, label="Country Code", widget= forms.TextInput
                           (attrs={'placeholder': '**MANDATORY and only for Earth**'}))
    geolocation_x_type = forms.ChoiceField(required=False, choices=GEOLOCATION_TYPE, label="Type - **MANDATORY, recommended for DOI**")
    coordinate_x_latitude = forms.CharField(required=False, label="Latitude", widget= forms.TextInput
                           (attrs={'placeholder': '**MANDATORY**'}))
    coordinate_x_longitude = forms.CharField(required=False, label="Longitude", widget= forms.TextInput
                           (attrs={'placeholder': '**MANDATORY**'}))
    coordinate_x_altitude = forms.CharField(required=False, label="Altitude",)
    variable_parameters_types_x_variable_parameters_type = forms.ChoiceField(choices=VARIABLE_PARAMETERS_TYPE, label="Variable Parameter Types", required=False)
    experiment_x_variable_parameters_comments = forms.CharField(required=False, label="Parameter Comments")
    parameters_instrument_x_instrument_uid = forms.CharField(required=False, label="Instrument UID")
    parameters_instrument_x_instrument_carrier = forms.CharField(required=False, label="Instrument Carrier")
    parameters_instrument_x_instrument_sample_holder = forms.CharField(required=False, label="Instrument Sample Holder")
    parameters_instrument_x_spectrum_scan_number = forms.CharField(required=False, label="Spectrum Scan Number")
    spectral_x_unit = forms.ChoiceField(choices=SPECTRAL_UNIT, required=False, label="Unit")
    spectral_x_standard = forms.ChoiceField(choices=SPECTRAL_STANDARD, required=False, label="Standard")
    spectral_x_observation_mode = forms.ChoiceField(choices=SPECTRAL_OBERSATION_MODE, required=False, label="Observation Mode")
    range_types_x_type = forms.ChoiceField(choices=RANGE_TYPE, required=False, label="Type")
    range_x_min = forms.CharField(required=False, label="Min")
    range_x_max = forms.CharField(required=False, label="Max")
    range_x_absorption_edge_element_uid = forms.CharField(required=False, label="Absorption Edge Element UID")
    range_x_absorption_edge_type = forms.CharField(required=False, label="Absorption Edge type")
    range_x_sampling = forms.CharField(required=False, label="Sampling")
    range_x_resolution = forms.CharField(required=False, label="Resolution")
    range_x_position_error = forms.CharField(required=False, label="Position Error")
    filter_x_type = forms.CharField(required=False, label="Type")
    filter_x_place = forms.CharField(required=False, label="Place")
    filter_x_center = forms.CharField(required=False, label="Center")
    filter_x_width = forms.CharField(required=False, label="Width")
    spectral_x_comments = forms.CharField(required=False, label="Comments")
    angle_x_observation_geometry = forms.ChoiceField(choices=ANGLE_OBSERVATION_GEOMETRY, required=False)
    angle_x_observation_mode = forms.ChoiceField(choices=ANGLE_OBSERVATION_MODE, required=False)
    angle_x_incidence = forms.CharField(required=False, label="Incidence", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    angle_x_emergence = forms.CharField(required=False, label="Emergence", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    angle_x_azimuth = forms.CharField(required=False, label="Azimuth", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    angle_x_phase = forms.CharField(required=False, label="Phase",)
    angle_x_resolution_illumination = forms.CharField(required=False, label="Resolution Illumination", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    angle_x_resolution_observation = forms.CharField(required=False, label="Resolution Observation", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    angle_x_comments = forms.CharField(required=False, label="Comments",)
    polarization_x_type_illumination = forms.ChoiceField(label="Type Illumination", choices=POLARIZATION_TYPE_ILLUMINATION, required=False)
    polarization_x_type_observation = forms.ChoiceField(label="Type Observation", choices=POLARIZATION_TYPE_ILLUMINATION, required=False)
    polarization_x_polarizer_illumination = forms.CharField(label="Polarizer Illumination", required=False)
    polarization_x_polarizer_observation = forms.CharField(label="Polarizer Observation", required=False)
    polarization_x_rejection_illumination = forms.CharField(label="Rejection Illumination", required=False)
    polarization_x_rejection_observation = forms.CharField(label="Rejection Observation", required=False)
    polarization_x_angle_illumination = forms.CharField(label="Angle Illumination", required=False)
    polarization_x_angle_observation = forms.CharField(label="Angle Observation", required=False)
    polarization_x_comments = forms.CharField(label="Comments", required=False)
    spatial_x_observation_mode = forms.ChoiceField(label="Observation Mode", required=False, choices=SPATIAL_OBSERVATION_MODE)
    spatial_x_unit = forms.ChoiceField(label="Unit", choices=SPATIAL_UNIT, required=False)
    spatial_x_objective = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'auto_fill': 'False',
                                   'placeholder': 'x10'}))
    spatial_x_spots_number = forms.CharField(required=False, label="Spots Number")
    spatial_x_sampling_x = forms.CharField(required=False, label="Sampling X")
    spatial_x_sampling_y = forms.CharField(required=False, label="Sampling Y")
    spatial_x_measures_x = forms.CharField(required=False, label="Measures X")
    spatial_x_measures_y = forms.CharField(required=False, label="Measures Y")
    spatial_x_extent_x = forms.CharField(required=False, label="Extent X")
    spatial_x_extent_y = forms.CharField(required=False, label="Extent Y")
    resolution_x_width = forms.CharField(required=False, label="Width")
    resolution_x_width_error = forms.CharField(required=False, label="Width Error")  
    resolution_x_position = forms.CharField(required=False, label="Position")  
    spatial_x_comments = forms.CharField(required=False, label="Comments")
    experiment_x_comments = forms.CharField(required=False, widget= forms.TextInput
                           (attrs={'parent_tag':'experiment',
                                   'name': 'comments',
                                   'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    preview_x_x = forms.CharField(required=False, label="X")
    preview_x_y = forms.CharField(required=False, label="Y")
    preview_x_y2 = forms.CharField(required=False, label="Y2")
    preview_x_filename = forms.CharField(required=False, label="Filename")
    image_x_filename = forms.CharField(required=False, label="Filename")
    image_x_caption = forms.CharField(required=False, label="Caption", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    documentation_x_name = forms.CharField(required=False, label="Name")
    documentation_x_filename = forms.CharField(required=False, label="Filename")
    publications_x_publication_uid = forms.CharField(required=False, label="Publication UID")
    experiment_x_publication_comments = forms.CharField(required=False, label="Publication Comments")
    sponsor_x_acronym = forms.CharField(required=False, label="Acronym")
    sponsor_x_name = forms.CharField(required=False, label="Name")
    sponsor_x_award = forms.CharField(required=False, label="Award")
    spectrum_x_import_mode = forms.ChoiceField(choices=SPECTRUM_IMPORT_MODE, required=False, label="Import Mode")
    spectrum_x_uid = forms.CharField(required=False, label="UID")
    spectrum_x_experiment_type = forms.ChoiceField(choices=SPECTRUM_EXPERIMENT_TYPE, required=False, label="Experiment Type")
    spectrum_x_chronologically_ordered = forms.ChoiceField(choices=SPECTRUM_EXPERIMENT_TYPE, required=False, label="Chronologically Ordered")
    spectrum_x_previous_spectrum_uid = forms.CharField(required=False, label="Previous Spectrum UID")
    spectrum_x_title = forms.CharField(required=False, label="Title")
    spectrum_x_type = forms.ChoiceField(choices=SPECTRUM_TYPE, required=False, label="Type")
    spectrum_x_intensity_unit = forms.ChoiceField(choices=SPECTRUM_INTENSITY_UNIT, required=False, label="Intensity Unit")
    spectrum_x_reference_position = forms.CharField(required=False, label="Reference Position")
    reference_spectra_x_spectrum_uid = forms.CharField(required=False, label="Spectrum UID", widget= forms.TextInput
                           (attrs={'auto_fill': 'False',
                                   'placeholder': 'SPECTRUM_AB_yyyymmdd_123'}))
    spectrum_x_model_parameters = forms.CharField(required=False, label="Model Parameters")
    sample_x_uid = forms.CharField(required=False, label="UID")
    sample_x_changes = forms.CharField(required=False, label="Changes")
    sample_x_comments = forms.CharField(required=False, label="Comments")
    primary_constituent_x_constituent_uid = forms.CharField(required=False, label="Constituent UID", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    primary_constituent_x_constituent_comments = forms.CharField(required=False, label="Constituent Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    parameters_instrument_x_instrument_uid = forms.CharField(required=False, label="Instrument UID", widget= forms.TextInput
                           (attrs={'placeholder': 'INSTRU_InstrumentName_Technique_LabAcronym'}))
    range_x_min = forms.CharField(required=False, label="Min")
    range_x_max = forms.CharField(required=False, label="Max")
    spectrum_x_date_begin = forms.CharField(required=False, label="Date Begin", widget= forms.TextInput
                           (attrs={'auto_fill': 'NULL',
                                   'placeholder': 'NULL'}))
    spectrum_x_time_begin = forms.CharField(required=False, label="Time Begin")
    spectrum_x_date_end = forms.CharField(required=False, label="Date End")
    spectrum_x_time_end = forms.CharField(required=False, label="Time End")
    previous_version_x_status = forms.CharField(required=False, label="Status")
    previous_version_x_comments = forms.CharField(required=False, label="Comments")
    previous_version_x_new_spectrum_uid = forms.CharField(required=False, label="New Spectrum UID")
    spectrum_x_history = forms.CharField(required=False, label="History", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    spectrum_x_analysis = forms.CharField(required=False, label="Analysis")
    spectrum_x_quality_flag = forms.ChoiceField(required=False, choices=SPECTRUM_QUALITY_FLAG)
    validators_x_experimentalist_uid = forms.CharField(required=False, label="Experimentalist UID")
    spectrum_x_comments = forms.CharField(required=False, label="Comments")
    publications_x_publication_uid = forms.CharField(required=False, label="Publication UID")
    spectrum_x_publication_comments = forms.CharField(required=False, label="Publication Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))
    parameter_x_type = forms.ChoiceField(choices=PARAMETER_TYPE, required=False, label="Type")
    parameter_x_format = forms.ChoiceField(choices=PARAMTER_FORMAT, required=False, label="Format")
    parameter_x_header_lines_number = forms.CharField(required=False, label="Header Lines Number")
    file_x_filename = forms.CharField(required=False, label="Filename")
    spectrum_x_export_filename = forms.CharField(required=False, label="Export Filename")
    experiment_x_preview_flag = forms.ChoiceField(choices=SPECTRUM_EXPERIMENT_TYPE, required=False, label="Flag")

    band_x_position_min = forms.CharField(required=False, label="Position Min")
    band_x_position_peak = forms.CharField(required=False, label="Position Peak")
    band_x_position_max = forms.CharField(required=False, label="Position Max")
    band_x_peak_intensity_relative = forms.CharField(required=False, label="Peak Intensity relative")
    band_x_primary_constituent_uid = forms.CharField(required=False, label="Primary Constituent UID")
    band_x_primary_specie_uid = forms.CharField(required=False, label="Primary Specie UID")
    transition_chemical_bonds_x_chemical_bond_uid = forms.CharField(required=False, label="Chemical Bond UID")
    band_x_transition_assignment = forms.CharField(required=False, label="Transition Assignment")
    band_x_vibration_mode = forms.ChoiceField(choices=VIBRATION_MODE, required=False, label="Vibration Mode")
    band_x_rotation_mode = forms.ChoiceField(choices=ROTATION_MODE, required=False, label="Rotation Mode")
    band_x_phonon_mode = forms.ChoiceField(choices=PHONON_MODE, required=False, label="Phonon Mode")
    band_x_label = forms.CharField(required=False, label="Label")
    band_x_comments = forms.CharField(required=False, label="Comments", widget= forms.TextInput
                           (attrs={'auto_fill': '<![CDATA[]]>',
                                   'placeholder': '<![CDATA[]]>'}))

    def __init__(self, *args, **kwargs):
                session = kwargs.pop('session', 0)
                array = []
                database_uid_counter = 0
                experimentalist_uid_counter = 0
                type_counter = 0
                if len(session) != 0:
                        for i in session:
                                array.append(i)
                        database_uid_counter = array.count('owner_databases_x_database_uid')
                        experimentalist_uid_counter = array.count('experimentalists_x_experimentalist_uid')
                        type_counter = array.count('types_x_type')

                super(InsertExperimentForm, self).__init__(*args, **kwargs)

                # correct all to True
                for index in range(int(database_uid_counter)):
                        string_index = str(index+1)
                        self.fields['owner_databases_x_database_uid_{index}'.format(index=index)] = \
                                forms.CharField(required=False, label="Owner Databases "+string_index)
                for index in range(int(experimentalist_uid_counter)):
                        string_index = str(index+1)
                        self.fields['owner_databases_x_database_uid_{index}'.format(index=index)] = \
                                forms.CharField(required=False, label="Experimentalist UID "+string_index)
                for index in range(int(type_counter)):
                        string_index = str(index+1)
                        self.fields['types_x_type_{index}'.format(index=index)] = \
                                forms.ChoiceField(required=False, choices=TYPES_CHOICES, label="Type "+string_index)


class ContactForm(forms.Form):
    """
    Contact email form
    """
    name = forms.CharField(required=True)
    email_address = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class UploadFileForm(forms.Form):
    file = forms.FileField()

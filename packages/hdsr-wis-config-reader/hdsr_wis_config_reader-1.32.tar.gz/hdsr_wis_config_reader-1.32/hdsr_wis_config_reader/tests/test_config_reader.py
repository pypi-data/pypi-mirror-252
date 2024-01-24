from hdsr_pygithub import GithubDirDownloader
from hdsr_wis_config_reader import constants
from hdsr_wis_config_reader.readers.config_reader import FewsConfigReader
from hdsr_wis_config_reader.tests.fixtures import fews_config_local
from hdsr_wis_config_reader.tests.helpers import _remove_dir_recursively
from pathlib import Path

import datetime
import logging
import pandas as pd  # noqa pandas comes with geopandas
import pytest


# silence flake8
fews_config_local = fews_config_local

logger = logging.getLogger(__name__)


expected_df_parameter_column_names = [
    "DESCRIPTION",
    "GROUP",
    "ID",
    "NAME",
    "PARAMETERTYPE",
    "SHORTNAME",
    "UNIT",
    "USESDATUM",
    "VALUERESOLUTION",
]

KNOWN_LOC_SETS_NONE = [
    "AFVOERGEBIEDEN",
    "AFVOERGEBIEDEN_AANVOER",
    "AFVOERGEBIEDEN_AFVOER",
    "BEGROEIINGSMONITORING_ERGKRAP",
    "BEGROEIINGSMONITORING_KRAP",
    "BEGROEIINGSMONITORING_NORMAAL",
    "BEGROEIINGSMONITORING_RUIM",
    "BEGROEIINGSMONITORING_XRUIM",
    "BEGROEIINGSTRAJECTEN",
    "BEG_RAYON",
    "BEMALINGSGEBIEDEN",
    "BEREKEND_DEBIET_NT",
    "BOEZEMWATERSYSTEMEN",
    "DEBIETBEREKENING",
    "DEBIETBEREKENING_Inlaat",
    "DEBIETBEREKENING_Kantelstuw",
    "DEBIETBEREKENING_Overlaat",
    "DEBIETBEREKENING_Pomp",
    "DEBIETBEREKENING_Pomp_gF",
    "DEBIETBEREKENING_Pomp_sF",
    "DEBIETBEREKENING_Schuif",
    "DEBIETBEREKENING_TOTAAL",
    "DEBIETBEREKENING_TOTAAL_MIN",
    "DEBIETBEREKENING_TOTAAL_PLUS",
    "DEBIETBEREKENING_Vijzel",
    "DEBIETBEREKENING_Vispassage",
    "GRONDWATERMEETPUNTEN_DINO",
    "HDSRNEERSLAG_15M",
    "HDSRNEERSLAG_5M",
    "HERHALINGSTIJDEN.OW",
    "Langsprofiel_Amerongerwetering",
    "Langsprofiel_Amsterdam-Rijnkanaal",
    "Langsprofiel_Boezem_AGV",
    "Langsprofiel_Caspargouwse_Wetering",
    "Langsprofiel_Doorslag-Gekanaliseerde_Hollandse_IJssel",
    "Langsprofiel_Dubbele_Wiericke",
    "Langsprofiel_Grecht",
    "Langsprofiel_Kromme_Rijn",
    "Langsprofiel_Langbroekerwetering",
    "Langsprofiel_Lange_Linschoten_tm_Jaap_Bijzerwetering",
    "Langsprofiel_Leidsche_Rijn",
    "Langsprofiel_Merwedekanaal",
    "Langsprofiel_Oude_Rijn_boezem_Oost",
    "Langsprofiel_Oude_Rijn_boezem_West",
    "Langsprofiel_Schalkwijkse_wetering",
    "Langsprofiel_Stadswater_Utrecht_en_Vecht",
    "MODULES",
    "OPVLWATER_HFDLOC_HSTREEF1",
    "OPVLWATER_HFDLOC_HSTREEF1_NONEQ",
    "OPVLWATER_HFDLOC_HSTREEF1_NONEQ_NOVALID",
    "OPVLWATER_HFDLOC_HSTREEF1_NONEQ_VALID",
    "OPVLWATER_HFDLOC_HSTREEF2",
    "OPVLWATER_HFDLOC_HSTREEF2_NOVALID",
    "OPVLWATER_HFDLOC_HSTREEF2_VALID",
    "OPVLWATER_HFDLOC_HSTREEF3",
    "OPVLWATER_HFDLOC_HSTREEF3_NOVALID",
    "OPVLWATER_HFDLOC_HSTREEF3_VALID",
    "OPVLWATER_HFDLOC_KENTERMEETDATA",
    "OPVLWATER_HFDLOC_Q2R",
    "OPVLWATER_HFDLOC_Q2S",
    "OPVLWATER_HFDLOC_Q3R",
    "OPVLWATER_HFDLOC_Q3S",
    "OPVLWATER_HFDLOC_QR",
    "OPVLWATER_HFDLOC_QS",
    "OPVLWATER_HFDLOC_QS_NONEQ",
    "OPVLWATER_HFDLOC_WR_NONEQ",
    "OPVLWATER_HFDLOC_WS_NONEQ",
    "OPVLWATER_INLATEN_HH_NONEQ",
    "OPVLWATER_INLATEN_POS1_NONEQ",
    "OPVLWATER_PEILSCHALEN_AFVOERGEBIED",
    "OPVLWATER_PEILSCHALEN_PEILGEBIED",
    "OPVLWATER_SUBLOC_AFSLUITER",
    "OPVLWATER_SUBLOC_DD0",
    "OPVLWATER_SUBLOC_DDH",
    "OPVLWATER_SUBLOC_DDL",
    "OPVLWATER_SUBLOC_DEBIETEN",
    "OPVLWATER_SUBLOC_DEBIETEN_AANVOER",
    "OPVLWATER_SUBLOC_DEBIETEN_AFVOER",
    "OPVLWATER_SUBLOC_DEBIETEN_HBEN",
    "OPVLWATER_SUBLOC_DEBIETEN_HBOV",
    "OPVLWATER_SUBLOC_DEBIETEN_NOHBEN",
    "OPVLWATER_SUBLOC_DEBIETEN_NOHBOV",
    "OPVLWATER_SUBLOC_DEBIETMETER",
    "OPVLWATER_SUBLOC_ES",
    "OPVLWATER_SUBLOC_ES2",
    "OPVLWATER_SUBLOC_ES2_NONEQ",
    "OPVLWATER_SUBLOC_ES_NONEQ",
    "OPVLWATER_SUBLOC_FR",
    "OPVLWATER_SUBLOC_FR_NONEQ",
    "OPVLWATER_SUBLOC_FR_NONEQ_NOVALID",
    "OPVLWATER_SUBLOC_FR_NONEQ_VALID",
    "OPVLWATER_SUBLOC_HBEN",
    "OPVLWATER_SUBLOC_HBENPS",
    "OPVLWATER_SUBLOC_HBOV",
    "OPVLWATER_SUBLOC_HBOVPS",
    "OPVLWATER_SUBLOC_HH1",
    "OPVLWATER_SUBLOC_HH1_NONEQ",
    "OPVLWATER_SUBLOC_HH1_NONEQ_NOVALID",
    "OPVLWATER_SUBLOC_HH1_NONEQ_VALID",
    "OPVLWATER_SUBLOC_HK",
    "OPVLWATER_SUBLOC_HK_NONEQ",
    "OPVLWATER_SUBLOC_HK_NONEQ_NOVALID",
    "OPVLWATER_SUBLOC_HK_NONEQ_VALID",
    "OPVLWATER_SUBLOC_HM1",
    "OPVLWATER_SUBLOC_HM1_NONEQ",
    "OPVLWATER_SUBLOC_HM1_NONEQ_NOVALID",
    "OPVLWATER_SUBLOC_HM1_NONEQ_VALID",
    "OPVLWATER_SUBLOC_HSTUUR1",
    "OPVLWATER_SUBLOC_HSTUUR1_NONEQ",
    "OPVLWATER_SUBLOC_HSTUUR1_NONEQ_NOVALID",
    "OPVLWATER_SUBLOC_HSTUUR1_NONEQ_VALID",
    "OPVLWATER_SUBLOC_HSTUUR2",
    "OPVLWATER_SUBLOC_HSTUUR2_NONEQ",
    "OPVLWATER_SUBLOC_HSTUUR2_NONEQ_NOVALID",
    "OPVLWATER_SUBLOC_HSTUUR2_NONEQ_VALID",
    "OPVLWATER_SUBLOC_HSTUUR3",
    "OPVLWATER_SUBLOC_HSTUUR3_NONEQ",
    "OPVLWATER_SUBLOC_HSTUUR3_NONEQ_NOVALID",
    "OPVLWATER_SUBLOC_HSTUUR3_NONEQ_VALID",
    "OPVLWATER_SUBLOC_IB0",
    "OPVLWATER_SUBLOC_IB0_NONEQ",
    "OPVLWATER_SUBLOC_IBH",
    "OPVLWATER_SUBLOC_IBH_NONEQ",
    "OPVLWATER_SUBLOC_IBL",
    "OPVLWATER_SUBLOC_IBL_NONEQ",
    "OPVLWATER_SUBLOC_KROOSHEK",
    "OPVLWATER_SUBLOC_NO_Q_HMAX",
    "OPVLWATER_SUBLOC_POMPVIJZEL",
    "OPVLWATER_SUBLOC_POS1",
    "OPVLWATER_SUBLOC_POS1_NONEQ",
    "OPVLWATER_SUBLOC_POS1_NONEQ_NOVALID",
    "OPVLWATER_SUBLOC_POS1_NONEQ_VALID",
    "OPVLWATER_SUBLOC_POS2",
    "OPVLWATER_SUBLOC_POS2_NONEQ",
    "OPVLWATER_SUBLOC_POS2_NONEQ_NOVALID",
    "OPVLWATER_SUBLOC_POS2_NONEQ_VALID",
    "OPVLWATER_SUBLOC_QIPCL",
    "OPVLWATER_SUBLOC_QIPCL_NONEQ",
    "OPVLWATER_SUBLOC_QM1",
    "OPVLWATER_SUBLOC_QM1_NONEQ",
    "OPVLWATER_SUBLOC_Q_HMAX",
    "OPVLWATER_SUBLOC_Q_NORM",
    "OPVLWATER_SUBLOC_RPM",
    "OPVLWATER_SUBLOC_RPM_NOVALID",
    "OPVLWATER_SUBLOC_RPM_VALID",
    "OPVLWATER_SUBLOC_SCHUIF",
    "OPVLWATER_SUBLOC_STUW",
    "OPVLWATER_SUBLOC_SWM",
    "OPVLWATER_SUBLOC_SWM_AANVOER",
    "OPVLWATER_SUBLOC_SWM_AFVOER",
    "OPVLWATER_SUBLOC_VISPASSAGE",
    "OPVLWATER_SUBLOC_VISSCHUIF",
    "OPVLWATER_WATERSTANDEN",
    "OPVLWATER_WATERSTANDEN_AFVOERGEBIED",
    "OPVLWATER_WATERSTANDEN_CACB",
    "OPVLWATER_WATERSTANDEN_DIFF",
    "OPVLWATER_WATERSTANDEN_GAPFILLING",
    "OPVLWATER_WATERSTANDEN_NOVALID",
    "OPVLWATER_WATERSTANDEN_PEILGEBIED",
    "OPVLWATER_WATERSTANDEN_PEILSCHAAL",
    "OPVLWATER_WATERSTANDEN_RBG",
    "OPVLWATER_WATERSTANDEN_VALID",
    "OPVLWATER_WQLOC_CONDUCT",
    "OPVLWATER_WQLOC_CONDUCT_MICRO",
    "OPVLWATER_WQLOC_CONDUCT_MICRO_NONEQ",
    "OPVLWATER_WQLOC_CONDUCT_MILLI",
    "OPVLWATER_WQLOC_CONDUCT_MILLI_NONEQ",
    "OPVLWATER_WQLOC_CONDUCT_NONEQ",
    "OPVLWATER_WQLOC_O2",
    "OPVLWATER_WQLOC_O2_NONEQ",
    "OPVLWATER_WQLOC_TC",
    "OPVLWATER_WQLOC_TC_NONEQ",
    "OPVLWATER_WQLOC_TROEB",
    "OPVLWATER_WQLOC_TROEB_NONEQ",
    "OPVL_GROND_WATER_WATERSTANDEN",
    "PEILGEBIEDEN",
    "RIOOLGEMALEN_EN_RWZIS",
    "STROOMSNELHEID",
    "SWMGEBIEDEN_AANVOER",
    "SWMGEBIEDEN_AFVOER",
    "SWMGEBIEDEN_NETTO",
    "SWMHDSRGEBIEDEN",
    "SWMSUBGEBIEDEN",
    "SWMSUBGEBIEDEN_AANAFVOER",
    "WATERSCHAPPEN",
]

PRODUCTION_LOC_SETS_RESULT_IN_NONE = [
    "ALLE_GEBIEDEN",
    "DEBIETBEREKENING_MetDebietmeter",
    "DEBIETBEREKENING_Pomp_sF_VF",
    "MODULES_GRID",
    "MODULES_SCALAIR",
    "OPVLWATER_HFDLOC_HSTREEF1_NOVALID",
    "OPVLWATER_HFDLOC_HSTREEF1_VALID",
    "OPVLWATER_SUBLOC_DEBIETMETER_MINUS_KW43131x",
    "OPVLWATER_SUBLOC_DEBIET_NEG",
    "OPVLWATER_SUBLOC_DEBIET_POS",
    "OPVLWATER_SUBLOC_HH",
    "OPVLWATER_SUBLOC_HH_NONEQ",
    "OPVLWATER_SUBLOC_HH_NONEQ_NOVALID",
    "OPVLWATER_SUBLOC_HH_NONEQ_VALID",
    "OPVLWATER_SUBLOC_HSTUUR1_NOVALID",
    "OPVLWATER_SUBLOC_HSTUUR1_VALID",
    "OPVLWATER_SUBLOC_HSTUUR2_NOVALID",
    "OPVLWATER_SUBLOC_HSTUUR2_VALID",
    "OPVLWATER_SUBLOC_HSTUUR3_NOVALID",
    "OPVLWATER_SUBLOC_HSTUUR3_VALID",
    "OPVLWATER_SUBLOC_SS",
    "OPVLWATER_SUBLOC_TT",
    "OPVLWATER_SUBLOC_TT_NOVALID",
    "OPVLWATER_SUBLOC_TT_VALID",
    "OPVLWATER_WATERSTANDEN_AUTO_RPS",
    "OPVLWATER_WATERSTANDEN_NOPEILSCHAAL",
    "PEILAFVOER_GEBIEDEN",
]

PRODUCTION_LOC_SETS_RESULT_IN_9999_ERROR = ["OPVLWATER_INLATEN"]


def _validate_loc_sets(fews_config, loc_sets):
    for loc_set in loc_sets:
        if loc_set == "OPVLWATER_SUBLOC":
            print(1)

        try:
            df = fews_config.get_locations(location_set_key=loc_set)
        except Exception as err:
            assert loc_set in PRODUCTION_LOC_SETS_RESULT_IN_9999_ERROR, f"loc_set {loc_set}: {err}"
            continue

        if loc_set in PRODUCTION_LOC_SETS_RESULT_IN_NONE:
            continue

        if df is None:
            assert loc_set in KNOWN_LOC_SETS_NONE, f"loc_set {loc_set} not in KNOWN_LOC_SETS_NONE"
            continue

        assert not df.empty, f"loc_set {loc_set} results in empty dataframe"


@pytest.mark.second_to_last  # run this test second_to_last as it takes long (~3 min)!
def test_local_fews_config(fews_config_local):
    fews_config = fews_config_local
    fews_config.MapLayerFiles  # noqa
    fews_config.RegionConfigFiles  # noqa
    fews_config.IdMapFiles  # noqa
    loc_sets = fews_config.location_sets

    _validate_loc_sets(fews_config, loc_sets)

    # test FewsConfigReader parameters (special case that works different for old configs and new configs)
    df_parameters = fews_config_local.get_parameters()
    assert isinstance(df_parameters, pd.DataFrame)
    assert len(df_parameters) > 100
    assert sorted(df_parameters.columns) == expected_df_parameter_column_names


@pytest.mark.last  # run this test last as it takes long (~3 min)!
def test_github_fews_config_prd():
    target_dir = Path("FEWS/Config")
    github_downloader = GithubDirDownloader(
        target_dir=target_dir,
        only_these_extensions=[".csv", ".xml"],
        allowed_period_no_updates=datetime.timedelta(weeks=52 * 2),
        repo_name=constants.GITHUB_WIS_CONFIG_REPO_NAME,
        branch_name=constants.GITHUB_WIS_CONFIG_BRANCH_NAME,
        repo_organisation=constants.GITHUB_ORGANISATION_NAME,
    )
    download_dir = github_downloader.download_files(use_tmp_dir=True)
    config_dir = download_dir / target_dir
    fews_config = FewsConfigReader(path=config_dir)
    assert fews_config.path == config_dir

    # test FewsConfigReader
    fews_config.MapLayerFiles  # noqa
    fews_config.RegionConfigFiles  # noqa
    fews_config.IdMapFiles  # noqa
    loc_sets = fews_config.location_sets

    _validate_loc_sets(fews_config, loc_sets)

    # test FewsConfigReader parameters (special case that works different for old configs and new configs)
    df_parameters = fews_config.get_parameters()
    assert "VALUERESOLUTION" in df_parameters.columns
    assert len(df_parameters) > 100

    # clean up
    _remove_dir_recursively(dir_path=download_dir)

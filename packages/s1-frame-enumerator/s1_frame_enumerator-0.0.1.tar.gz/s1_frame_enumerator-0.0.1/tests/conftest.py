import json
from pathlib import Path

import geopandas as gpd
import pytest


@pytest.fixture(scope='session')
def test_data_dir():
    data_dir = Path(__file__).resolve().parent / 'data'
    return data_dir


@pytest.fixture(scope='session')
def asf_results_from_query_by_frame():
    data_dir = Path(__file__).resolve().parent / 'data'

    def query_asf_by_frame(frame_id):
        return json.load(open(data_dir / f'frame_{frame_id}_asf_results.json'))

    return query_asf_by_frame


@pytest.fixture(scope='session')
def sample_stack():
    data_dir = Path(__file__).resolve().parent / 'data'
    df = gpd.read_file(data_dir / 'sample_stack_137.geojson')
    return df


@pytest.fixture(scope='session')
def CA_20210915_resp():
    data_dir = Path(__file__).resolve().parent / 'data'
    json_data = json.load(open(data_dir / 'CA-subset_2021-09-14_asf_results.json'))
    return json_data

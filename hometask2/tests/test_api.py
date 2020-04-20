import pytest

from tests.base_api import BaseCase


@pytest.mark.API
class TestApi(BaseCase):

    def test_create_new_segment(self, create_temp_segment_with_api):
        self.api_client = create_temp_segment_with_api[0]
        tmp_segment_id = create_temp_segment_with_api[1]
        flag = False
        for segment in self.api_client.get_segments_list():
            if segment['id'] == tmp_segment_id:
                flag = True
        assert flag

    def test_delete_segment(self, create_temp_segment_with_api):
        self.api_client = create_temp_segment_with_api[0]
        tmp_segment_id = create_temp_segment_with_api[1]
        self.api_client.delete_segment(tmp_segment_id)
        for segment in self.api_client.get_segments_list():
            assert not segment['id'] == tmp_segment_id

    def test_delete_all_my_segments(self, create_temp_segment_with_api):
        self.api_client = create_temp_segment_with_api[0]
        self.api_client.create_new_segment('Test2')
        self.api_client.delete_all_segments(self.api_client.get_segments_list())
        assert self.api_client.get_segments_list() == []

import mock
import unittest
import request_augment_service as ras

class TestAdRequestAugmentService(unittest.TestCase):

    @mock.patch('request_augment_service.get_site_demographics', return_value={'female_pct': 45.5, 'male_pct': 55.5})
    def test_inject_site_demographics_200_response(self, mock_site_demo):
        input_req = {
            'site': {
                'id': 'id1'
            }
        }
        expected = {
            'site': {
                'id': 'id1',
                'demographics': {
                    'female_pct': 45.5,
                    'male_pct': 55.5
                }
            }
        }
        self.assertEqual(expected, ras.inject_site_demographics(input_req))
        mock_site_demo.assert_called_with('id1')

    @mock.patch('request_augment_service.get_site_demographics', return_value=None)
    def test_inject_site_demographics_400_response(self, mock_site_demo):
        input_req = {
            'site': {
                'id': 'id1'
            }
        }
        self.assertEqual(input_req, ras.inject_site_demographics(input_req))
        mock_site_demo.assert_called_with('id1')

    @mock.patch('request_augment_service.publisher_details_by_site_id', return_value={'id': 'pub1', 'name': 'good pub'})
    def test_inject_publisher_details_200_response(self, mock_get_pub):
        input_req = {
            'site': {
                'id': 'id1'
            }
        }
        expected = {
            'site': {
                'id': 'id1',
                'publisher': {
                    'id': 'pub1',
                    'name': 'good pub'
                }
            }
        }
        self.assertEqual(expected, ras.inject_publisher_details(input_req))
        mock_get_pub.assert_called_with('id1')

    @mock.patch('request_augment_service.publisher_details_by_site_id', return_value=None)
    def test_inject_publisher_details_400_response(self, mock_get_pub):
        input_req = {
            'site': {
                'id': 'id1'
            }
        }
        self.assertEqual(input_req, ras.inject_publisher_details(input_req))
        mock_get_pub.assert_called_with('id1')

    @mock.patch('request_augment_service.get_country_by_device_ip', return_value='US')
    def test_inject_device_country_200_response(self, mock_get_pub):
        input_req = {
            'device': {
                'ip': 'us based ip'
            }
        }
        expected = {
            'device': {
                'ip': 'us based ip',
                'country': 'US'
            }
        }
        self.assertEqual(expected, ras.inject_device_country(input_req))
        mock_get_pub.assert_called_with('us based ip')

    @mock.patch('request_augment_service.get_country_by_device_ip', return_value=None)
    def test_inject_device_country_400_response(self, mock_get_pub):
        input_req = {
            'device': {
                'ip': 'us based ip'
            }
        }
        self.assertEqual(input_req, ras.inject_device_country(input_req))
        mock_get_pub.assert_called_with('us based ip')



if __name__ == '__main__':
    unittest.main()
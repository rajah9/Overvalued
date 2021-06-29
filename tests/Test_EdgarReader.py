import logging
import sys
from unittest import TestCase, mock, skip

from EdgarReader import EdgarReader, Company
from edgar import Edgar

sys.path.insert(0, '../../Utilities') # Fix for where your Utilities dir is.
from LogitUtil import logit

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""
Interesting Python features:
"""

def mock_edgar_company_match(name: str, top: int) -> list:
    # Following is a search for "APPLE COMPUTER" and top 5.
    ans = [
        {'company_name': 'APPLE COMPUTER INC/ FA', 'cik': '0000320193', 'score': 100},
        {'company_name': 'APPLE COMPUTER INC', 'cik': '0000320193', 'score': 100},
        {'company_name': 'E CO', 'cik': '0001427543', 'score': 100},
        {'company_name': 'APEX COMPUTER SOLUTIONS', 'cik': '0001327464', 'score': 86},
        {'company_name': 'APPLIED COMPUTATIONAL TECHNOLOGIES LLC', 'cik': '0001457108', 'score': 86},
    ]
    return ans

_ONE_TO_MATCH = 1

class test_PythonImport(TestCase):
    def setUp(self):
        self.er = EdgarReader()

    @skip("takes too long")
    @logit()
    def test_companies_by_name(self):
        # Test 1, normal name
        name = "APPLE COMPUTER"
        top = 5
        # with mock.patch('Edgar.match_company_by_company_name') as mocked_match:
        #     mocked_match.return_value = mock_edgar_company_match(name, top)
        #     mocked_er = EdgarReader()
        #     act1 = mocked_er.companies_by_name(name="APPLE COMPUTER", top=5)
        act1 = self.er.companies_by_name(name="APPLE COMPUTER", top=5)

        exp1 = mock_edgar_company_match(name, top)
        self.assertEqual(exp1[_ONE_TO_MATCH], act1[_ONE_TO_MATCH])

    @logit()
    def test_company_property(self):
        # Test 1, normal company
        name = "APPLE COMPUTER"
        top = 5
        d = mock_edgar_company_match(name, top)[_ONE_TO_MATCH]
        self.er.company = (d['company_name'], d['cik'])
        exp1 = Company(name=d['company_name'], cik=d['cik'])
        act1 = self.er.company
        self.assertEqual(exp1.name, act1.name, "Fail test 1 (name)")
        self.assertEqual(exp1.cik, act1.cik, "Fail test 1 (cik)")
        # Test 2, company name and cik do not match
        d1 = mock_edgar_company_match(name, top)[_ONE_TO_MATCH]
        d2 = mock_edgar_company_match(name, top)[_ONE_TO_MATCH + 1]
        self.er.company = (d1['company_name'], d2['cik']) # company name of d1 does not match cik of d2
        exp2 = Company(name=d1['company_name'], cik=d2['cik'])
        act2 = self.er.company
        self.assertEqual(exp2.name, act2.name, "Fail test 2 (name)")
        self.assertEqual(exp2.cik, act2.cik, "Fail test 2 (cik)")

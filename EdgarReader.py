from edgar import Edgar, Company
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""
Interesting Python features:
* Setter for company takes two values, as in https://stackoverflow.com/questions/18714262/property-setter-with-multiple-values
* 
"""
class EdgarReader:
    def __init__(self):
        self.edgar = Edgar()
        self._company = None

    @property
    def company(self) -> Company:
        return self._company

    @company.setter
    def company(self, val):
        try:
            company_name, cik = val
            logger.debug(f'Setting company to {company_name} with a cik of {cik}.')
            ans = Company(company_name, cik)
        except ValueError:
            logger.warning(f'Must pass an iterable with two values (company name and cik).')
        else:
            self._company = ans

    def companies_by_name(self, name :str, top: int = 5) -> list:
        """
        Find the <top> companies matching the given name.
        :param name: name of company to match
        :param top: int of how many to return. If None, return all of them.
        :return: dict of companies
        """
        ans = self.edgar.match_company_by_company_name(name=name, top=top)
        for i, d in enumerate(ans):
            logger.debug(f'Company {i} matching {name}: {d}')
        return ans


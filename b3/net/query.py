import base64
import datetime
import json
import requests
from b3 import datatypes, exceptions

def jsonify(obj: dict) -> str:
    return json.dumps(obj, indent=None, separators=(',', ':'))

def btoa(s: str) -> bytes:
    utf8_data   = s.encode('utf-8')
    base64_data = base64.b64encode(utf8_data)

    return base64_data.decode('utf-8')

def make_service_string(cvm_code: int, language: str) -> str:
    json_obj = {
        'codeCVM': str(cvm_code),
        'language': language
    }

    json_str   = jsonify(json_obj)
    base64_str = btoa(json_str)

    return base64_str

def query_company(cvm_code: int) -> datatypes.CompanyDetail:
    url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetDetail/' + make_service_string(cvm_code, 'pt-BR')

    response = requests.get(url)
    response = response.json()

    if len(response) == 0:
        raise exceptions.RequestError(f'no company found with CVM code {cvm_code}')

    security_codes = []

    try:
        for elem in response['otherCodes']:
            security_codes.append(datatypes.SecurityCode(elem['code'], elem['isin']))
    except KeyError:
        pass

    return datatypes.CompanyDetail(
        cnpj                    = int(response['cnpj']),
        cvm_code                = int(response['codeCVM']),
        company_name            = response['companyName'],
        company_code            = response['issuingCompany'],
        trading_name            = response['tradingName'],
        activity                = response['activity'],
        industry                = response['industryClassification'],
        market                  = response['market'],
        market_indicator        = response['marketIndicator'],
        has_bdr                 = response['hasBDR'],
        bdr_type                = response['typeBDR'],
        has_emissions           = response['hasEmissions'],
        has_quotation           = response['hasQuotation'],
        common_institution      = response['institutionCommon'],
        preferred_institution   = response['institutionPreferred'],
        status                  = response['status'],
        website                 = response['website'],
        last_date               = datetime.datetime.strptime(response['lastDate'], '%d/%m/%Y %H:%M:%S'),
        bvmf_describle_category = response['describleCategoryBVMF'],
        security_codes          = tuple(security_codes)
    )
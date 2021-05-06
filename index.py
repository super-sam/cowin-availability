from helpers import *
import concurrent.futures

def main():
    '''
    Get District ids by state (ref README.md for state_id)
    https://cdn-api.co-vin.in/api/v2/admin/location/districts/<state_id>
    '''
    districts = []  # list of tuple with district_id and age group to check, eg: [('335', ['18', '45'])]
    pincodes = []  # list of tuple with pincode and age group to check, eg: [('751003', ['18']), ('751001', ['45'])]
    argslist = []
    for districtinfo in districts:
        district = districtinfo[0]
        age_group = districtinfo[1]
        argslist.append((district, 'district', age_group))

    for pininfo in pincodes:
        pincode = pininfo[0]
        age_group = pininfo[1]
        argslist.append((pincode, 'pincode', age_group))

    results = ['Vaccine Availability']
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        result = executor.map(lambda args: find_monthly_vaccine(*args), argslist)

    for r in result:
        results.extend(r)

    # If you want to send sms then configure aws credentials in helpers.py, send_sms
    # Uncomment the below function
    # send_sms(results)


if __name__ == '__main__':
    main()

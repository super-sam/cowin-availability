import json
from datetime import datetime, timedelta
import urllib3
from enum import Enum


class AGE_GROUP(Enum):
    BOTH = "session['min_age_limit'] >= 18"
    YOUNG = "session['min_age_limit'] == 18"
    OLD = "session['min_age_limit'] == 45"


class Settings:
    __instance = None

    @staticmethod
    def get():
        if Settings.__instance is None:
            Settings()
        return Settings.__instance

    def __init__(self, check=''):
        if Settings.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            if check in [AGE_GROUP.BOTH, AGE_GROUP.YOUNG, AGE_GROUP.OLD]:
                self.check = check.value
            else:
                self.check = AGE_GROUP.BOTH.value
            Settings.__instance = self


def geturi(by='district'):
    s = Settings.get()
    if by == 'district':
        return 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={id}&date={date}'

    return 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={id}&date={date}'


def find_vaccines(date, id, by='district'):
    uri = geturi(by)
    url = uri.format(date=date, id=str(id))
    results = []
    http = urllib3.PoolManager()

    try:
        res = http.request('GET', url, headers={
            'origin': ' https://www.cowin.gov.in',
            'referer': 'https://www.cowin.gov.in/',
            'sec-fetch-mode': 'cors',
            'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
        })
        jsonData = json.loads(res.data)
        centers = jsonData['centers']
        for center in centers:
            for session in center['sessions']:
                expression = Settings.get().check
                if session['available_capacity'] > 0 and eval(expression):
                    r = "{count} {hospital} {city} {date} {age}".format(
                        count=session['available_capacity'],
                        city=center['district_name'][:3],
                        hospital=center['name'][:5],
                        date=session['date'],
                        age=session['min_age_limit']
                    )
                    print("{count} {hospital} {city} {date} {age}".format(
                        count=session['available_capacity'],
                        city=center['district_name'],
                        hospital=center['name'],
                        date=session['date'],
                        age=session['min_age_limit']
                    ))
                    results.append(r)
    except Exception as e:
        print(str(e))

    return results


def find_monthly_vaccine(id, by):
    today = datetime.today()
    results = []
    for _ in range(4):
        results.extend(find_vaccines(today.strftime('%d-%m-%Y'), id, by))
        today = today + timedelta(days=7)
    return results


def send_sms(results):
    import boto3
    if len(results) > 1:
        message = '\n'.join(results)
        client = boto3.client(
            "sns",
            aws_access_key_id='<YOUR_ACCESS_ID>',
            aws_secret_access_key='<YOUR_ACCESS_KEY>',
            region_name=""
        )
        start = 0
        while start < len(message):
            diff = len(message) - start
            end = start + diff if diff <= 160 else start + 160
            client.publish(
                PhoneNumber="<YOUR_MOBILE_NUMBER>",
                Message=message[start: end],  # 160 char limit for sms
                MessageAttributes={
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
            start = end
def send_telegram(results):
    '''
    Send Message to Telegram channel
    Steps:
    1) Create a bot with telegram bot father: https://t.me/botfather to get bot api token
    2) Create a channel
    3) Add the bot as admin to the channel
    '''
    channel_id = '<YOUR_CHANNEL_ID>'
    api_token = '<YOUR_BOT_API_TOKEN'
    

    if len(results) > 0:
        http = urllib3.PoolManager()
        start = 0
        while start < len(results) - 1:
            diff = len(results) - start
            end = start + diff if diff <= 20 else start + 20
            message = '\n'.join(results[start:end])
            url = f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id=@{channel_id}&text={message}"
            fields = {
                "chatid": f"@{channel_id}",
                "text": message
            }
            try:
                http.request('POST', url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, fields=fields)
            except Exception as e:
                print(str(e))
            start = end

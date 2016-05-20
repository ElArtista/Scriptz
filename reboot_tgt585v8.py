import requests
from lxml import html

MODEM_URL = "http://192.168.1.254"
AUTH_PAIR = ('admin', 'admin')

def main():
    print("HAi!")

    # Phase 1 (Gather the session id)
    r = requests.get(MODEM_URL)
    http_session_id = r.cookies['HTTP_SESSION_ID']
    print("Got session id: " + http_session_id)
    cks_dict = dict(HTTP_SESSION_ID=http_session_id)

    # Setup session
    s = requests.Session()
    s.auth = AUTH_PAIR
    s.cookies = requests.cookies.cookiejar_from_dict(cks_dict)

    # Next requests are in session
    with s:
        # Phase 2 (Gather the magic number)
        payload = {'be': 0, 'l0': 1, 'l1': 0, 'tid': 'RESTART'}
        r = s.get(MODEM_URL + '/cgi/b/info/restart/', params=payload)
        tree = html.fromstring(r.content)
        # Parse magic number of the response body
        magicnum = tree.xpath('//form[@name="Restart"]/input[@type="hidden" and @name="2"]/@value')[0]
        print("Got magicnum: " + str(magicnum))

        # Phase 3 (Make the reboot request)
        print("Making reboot request...")
        payload = {'be': 0, 'l0': 1, 'l1': 1, 'tid': 'RESTART'}
        form = {'0': 17, '1': "", '2': magicnum}
        r = s.post(MODEM_URL + '/cgi/b/info/restart/', params=payload, data=form)
        print("Reboot request returned: " + str(r.status_code))

if __name__ == '__main__':
    main()

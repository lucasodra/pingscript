import whois
import pandas as pd

def get_whois(ip):
    try:
        w = whois.whois(ip)
        return [
            w.get('type', ''),
            w.get('netrange', ''),
            w.get('cidr', ''),
            w.get('netname', ''),
            w.get('nethandle', ''),
            w.get('parent', ''),
            w.get('nettype', ''),
            w.get('originas', ''),
            w.get('organization', ''),
            w.get('regdate', ''),
            w.get('updated', ''),
            w.get('ref', ''),
            w.get('orgname', ''),
            w.get('orgid', ''),
            w.get('address', ''),
            w.get('city', ''),
            w.get('stateprov', ''),
            w.get('postalcode', ''),
            w.get('country', ''),
            w.get('regdate', ''),
            w.get('updated', ''),
        ] + w.get('comment', [''] * 8)
    except Exception as e:
        print(f"Error fetching WHOIS for {ip}: {e}")
        return [''] * 31

df = pd.read_csv("traceroute_output.csv")

df[['Type','NetRange','CIDR','NetName','NetHandle','Parent','NetType','OriginAS','Organization','RegDate','Updated',
    'Ref','OrgName','OrgId','Address','City','StateProv','PostalCode','Country','RegDate2','Updated2',
    'Comment1','Comment2','Comment3','Comment4','Comment5','Comment6','Comment7','Comment8', 'Comment_Link']] = df.apply(
    lambda row: get_whois(row['ip']), axis=1, result_type="expand")

df.to_csv("traceroute_with_whois.csv", index=False)

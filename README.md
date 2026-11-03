# update-route53-from-home-assistant-with-lambda
Automation built using Home Assistant to update a Route53 entry using a Lambda function

For my purpose, I wanted to host a VPN server which reflected changes based on my non-static public IP address.  I don't need any significant availability so haven't tested polling frequency, etc. and as this is a home project, I haven't explored enterprise alternatives (such as a global server load balancer or even a static IP).  You may wish to adapt this for your use case - the important part is getting Home Assistant do call a Lambda function - although in this instance, it triggers a DNS change.
N.B., I have used a token as part of a REST API call for security which on paper requires you to create a function URL with "no security".  I say "no security" as HA uses the token from Home Assistant, so it is secure but you might want to validate this covers you from a security standpoint.  Usual rules apply; follow requirements, store credentials safely, rotate frequently, no sticky notes, and so on.  If token exchange like this is deemed insufficient, then you can look to do something with SecretsManager and do a two-step auth process, use certificates, etc.  That will not be covered here.

To get started, add the 'DNS IP' integration within Home Assistant.  This should be able to show you your public IP address in the 'Integration'.  N.b., I have seen some documentation refer to the integration as 'myip' but I found it as 'DNS IP'.  

<img width="1062" height="379" alt="image" src="https://github.com/user-attachments/assets/765e28c7-9024-4ed7-90c2-b203430b2c26" />


I assume by this point, you have a Route 53 registered domain name and can create an A record for your purpose.  When you do create the A record, record the Zone ID for the domain where you want to make the change.

Once you are able to see your IP address, create a Python Lambda function (see lambda_function.py) and create environment variables with the following:

RECORD:  vpn.exampledomainname.co.uk

ZONE_ID:  {taken from Route 53}

TOKEN:  {Generate an authorisation token and save it somewhere safe}


Create a Function URL with auth type 'NONE'.  

Add the changes to secrets.yaml, configurations.yaml and automations.yaml as per the files in this GitHub repo...

That should be sufficient to work.  Validate this from Home Assistant by running at the automation traces log and seeing the correct IP address under 'Changed Variables' (and then of course, running an nslookup on your VPN address)

<img width="820" height="484" alt="image" src="https://github.com/user-attachments/assets/b8c02f74-f285-45f8-9eed-52b16e71116f" />

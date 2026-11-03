# update-route53-from-home-assistant-with-lambda
Automation built using Home Assistant to update a Route53 entry using a Lambda function

For my purpose, I wanted to host a VPN server which allowed for my non-static public IP address (and I didn't want to use a 3rd party dynamic DNS service).  I don't need any significant availability so haven't tested polling frequency, how long between an IP address change and automation running, etc. and as this is a home project, I haven't explored enterprise alternatives (such as a global server load balancer or even a static IP).  You may wish to adapt this for your use case - the important part is getting Home Assistant do call a Lambda function - although in this instance, it triggers a DNS change.
N.B., I have used a token as part of a REST API call for security which on paper requires you to create a function URL with "no security".  I say "no security" as HA uses the token from Home Assistant as a security mechanism, so it is secure but you might want to validate this covers you based on your requirements.  Usual rules apply; follow requirements, store credentials safely, rotate frequently, no sticky notes, and so on.  If token exchange like this is deemed insufficient, then you can look to do something with SecretsManager and do a two-step auth process, use certificates, etc.  That will not be covered here.

To get started, add the 'DNS IP' integration within Home Assistant.  This should be able to show you your public IP address in the 'Integration'.  N.b., I have seen some documentation refer to the integration as 'myip' but I found it as 'DNS IP'.  

<img width="1062" height="379" alt="image" src="https://github.com/user-attachments/assets/765e28c7-9024-4ed7-90c2-b203430b2c26" />


I assume by this point, you have a Route 53 registered domain name and can create an A record for your purpose.  When you do create the A record, record the Zone ID for the domain where you want to make the change.

Once you are able to see your IP address, create a Python Lambda function (see lambda_function.py) and create environment variables with the following:

RECORD:  vpn.exampledomainname.co.uk

ZONE_ID:  {taken from Route 53}

TOKEN:  {Generate an authorisation token and save it somewhere safe}


Create a Function URL with auth type 'NONE'.  

You will then need to add the permissions for your Lambda function to make DNS changes - this can be done by modifying the IAM role which Lambda creates by default for access to CloudTrail to include a policy which allows "route53:ChangeResourceRecordSets".  You can do this through the GUI or CLI if you are feeling adventurous - JSON should look like the following:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "route53:ChangeResourceRecordSets",
            "Resource": "arn:aws:route53:::hostedzone/{{Hosted zone from Route 53}}"
        }
    ]
}"

You can check the Lambda function has the rights based on your changes: 

<img width="1607" height="472" alt="image" src="https://github.com/user-attachments/assets/b5c84d47-b78d-44c9-84bf-80a3bbaa80d6" />


Now, from Home Assistant, add the changes to secrets.yaml, configurations.yaml and automations.yaml as per the files in this GitHub repo...

That should be sufficient to work.  Validate this from Home Assistant by running at the automation traces log and seeing the correct IP address under 'Changed Variables' (and then of course, running an nslookup on your VPN address)

<img width="820" height="484" alt="image" src="https://github.com/user-attachments/assets/b8c02f74-f285-45f8-9eed-52b16e71116f" />

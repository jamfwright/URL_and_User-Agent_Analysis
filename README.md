# URL_and_User-Agent_Analysis
Tests a URL for different responses based on the user-agent string.  This can help expose targeted attacks using exploits based on specific browser or OS version.

GUI based on TKinter..

Takes a URL and a text file holding the list of user-agent strings, once per line. The analyzer will request the URL with each provided
user-agent string as part of the request header.  Responses are compared with the baseline (no user-agent), any different responses are 
recorded and shown.

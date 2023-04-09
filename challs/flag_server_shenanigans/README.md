# Flag Server Shenanigans


## Concept
 - Find the Wifi AP by bruteforcing md5 from the landing page
 - Wifi perform a deauthentication attack and crack the password with format `/\d{8}/`
 - Scan the subnet or just listen on it to catch a plain TCP authentication
 - Use the credentials to access the flagserver

## Notes:
 - Router should have DHCP set for MAC addresses of ESP32s
 - There should be some indication of "last week password" near the AP
 - The flagserver and client should be on the same subnet as the AP
 
## Flag
`DCTF{n0w_y0u_kn0w_whY_w3_u53_httP5_822b731}`


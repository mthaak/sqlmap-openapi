# SQLMAP-OpenAPI

This a project to show how an OpenAPI spec can be used to execute [sqlmap](https://github.com/sqlmapproject/sqlmap)
automatically against all endpoints of a target API. Parameters are replaced by wildcards which tell sqlmap where to
inject SQL payloads to detect vulnerabilities.

## Installation

Developed for Python 3.10.

```bash
python3 -m venv venv
source venv/bin/activate
make install
```

## Usage

```bash
python3 main.py <args...>
```

## Example

Command:

```bash
python3 main.py --url https://petstore.openapi.io --openapi https://petstore3.swagger.io/api/v3/openapi.json --dry-run  
```

Output (with `DRY_RUN=True`):

```bash
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/pet" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp4495_ndf.txt" --data "{\"id\": 0, \"name\": \"*\", \"category\": {\"id\": 0, \"name\": \"123\"}, \"photoUrls\": [\"123\"], \"tags\": [{\"id\": 0, \"name\": \"123\"}], \"status\": \"123\"}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/pet" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpecumu_g2.txt" --data "{\"id\": 0, \"name\": \"123\", \"category\": {\"id\": 0, \"name\": \"*\"}, \"photoUrls\": [\"123\"], \"tags\": [{\"id\": 0, \"name\": \"123\"}], \"status\": \"123\"}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/pet" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp396yychu.txt" --data "{\"id\": 0, \"name\": \"123\", \"category\": {\"id\": 0, \"name\": \"123\"}, \"photoUrls\": [\"*\"], \"tags\": [{\"id\": 0, \"name\": \"123\"}], \"status\": \"123\"}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/pet" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpx4nqf2wf.txt" --data "{\"id\": 0, \"name\": \"123\", \"category\": {\"id\": 0, \"name\": \"123\"}, \"photoUrls\": [\"123\"], \"tags\": [{\"id\": 0, \"name\": \"*\"}], \"status\": \"123\"}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/pet" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp0_vtmnv4.txt" --data "{\"id\": 0, \"name\": \"123\", \"category\": {\"id\": 0, \"name\": \"123\"}, \"photoUrls\": [\"123\"], \"tags\": [{\"id\": 0, \"name\": \"123\"}], \"status\": \"*\"}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/pet" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpjioyc5g1.txt" --data "{\"id\": 0, \"name\": \"*\", \"category\": {\"id\": 0, \"name\": \"123\"}, \"photoUrls\": [\"123\"], \"tags\": [{\"id\": 0, \"name\": \"123\"}], \"status\": \"123\"}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/pet" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpdbhdbz75.txt" --data "{\"id\": 0, \"name\": \"123\", \"category\": {\"id\": 0, \"name\": \"*\"}, \"photoUrls\": [\"123\"], \"tags\": [{\"id\": 0, \"name\": \"123\"}], \"status\": \"123\"}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/pet" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmptwiwkdbx.txt" --data "{\"id\": 0, \"name\": \"123\", \"category\": {\"id\": 0, \"name\": \"123\"}, \"photoUrls\": [\"*\"], \"tags\": [{\"id\": 0, \"name\": \"123\"}], \"status\": \"123\"}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/pet" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmps6czw2xg.txt" --data "{\"id\": 0, \"name\": \"123\", \"category\": {\"id\": 0, \"name\": \"123\"}, \"photoUrls\": [\"123\"], \"tags\": [{\"id\": 0, \"name\": \"*\"}], \"status\": \"123\"}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/pet" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpbpvxt9do.txt" --data "{\"id\": 0, \"name\": \"123\", \"category\": {\"id\": 0, \"name\": \"123\"}, \"photoUrls\": [\"123\"], \"tags\": [{\"id\": 0, \"name\": \"123\"}], \"status\": \"*\"}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=get --url="https://petstore.openapi.io/pet/findByStatus?status=*" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpt5zrs52q.txt" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=get --url="https://petstore.openapi.io/pet/findByTags?tags=*" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpunq3rqxl.txt" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/pet/0?name=*" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpjc8htlr4.txt" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/pet/0?status=*" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp_e4zmz0s.txt" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/pet/0/uploadImage?additionalMetadata=*" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmppt93d5zi.txt" --data "abc" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/pet/0/uploadImage" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpgmobalxa.txt" --data "*" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/store/order" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpd4umr0ca.txt" --data "{\"id\": 0, \"petId\": 0, \"quantity\": 0, \"shipDate\": \"*\", \"status\": \"123\", \"complete\": false}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/store/order" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpmby2thmd.txt" --data "{\"id\": 0, \"petId\": 0, \"quantity\": 0, \"shipDate\": \"123\", \"status\": \"*\", \"complete\": false}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpf2ejk1f3.txt" --data "{\"id\": 0, \"username\": \"*\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpp_t8idgp.txt" --data "{\"id\": 0, \"username\": \"123\", \"firstName\": \"*\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpmkpetmuw.txt" --data "{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"*\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp7ho3pk1v.txt" --data "{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"*\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpi870a_8j.txt" --data "{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"*\", \"phone\": \"123\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpq2wzq1gi.txt" --data "{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"*\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user/createWithList" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp3xhsuk_k.txt" --data "[{\"id\": 0, \"username\": \"*\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}]" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user/createWithList" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpm1zikalb.txt" --data "[{\"id\": 0, \"username\": \"123\", \"firstName\": \"*\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}]" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user/createWithList" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpghgkhj1p.txt" --data "[{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"*\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}]" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user/createWithList" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpg9olw5q4.txt" --data "[{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"*\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}]" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user/createWithList" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp7_elh8ho.txt" --data "[{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"*\", \"phone\": \"123\", \"userStatus\": 0}]" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=post --url="https://petstore.openapi.io/user/createWithList" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpii_14lp7.txt" --data "[{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"*\", \"userStatus\": 0}]" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=get --url="https://petstore.openapi.io/user/login?username=*" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpt4b01jnl.txt" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=get --url="https://petstore.openapi.io/user/login?password=*" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp84ixtg3p.txt" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=get --url="https://petstore.openapi.io/user/*" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp01gmocbm.txt" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/user/*" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp1dumb8ws.txt" --data "{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/user/123" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp_xajzu03.txt" --data "{\"id\": 0, \"username\": \"*\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/user/123" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpullzlz6j.txt" --data "{\"id\": 0, \"username\": \"123\", \"firstName\": \"*\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/user/123" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpnrvn0h2v.txt" --data "{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"*\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/user/123" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpzgeg8v47.txt" --data "{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"*\", \"password\": \"123\", \"phone\": \"123\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/user/123" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpveo8q4jh.txt" --data "{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"*\", \"phone\": \"123\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=put --url="https://petstore.openapi.io/user/123" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmp1ttbsu2r.txt" --data "{\"id\": 0, \"username\": \"123\", \"firstName\": \"123\", \"lastName\": \"123\", \"email\": \"123\", \"password\": \"123\", \"phone\": \"*\", \"userStatus\": 0}" -H "Accept: application/json"
python3 ./sqlmap-dev/sqlmap.py --batch --method=delete --url="https://petstore.openapi.io/user/*" --level=1 --risk=1 --dbms=postgres --time-sec=1 --results-file="/tmp/tmpkhhyti17.txt" -H "Accept: application/json"
```

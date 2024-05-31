def pattern_checker(url, pattern_list):
    try:
        result = {}
        logger(f"{url}{pattern_list['pattern']}")
        with requests.get(f"{url}{pattern_list['pattern']}", timeout=3) as response:
            response.raise_for_status()
            if response.status_code == 200:
                result.update([('pattern', pattern_list['pattern'])])
                logger(f'HTTPS Connection checking: PASSED')
                size = sum(len(chunk) for chunk in response.iter_content(8196))
                logger(f'Actual size: {size}')
                logger(f"Server size: {pattern_list['server_ini_size']}")
                if size == int(pattern_list['server_ini_size']):
                    logger(f'Pattern Size checking: PASSED')
                else:
                    logger(f'Pattern Size checking: FAILED')
                    failed.update([('Pattern', f"{url}{pattern_list['pattern']}"), ('Size checking', 'FAILED')])
    except requests.exceptions.HTTPError as errh:
        logger(f"Http Error: {errh}")
        failed.update([('Pattern', f"{url}{pattern_list['pattern']}"), ('Http Error', errh)])
    except requests.exceptions.ConnectionError as errc:
        logger(f"Error Connecting: {errc}")
        failed.update([('Pattern', f"{url}{pattern_list['pattern']}"), ('Error Connecting', errc)])
    except requests.exceptions.Timeout as errt:
        logger(f"Timeout Error: {errt}")
        failed.update([('Pattern', f"{url}{pattern_list['pattern']}"), ('Timeout Error', errt)])
    except requests.exceptions.RequestException as err:
        logger(f"OOps: Something Else {err}")
        failed.update([('Pattern', f"{url}{pattern_list['pattern']}"), ('OOps: Something Else ', err)])

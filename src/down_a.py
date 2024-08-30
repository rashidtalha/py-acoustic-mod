import requests

local_base = '../data'

def download_argo(year, month, date, chunk_size=1024 * 100, repo=None, out_dir=None, out_file=None):
    remote_base = 'https://data-argo.ifremer.fr/geo/indian_ocean/' if repo is None else repo
    local_base = '' if out_dir is None else out_dir
    fname = f'{year}{month:02}{date:02}_prof.nc' if out_file is None else out_file

    url = f'{remote_base}{year}/{month:02}/{fname}'
    resp = requests.get(url, stream=True)

    if resp.status_code == 200:
        total_size, obtained = float(resp.headers.get('Content-Length', 0)), 0
        print(f'Downloading {fname} [{total_size / 1000000:.2f} MB] ...')
        with open(f'{local_base}{fname}', 'wb') as file:
            for data in resp.iter_content(chunk_size=chunk_size):
                obtained += file.write(data)
                print(f'{100 * obtained / total_size:.2f} %')
            err, err_text = False, 'Download complete'
    else:
        err, err_text = True, f'Failed to download {url}'
        print(f'Failed to download {url}\nStatus code: {resp.status_code}')

    return resp.status_code, err, err_text

v = download_argo(2024, 7, 20, out_dir='../data/')
print(v)

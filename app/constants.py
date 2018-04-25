import myutil.const

from urllib.parse import urljoin
# get root absolute path
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
    )
)

#URL
const.CENTER_SERVER_URL = 'http://54.149.140.244:8000'
#PATH
const.DATABASE_PATH = ROOT_DIR+""

print(const.CENTER_SERVER_URL)
import bleach
import datetime
import bbcode
import requests

API_ENDPOINT = 'https://api.xda-developers.com/v3'
FORUM_NAME = 'xda-developers'
FORUM_URL = 'https://forum.xda-developers.com'
FAVICON_PATH = '/images/2015/favicons/favicon.ico'
JSONFEED_VERSION_URL = 'https://jsonfeed.org/version/1'

XDA_POSTS_PER_THREAD = 10
FEED_POSTS_LIMIT = 20  # default to 2 pages per page

page_limit = 1 if FEED_POSTS_LIMIT // XDA_POSTS_PER_THREAD < 1 else FEED_POSTS_LIMIT // XDA_POSTS_PER_THREAD


def render_attachment(tag_name, value, options, parent, context):
    dateline = context['dateline']

    # (undocumented) append post dateline to attachment request following forum behaviour
    attachment_url = f"{API_ENDPOINT}/posts/attachment?attachmentid={value}&d={dateline}"

    attachment_request = requests.get(attachment_url)

    content_type = attachment_request.headers.get('content-type')

    if attachment_request.ok and content_type.startswith('image/'):
        return f'<img src=\"{attachment_url}\" />'
    else:
        # forum rate-limiting may return status code 410
        return f'<a rel=\"nofollow\" href=\"{attachment_url}\">{attachment_url}</a>'


# use custom parser to handle additional tags, e.g. [mention], [attach]
parser = bbcode.Parser()
parser.add_simple_formatter('mention', '@%(value)s', render_embedded=True)
parser.add_formatter('attach', render_attachment)

allowed_tags = bleach.ALLOWED_TAGS + ['br', 'img']
allowed_attributes = bleach.ALLOWED_ATTRIBUTES.copy()
allowed_attributes.update({'img': ['src']})


def get_latest_json(thread_id):
    post_request = requests.get(f"{API_ENDPOINT}/posts?threadid={thread_id}")
    response_body = post_request.json()

    # return HTTP error code
    if not post_request.ok:
        return f"Error {post_request.status_code}"

    # return API error message
    if response_body.get('error') is not None:
        return {
            'error': response_body.get('error').get('code'),
            'message': response_body.get('error').get('message')
        }

    thread_data = response_body.get('thread')

    forum_title = thread_data.get('forumtitle')

    thread_uri = thread_data.get('web_uri')

    thread_title = thread_data.get('title')

    last_page = int(response_body.get('total_pages'))

    min_page = last_page - (page_limit - 1)

    start_page = 1 if min_page < 1 else min_page

    total_results = {}

    for page in range(start_page, last_page + 1):
        page_data = requests.get(f"{API_ENDPOINT}/posts?threadid={thread_id}&page={page}").json()
        total_results[page_data['current_page']] = page_data['results']

    json_output = {
        'version': JSONFEED_VERSION_URL,
        'title': ' - '.join((FORUM_NAME, forum_title)),
        'home_page_url': FORUM_URL + thread_uri,
        'favicon': FORUM_URL + FAVICON_PATH
    }

    items_list = []

    for page, results in total_results.items():
        for result in results:
            post_url = FORUM_URL + thread_uri + '/post' + result['postid']
            time_stamp = int(result['dateline'])
            item = {
                'id': post_url,
                'url': post_url,
                'title': ' - '.join((thread_title, f"Page {page}")),
                'content_html': bleach.clean(
                    parser.format(
                        result['pagetext'],
                        dateline=time_stamp
                    ),
                    tags=allowed_tags,
                    attributes=allowed_attributes
                ),
                'date_published': datetime.datetime.utcfromtimestamp(time_stamp).isoformat('T'),
                'author': {
                    'name': result['username']
                }
            }
            items_list.append(item)

    json_output['items'] = items_list

    return json_output

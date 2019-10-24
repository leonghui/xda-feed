import datetime
import bbcode
import requests

API_ENDPOINT = 'https://api.xda-developers.com/v3'
FORUM_NAME = 'xda-developers'
FORUM_ENDPOINT = 'https://forum.xda-developers.com'
JSONFEED_VERSION_URL = 'https://jsonfeed.org/version/1'

XDA_POSTS_PER_THREAD = 10
FEED_POSTS_LIMIT = 20  # default to 2 pages per page

page_limit = 1 if FEED_POSTS_LIMIT // XDA_POSTS_PER_THREAD < 1 else FEED_POSTS_LIMIT // XDA_POSTS_PER_THREAD


def get_latest_json(thread_id):
    data = requests.get(f"{API_ENDPOINT}/posts?threadid={thread_id}").json()

    # return API error message
    if data.get('error') is not None:
        return {
            'error': data.get('error').get('code'),
            'message': data.get('error').get('message')
        }

    thread_data = data.get('thread')

    forum_title = thread_data.get('forumtitle')

    thread_uri = thread_data.get('web_uri')

    thread_title = thread_data.get('title')

    last_page = int(data.get('total_pages'))

    start_page = last_page - (page_limit - 1)

    total_results = {}

    for page in range(start_page, last_page + 1):
        page_data = requests.get(f"{API_ENDPOINT}/posts?threadid={thread_id}&page={page}").json()
        total_results[page_data['current_page']] = page_data['results']

    json_output = {
        'version': JSONFEED_VERSION_URL,
        'title': ' - '.join((FORUM_NAME, forum_title)),
        'home_page_url': FORUM_ENDPOINT + thread_uri
    }

    items_list = []

    for page, results in total_results.items():
        for result in results:
            post_id = result['postid']
            time_stamp = int(result['dateline'])
            item = {
                'id': post_id,
                'url': FORUM_ENDPOINT + thread_uri + '/post' + post_id,
                'title': ' - '.join((thread_title, f"Page {page}")),
                'content_html': bbcode.render_html(result['pagetext']),
                'date_published': datetime.datetime.utcfromtimestamp(time_stamp).isoformat('T')
            }
            items_list.append(item)

    json_output['items'] = items_list

    return json_output

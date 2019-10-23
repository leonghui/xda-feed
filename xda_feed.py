import datetime
import bbcode
import requests


API_ENDPOINT = 'https://api.xda-developers.com/v3'
FORUM_NAME = 'xda-developers'
FORUM_ENDPOINT = 'https://forum.xda-developers.com'
JSONFEED_VERSION_URL = 'https://jsonfeed.org/version/1'
POST_LIMIT = 100


def get_latest_json(thread_id):
    thread_data = requests.get(f"{API_ENDPOINT}/posts?threadid={thread_id}").json()

    if thread_data.get('error') is not None:
        return {
            'error': thread_data.get('error').get('code'),
            'message': thread_data.get('error').get('message')
        }

    forum_title = thread_data.get('thread').get('forumtitle')

    thread_uri = thread_data.get('thread').get('web_uri')

    thread_title = thread_data.get('thread').get('title')

    last_page = thread_data.get('total_pages')

    page_data = requests.get(f"{API_ENDPOINT}/posts?threadid={thread_id}&page={last_page}").json()

    json_output = {
        'version': JSONFEED_VERSION_URL,
        'title': ' - '.join((FORUM_NAME, forum_title)),
        'home_page_url': FORUM_ENDPOINT + thread_uri
    }

    items_list = []

    for result in page_data['results']:
        post_id = result['postid']
        time_stamp = int(result['dateline'])
        item = {
            'id': post_id,
            'url': FORUM_ENDPOINT + thread_uri + '/post' + post_id,
            'title': ' - '.join((thread_title, f"Page {last_page}")),
            'content_html': bbcode.render_html(result['pagetext']),
            'date_published': datetime.datetime.utcfromtimestamp(time_stamp).isoformat('T')
        }
        items_list.append(item)

    json_output['items'] = items_list

    return json_output

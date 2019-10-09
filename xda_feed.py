import datetime
import bbcode
import requests


def get_latest_json(thread_id):
    api_endpoint = 'https://api.xda-developers.com/v3'

    forum_endpoint = 'https://forum.xda-developers.com'

    thread_data = requests.get(f"{api_endpoint}/posts?threadid={thread_id}").json()

    if thread_data.get('error') is not None:
        return {
            'error': thread_data.get('error').get('code'),
            'message': thread_data.get('error').get('message')
        }

    title_text = thread_data.get('thread').get('forumtitle')

    thread_uri = thread_data.get('thread').get('web_uri')

    last_page = thread_data.get('total_pages')

    page_data = requests.get(f"{api_endpoint}/posts?threadid={thread_id}&page={last_page}").json()

    json_output = {
        'version': 'https://jsonfeed.org/version/1',
        'title': title_text,
        'home_page_url': forum_endpoint + thread_uri
    }

    items_list = []

    for result in page_data['results']:
        post_id = result['postid']
        time_stamp = int(result['dateline'])
        item = {
            'id': post_id,
            'url': forum_endpoint + thread_uri + '/post' + post_id,
            'title': result['title'],
            'content_html': bbcode.render_html(result['pagetext']),
            'date_published': datetime.datetime.utcfromtimestamp(time_stamp).isoformat('T')
        }
        items_list.append(item)

    json_output['items'] = items_list

    return json_output

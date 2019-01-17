# coding:utf-8 
'''
created on 2019/1/16

@author:sunyihuan
'''

from utils import connect_mongodb_sheji, connect_es

es = connect_es()

from elasticsearch import helpers


def search(index_release):
    es_search_options = set_search_optional()
    es_result = get_search_result(es_search_options, index_release)
    # final_result = get_result_list(es_result)
    return es_result


def get_result_list(es_result):
    sid = es_result['_scroll_id']
    scroll_size = es_result['hits']['total']
    return sid, scroll_size


def get_search_result(es_search_options, index, scroll='5m'):
    page = es.search(
        index=index,
        scroll=scroll,
        size=10000,
        body=es_search_options,
    )
    return page


def set_search_optional():
    # 检索选项
    es_search_options = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "action_timestamp": {
                                "gt": "1541779200",  # >1541779200
                                "lt": "1544371200"  # <=1544371200
                            }
                        }
                    },
                    {
                        "term": {
                            "business_line": 'meiyezhushou'
                        }
                    }
                ],
                "should": []
            }
        },
    }
    return es_search_options


if __name__ == '__main__':
    index_release = 'user_behavior_log_prod_20180723'  # 线上index

    page = search(index_release)
    print("page........")
    print(page['hits'].keys())
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']
    print(scroll_size)


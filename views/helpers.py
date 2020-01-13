"""Helpers functions for project view."""


def data_nomralize_tonality(objs, max_val):
    """Decrease count of elements in tonality data list to max val.

    Accept django model object NewsTonal and int max_val.
    """

    data = []
    max_val_in_single = round(len(objs)/max_val)
    max_val_tonality = []
    max_val_index = []
    tmp_index = 1
    for item in objs.order_by("-news_item__date"):
        max_val_tonality.append(item.tonality)
        max_val_index.append(item.tonality_index)
        tmp_index += 1
        if tmp_index > max_val_in_single:
            data.append({
                "news_title": item.news_item.title,
                "news_date": item.news_item.date,
                "tonality": round(
                    sum(max_val_tonality)/len(max_val_tonality), 2
                ),
                "tonality_index": round(
                    sum(max_val_index)/len(max_val_index), 2
                )
            })
            max_val_tonality = []
            max_val_index = []
            tmp_index = 1
    return data

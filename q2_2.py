from typing import Dict, List, Set, Union
import pprint


def analyze_views(views: str) -> Dict[str, Union[List[str], Set[str], int, Dict[str, int], str]]:

    if not views or views.strip() == "":
        return {}
    
    normalized_views = views.lower()
    view_list = normalized_views.split()
    unique_videos = set(view_list)
    view_counts = {}
    for video in view_list:
        view_counts[video] = view_counts.get(video, 0) + 1
    total_views = len(view_list)

    most_watched = max(view_counts, key=view_counts.get)
    least_watched = min(view_counts, key=view_counts. get)
    return {
        "views": view_list,
        "unique_videos": unique_videos,
        "total_views":  total_views,
        "view_counts": view_counts,
        "most_watched": most_watched,
        "least_watched": least_watched
    }


if __name__ == "__main__":
    views = "Intro Python intro Java Python intro"
    pprint.pprint(analyze_views(views=views))
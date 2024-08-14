import praw
import datetime 
import pandas as pd
from tqdm import tqdm

def parse_author(author):
    print(author)
    if author:
        if author.comment_karma:
            author_comment_karma=author.comment_karma
        else:
            author_comment_karma = None
        if author.created_utc:
            author_created_utc=datetime.datetime.fromtimestamp(int(author.created_utc)).replace(tzinfo=datetime.timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
        else:
            author_created_utc = datetime.datetime(1970,1,1,0,0,0)
        if author.icon_img:
            author_icon_img=author.icon_img
        else:
            author_icon_img = None
        if author.id:
            author_id=author.id
        else:
            author_id = None
        if author.is_employee:
            author_is_employee=author.is_employee
        else:
            author_is_employee = None
        if author.is_mod:
            author_is_mod=author.is_mod
        else:
            author_is_mod = None

        if author.is_gold:
            author_is_gold=author.is_gold
        else:
            author_is_gold = None

        if author.link_karma:
            author_link_karma=author.link_karma
        else:
            author_link_karma = None

        if author.name:
            author_name=author.name
        else:
            author_name = None
        record = (author_id, author_name, author_link_karma, author_comment_karma, author_created_utc, author_icon_img, author_is_employee, author_is_mod, author_is_gold)
    else:
        record = (None, None, None, None, None, None, None, None, None)
    return record


def getSubmissions(reddit_client, lst_ids, subreddit_filter, subreddit_items, time_filter):
    
    all_records = []
    for url in tqdm(lst_ids, total=len(lst_ids), desc="Récupération des soumissions"):
        subreddit = reddit_client.subreddit(str(url))

        sub_record = parse_subreddit(subreddit)

        if subreddit_filter == "top":
            subreddit_selection = subreddit.top(limit=subreddit_items, time_filter= time_filter)
        elif subreddit_filter == "hot":
            subreddit_selection = subreddit.hot(limit=subreddit_items, time_filter= time_filter)
        elif subreddit_filter == "controversial":
            subreddit_selection = subreddit.controversial(limit=subreddit_items, time_filter= time_filter)
        else:
            subreddit_selection = subreddit.new(limit=subreddit_items, time_filter= time_filter)

        for submission in subreddit_selection:
            author = submission.author
            author_record  = parse_author(author)
            submission_record = parse_submission(submission)    

            record = sub_record + author_record + submission_record
            all_records.append(record)

            df = pd.DataFrame.from_records(all_records, 
                                           columns = ["subreddit_id", "subreddit_name", "subreddit_display_name", "subreddit_subscribers", "subreddit_date", "subreddit_description", "subreddit_public_description", "subreddit_over18", 
                                                      "subreddit_spoilers_enabled", "subreddit_can_assign_user_flair", "subreddit_can_assign_link_flair", "subreddit_lang", "subreddit_active_user_count",
                                                      "author_id", "author_name", "author_link_karma", "author_comment_karma", "author_created_utc", "author_icon_img", "author_is_employee", "author_is_mod", "author_is_gold",
                                                      "submission_id", "submission_title", "submission_name", "submission_created_utc", "submission_distinguished", "submission_edited", "submission_is_self", "submission_link_flair_template_id", 
                                                      "submission_link_flair_text", "submission_locked", "submission_num_comments", "submission_over_18", "submission_permalink", "submission_score", "submission_selftext", "submission_spoiler", 
                                                      "submission_stickied", "submission_url", "submission_upvote_ratio", "submission_downs", "submission_ups", "submission_num_crossposts", "submission_num_reports", "submission_score", 
                                                      "submission_total_awards_received", "submission_view_count"]
            )
            
    return df


def parse_submission(submission):
    if submission.id:
        submission_id=submission.id
    else:
        submission_id = None
    if submission.title:
        submission_title=submission.title
    else:
        submission_title = None
    if submission.name:
        submission_name=submission.name
    else:
        submission_name = None
    if submission.created_utc:
        submission_created_utc=datetime.datetime.fromtimestamp(int(submission.created_utc)).replace(tzinfo=datetime.timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
    else:
        submission_created_utc = datetime.datetime(1970,1,1,0,0,0)
    if submission.distinguished:
        submission_distinguished=submission.distinguished
    else:
        submission_distinguished = None
    if submission.edited:
        submission_edited=submission.edited
    else:
        submission_edited = None
    if submission.is_self:
        submission_is_self=submission.is_self
    else:
        submission_is_self = None
    if submission.link_flair_template_id:
        submission_link_flair_template_id=submission.link_flair_template_id
    else:
        submission_link_flair_template_id = None
    if submission.link_flair_text:
        submission_link_flair_text=submission.link_flair_text
    else:
        submission_link_flair_text = None
    if submission.locked:
        submission_locked=submission.locked
    else:
        submission_locked = None
    if submission.num_comments:
        submission_num_comments=submission.num_comments
    else:
        submission_num_comments = None
    if submission.over_18:
        submission_over_18=submission.over_18
    else:
        submission_over_18 = None
    if submission.permalink:
        submission_permalink=submission.permalink
    else:
        submission_permalink = None
    if submission.score:
        submission_score=submission.score
    else:
        submission_score = None
    if submission.selftext:
        submission_selftext=submission.selftext
    else:
        submission_selftext = None
    if submission.spoiler:
        submission_spoiler=submission.spoiler
    else:
        submission_spoiler = None
    if submission.stickied:
        submission_stickied=submission.stickied
    else:
        submission_stickied = None
    if submission.upvote_ratio:
        submission_upvote_ratio=submission.upvote_ratio
    else:
        submission_upvote_ratio = None
    if submission.url:
        submission_url=submission.url
    else:
        submission_url = None
    if submission.downs:
        submission_downs=submission.downs
    else:
        submission_downs = None
    if submission.num_crossposts:
        submission_num_crossposts=submission.num_crossposts 
    else:
        submission_num_crossposts = None
    if submission.num_reports:
        submission_num_reports=submission.num_reports 
    else:
        submission_num_reports = None

    if submission.score:
        submission_score=submission.score 
    else:
        submission_score = None

    if submission.ups:
        submission_ups=submission.ups 
    else:
        submission_ups = None

    if submission.total_awards_received:
        submission_total_awards_received=submission.total_awards_received 
    else:
        submission_total_awards_received = None

    if submission.view_count:
        submission_view_count=submission.view_count 
    else:
        submission_view_count = None


    record = (submission_id, submission_title, submission_name, submission_created_utc, submission_distinguished, submission_edited, submission_is_self, submission_link_flair_template_id, submission_link_flair_text, submission_locked, submission_num_comments, submission_over_18, submission_permalink, submission_score, submission_selftext, submission_spoiler, submission_stickied, submission_url, submission_upvote_ratio, submission_downs, submission_ups, submission_num_crossposts, submission_num_reports, submission_score, submission_total_awards_received, submission_view_count)
    return record

    

def get_subreddit_info(reddit_client : praw.Reddit, lst_ids: list) -> pd.DataFrame:
    """
    Retrieves information about subreddits based on a list of subreddit IDs.

    Args:
        lst_ids (list): A list of subreddit IDs.

    Returns:
        pd.DataFrame: A DataFrame containing the following information for each subreddit:
            - subreddit_id: The ID of the subreddit.
            - name: The name of the subreddit.
            - display_name: The display name of the subreddit.
            - subscribers: The number of subscribers to the subreddit.
            - date: The creation date of the subreddit.
            - description: The description of the subreddit.
            - public_description: The public description of the subreddit.
            - over18: Indicates if the subreddit is for users over 18 years old.
            - spoilers_enabled: Indicates if spoilers are enabled in the subreddit.
            - can_assign_user_flair: Indicates if users can assign their own flair in the subreddit.
            - can_assign_link_flair: Indicates if users can assign flair to links in the subreddit.
    """
    all_records = []
    for reddit_id in lst_ids:
        subreddit = reddit_client.subreddit(str(reddit_id))
        record = parse_subreddit(subreddit)
  
        all_records.append(record)

    df = pd.DataFrame.from_records(all_records, columns=["subreddit_id", "subreddit_name", "subreddit_display_name", "subreddit_subscribers", "subreddit_date", "subreddit_description", "subreddit_public_description", "subreddit_over18", "subreddit_spoilers_enabled", "subreddit_can_assign_user_flair", "subreddit_can_assign_link_flair", "subreddit_lang", "subreddit_active_user_count"])
    return df

def parse_subreddit(subreddit):
    if subreddit.id:
        subreddit_id = subreddit.id
    else:
        subreddit_id = None
        
    if subreddit.name:
        name = subreddit.name
    else:
        name = None

    if subreddit.display_name:
        display_name = subreddit.display_name
    else:
        display_name = None

    if subreddit.subscribers:
        subscribers = subreddit.subscribers
    else:
        subscribers = None    

    if subreddit.created_utc:
        date=datetime.datetime.fromtimestamp(int(subreddit.created_utc)).replace(tzinfo=datetime.timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
    else:
        date = datetime.datetime(1970,1,1,0,0,0)
    if subreddit.description:
        description=subreddit.description
    else:
        description=None
    if subreddit.public_description:
        public_description = subreddit.public_description
    else:
        public_description = None
    if subreddit.over18:
        over18 = subreddit.over18
    else:
        over18 = None
    if subreddit.lang:
        lang = subreddit.lang
    else:
        lang = None
    if subreddit.active_user_count:
        active_user_count = subreddit.active_user_count
    else:
        active_user_count = None

    if subreddit.spoilers_enabled:
        spoilers_enabled = subreddit.spoilers_enabled
    else:
        spoilers_enabled = None

    if subreddit.can_assign_user_flair:
        can_assign_user_flair = subreddit.can_assign_user_flair
    else:
        can_assign_user_flair = None

    if subreddit.can_assign_link_flair:
        can_assign_link_flair = subreddit.can_assign_link_flair     
    else:
        can_assign_link_flair = None

    record = (subreddit_id, name, display_name, subscribers, date, description, public_description, over18, spoilers_enabled, can_assign_user_flair, can_assign_link_flair, lang, active_user_count)
    return record


def getComments(reddit, lst_ids):
    all_records = []
    for i, submission_id in tqdm(enumerate(lst_ids), total=len(lst_ids), desc="Récupération des commentaires"):
        submission = reddit.submission(str(submission_id))
        for comment in submission.comments.list():
            record = (submission_id,) + parse_comments(comment)
            
            all_records.append(record)

    df = pd.DataFrame.from_records(all_records, columns=["submission_id", "comment_id", "comment_body", "comment_date", "comment_distinguished", "comment_edited", "comment_is_submitter", "comment_link_id", "comment_parent_id", "comment_permalink", 
                                                         "comment_controversiality", "comment_depth", "comment_downs", "comment_likes", "comment_num_reports", "comment_score", "comment_total_awards_received", "comment_ups",
                                                         "author_id", "author_name", "author_link_karma", "author_comment_karma", "author_created_utc", "author_icon_img", "author_is_employee", "author_is_mod", "author_is_gold"
                                                         ])

    return df

def parse_comments(comment):
    if comment.id:
        comment_id=comment.id
    else:
        comment_id = None
    if comment.body:
        comment_body=comment.body
    else:
        comment_body = None
    if comment.created_utc:
        comment_date=datetime.datetime.fromtimestamp(int(comment.created_utc)).replace(tzinfo=datetime.timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
    else:
        comment_date = None
    if comment.distinguished:
        comment_distinguished=comment.distinguished
    else:
        comment_distinguished = None
    if comment.edited:
        comment_edited=comment.edited
    else:
        comment_edited = None
    if comment.is_submitter:
        comment_is_submitter=comment.is_submitter
    else:
        comment_is_submitter = None

    if comment.link_id:
        comment_link_id=comment.link_id
    else:
        comment_link_id = None
    if comment.parent_id:
        comment_parent_id=comment.parent_id
    else:
        comment_parent_id = None
    if comment.permalink:
        comment_permalink=comment.permalink
    else:
        comment_permalink = None

    if comment.controversiality:
        comment_controversiality=comment.controversiality
    else:
        comment_controversiality = None
    if comment.depth:
        comment_depth=comment.depth
    else:
        comment_depth = None
    if comment.downs:
        comment_downs=comment.downs
    else:
        comment_downs = None
    if comment.likes:
        comment_likes=comment.likes
    else:
        comment_likes = None
    if comment.num_reports:
        comment_num_reports=comment.num_reports
    else:
        comment_num_reports = None
    if comment.score:
        comment_score=comment.score
    else:
        comment_score = None
    if comment.total_awards_received:
        comment_total_awards_received=comment.total_awards_received
    else:
        comment_total_awards_received = None
    if comment.ups:
        comment_ups=comment.ups
    else:
        comment_ups = None
    if comment.author:
        author_record = parse_author(comment.author)
    else:
        author_record = (None, None, None, None, None, None, None, None, None)

    record = (comment_id, comment_body, comment_date, comment_distinguished, comment_edited, comment_is_submitter, comment_link_id, comment_parent_id, comment_permalink, comment_controversiality, comment_depth, comment_downs, comment_likes, comment_num_reports, comment_score, comment_total_awards_received, comment_ups) + author_record

    return record
            
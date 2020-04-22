import aiohttp
import pylint
from apraw.models.endpoints import API_PATH
from apraw.models.listing.generator import ListingGenerator


class Subreddit:
    STR_FIELD = "display_name"
    MESSAGE_PREFIX = "#"

    @staticmethod
    def _create_or_update(
            _reddit,
            allow_images=None,
            allow_post_crossposts=None,
            allow_top=None,
            collapse_deleted_comments=None,
            comment_score_hide_mins=None,
            description=None,
            domain=None,
            exclude_banned_modqueue=None,
            header_hover_text=None,
            hide_ads=None,
            lang=None,
            key_color=None,
            link_type=None,
            name=None,
            over_18=None,
            public_description=None,
            public_traffic=None,
            show_media=None,
            show_media_preview=None,
            spam_comments=None,
            spam_links=None,
            spam_selfposts=None,
            spoilers_enabled=None,
            sr=None,
            submit_link_label=None,
            submit_text=None,
            submit_text_label=None,
            subreddit_type=None,
            suggested_comment_sort=None,
            title=None,
            wiki_edit_age=None,
            wiki_edit_karma=None,
            wikimode=None,
            **other_settings
    ):
        # pylint: disable=invalid-name,too-many-locals,too-many-arguments
        model = {
            "allow_images": allow_images,
            "allow_post_crossposts": allow_post_crossposts,
            "allow_top": allow_top,
            "collapse_deleted_comments": collapse_deleted_comments,
            "comment_score_hide_mins": comment_score_hide_mins,
            "description": description,
            "domain": domain,
            "exclude_banned_modqueue": exclude_banned_modqueue,
            "header-title": header_hover_text,  # Remap here - better name
            "hide_ads": hide_ads,
            "key_color": key_color,
            "lang": lang,
            "link_type": link_type,
            "name": name,
            "over_18": over_18,
            "public_description": public_description,
            "public_traffic": public_traffic,
            "show_media": show_media,
            "show_media_preview": show_media_preview,
            "spam_comments": spam_comments,
            "spam_links": spam_links,
            "spam_selfposts": spam_selfposts,
            "spoilers_enabled": spoilers_enabled,
            "sr": sr,
            "submit_link_label": submit_link_label,
            "submit_text": submit_text,
            "submit_text_label": submit_text_label,
            "suggested_comment_sort": suggested_comment_sort,
            "title": title,
            "type": subreddit_type,
            "wiki_edit_age": wiki_edit_age,
            "wiki_edit_karma": wiki_edit_karma,
            "wikimode": wikimode,
        }

        model.update(other_settings)

    def __init__(self, subreddit):
        self.subreddit = subreddit

    @property
    async def banned(self):
        return SubredditRelationship(self, "banned")

    @property
    def contributor(self):
        return ContributorRelationship(self, "contributor")

    @property
    async def flair(self):
        return SubredditFlair(self)

    @property
    async def mod(self):
        return SubredditModeration(self)

    @property
    async def moderator(self):
        return ModeratorRelationship(self, "moderator")


class SubredditFlair:

    async def __call__(self):
        pass

    def __init__(self, subreddit): \
            self.subreddit = subreddit


class SubredditRelationship:

    def __init__(self, subreddit, relationship):
        self.relationship = relationship
        self.subreddit = subreddit


class SubredditModeration:

    def __init__(self, subreddit):
        self.subreddit = subreddit
        self._stream = None

    async def modqueue(self, only=None, **generator_kwargs):
        self._handle_only(only, generator_kwargs)
        return ListingGenerator(
            self.subreddit._reddit,
            API_PATH["about_modqueue"].format(subreddit=self.subreddit),
            **generator_kwargs
        )


class ContributorRelationship(SubredditRelationship):

    async def leave(self):
        pass


class ModeratorRelationship(SubredditRelationship):

    async def __call__(self, redditor=None):
        params = {} if redditor is None else {"user": redditor}


class Modmail:

    async def __call__(self, id=None, mark_read=False):
        pass

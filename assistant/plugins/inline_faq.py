from pyrogram import (
    Client,
    Filters,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent
)
from .get_faqs import faq



def _search_title(query):
    q = ''.join(map(str.strip, query.query.split('!f')))
    print(tuple(faq))
    return [(title, url) for title, url in faq if q.lower() in title.lower()]


@Client.on_inline_query(Filters.create(
    lambda _, i: i.query.strip().startswith('!f')
))
def answer_inline_query(_, i: InlineQuery):
    faqs = _search_title(i)
    if not faqs:
        i.answer(
            results=[],
            switch_pm_text='❌ nothing to show! ❌',
            switch_pm_parameter='start'
        )


    else:
        i.answer(
            results=[
                InlineQueryResultArticle(
                    title=title,
                    input_message_content=InputTextMessageContent(
                        message_text=f"[{title}]({url})",
                        disable_web_page_preview=False
                    ),
                    thumb_url='https://imgur.com/BXXK3Nj.png'
                ) for title, url in faqs
            ], cache_time=1, is_personal=True
        )

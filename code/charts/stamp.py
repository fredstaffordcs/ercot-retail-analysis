"""Date stamp for the charts: 'Updated <day> <Month> <year>', centred on the footer line between the byline and the
website. The date is today's unless CHART_DATE=YYYY-MM-DD is set (to reproduce a published chart exactly)."""
import datetime
import os

MU = '#5d6b66'


def stamp_text():
    d = os.environ.get('CHART_DATE')
    d = datetime.date.fromisoformat(d) if d else datetime.date.today()
    return f'Updated {d.day} {d:%B %Y}'


def stamp(f, y=.018):
    f.text(.5, y, stamp_text(), fontsize=11, color=MU, va='center', ha='center')

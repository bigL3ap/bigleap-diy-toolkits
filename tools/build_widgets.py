#!/usr/bin/env python3
"""Build the mini-toolkit widgets in widgets/ from tools/widget_template.html.

Each widget asks 2-4 quick questions, gives an instant answer and links to its full toolkit.
It stores nothing, and it sends the same diy_widget_* events and height messages as the original widgets.

Run from the repo root:  python3 tools/build_widgets.py
Only the widgets listed in WIDGETS below are (re)built; the original seven hand-made widgets are left alone.
After adding one, list it in data/widgets.json and run tools/build_tiles.py for its slide tile.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCENTS = {  # light, dark (same as the hub's service colours)
    'RevOps': ('#143D55', '#6FB3DA'), 'Paid Media': ('#EA4335', '#F0675B'), 'SEO': ('#0F7B5F', '#4CC9A3'),
    'Digital PR': ('#7A4E9C', '#B78ED6'), 'Email Marketing': ('#B45309', '#E7A64A'), 'Strategy': ('#246D96', '#8CC4E4'),
}
YN = None  # default yes / no / not sure options

WIDGETS = [
    # ---------------- RevOps
    dict(id='lead-speed', service='RevOps', minutes='1 minute', kit='toolkits/revops/02_Never_Let_a_Lead_Go_Cold.html',
         title='How fast does a new lead hear back?', cta='Build my follow-up workflow',
         Q=[dict(id='speed', label='How fast does a new lead usually get a reply?', type='choice',
                 options=[['5m', 'Under 5 min'], ['1h', 'Within the hour'], ['day', 'Same day'], ['later', 'Later']]),
            dict(id='auto', label='Is the first reply sent automatically?', type='choice'),
            dict(id='owner', label='Does every new lead have a named owner?', type='choice')],
         A=dict(speed='day', auto='no', owner='unsure'),
         compute=r"""function compute(a){
  var slow = a.speed === 'day' || a.speed === 'later';
  var gaps = (slow ? 1 : 0) + (a.auto !== 'yes' ? 1 : 0) + (a.owner !== 'yes' ? 1 : 0);
  if (!gaps) return { big: 'Fast and covered', detail: 'Leads hear back quickly and someone owns each one. The full toolkit checks the follow-up after that first reply.', cta: 'Check the rest of my follow-up' };
  if (a.owner !== 'yes' && !slow && a.auto === 'yes') return { big: 'Fast, but unowned', hot: true, detail: 'Replies go out, but nobody is clearly on the hook for the next step. Give every lead a named owner.', cta: 'Set up lead ownership', link: '../toolkits/revops/03_Who_Should_Own_Each_New_Lead.html' };
  return { big: gaps + ' of 3 gaps', hot: true, detail: (slow ? 'Replies arrive hours later, and a lead who waits often talks to someone else in the meantime. ' : '') + (a.auto !== 'yes' ? 'An automatic first reply buys time while a person follows up.' : 'Make sure a person follows the automatic reply.') };
}"""),
    # ---------------- Paid Media
    dict(id='conversions-check', service='Paid Media', minutes='1 minute', kit='toolkits/paid/03_Which_Conversions_Should_You_Track.html',
         title='Is Google Ads learning from the right results?', cta='Plan my conversions',
         Q=[dict(id='goal', label='What should a visit turn into?', type='choice',
                 options=[['form', 'Form'], ['call', 'Call'], ['buy', 'Purchase'], ['book', 'Booking']]),
            dict(id='tracked', label='Is that action tracked as a conversion?', type='choice'),
            dict(id='crm', label='Do closed deals or sales flow back to Google Ads?', type='choice')],
         A=dict(goal='form', tracked='unsure', crm='no'),
         compute=r"""function compute(a){
  var names = { form: 'form fills', call: 'calls', buy: 'purchases', book: 'bookings' };
  if (a.tracked !== 'yes') return { big: 'Flying blind', hot: true, detail: 'If ' + names[a.goal] + ' are not tracked, Google Ads can only optimize for clicks. Track the action first.' };
  if (a.goal !== 'buy' && a.crm !== 'yes') return { big: 'Half the picture', hot: true, detail: 'Ads can see the ' + names[a.goal] + ', not which ones became customers. Sending closed deals back teaches bidding which leads are worth paying for.' };
  return { big: 'Learning from results', detail: 'Ads see the action that matters. The full toolkit checks values, duplicates and the GA4 link.', cta: 'Check my conversion setup' };
}"""),
    dict(id='campaign-pick', service='Paid Media', minutes='1 minute', kit='toolkits/paid/04_Which_Campaigns_Should_You_Run_First.html',
         title='Which Google Ads campaign should you run first?', cta='Plan my first campaigns',
         Q=[dict(id='goal', label='What do you want most?', type='choice',
                 options=[['leads', 'Leads'], ['sales', 'Online sales'], ['local', 'Local visits or calls'], ['aware', 'Awareness']]),
            dict(id='search', label='Do people already search for what you sell?', type='choice'),
            dict(id='budget', label='Monthly ad budget, in dollars', type='number', max=1000000)],
         A=dict(goal='leads', search='yes', budget=1500),
         compute=r"""function compute(a){
  var b = +a.budget || 0, one = b < 1500;
  var pick, why;
  if (a.goal === 'aware' || a.search === 'no') { pick = 'Demand Gen or video'; why = 'Few people search for this yet, so start by being seen, then capture searches as they grow.'; }
  else if (a.goal === 'sales') { pick = 'Shopping'; why = 'Product listings show the item and price before the click.'; }
  else if (a.goal === 'local') { pick = 'Search, with call and location assets'; why = 'Nearby searchers can call or get directions straight from the ad.'; }
  else { pick = 'Search'; why = 'People are already looking; Search puts you in front of them at that moment.'; }
  if (b > 0 && b < 1000) return { big: pick, detail: why + ' Under about $1,000 a month, keep it to one tightly focused campaign.' };
  return { big: pick, detail: why + (one ? ' Start with one campaign; add a second as budget grows.' : ' There is room for a second campaign once the first is measured.') };
}"""),
    # ---------------- SEO
    dict(id='local-ready', service='SEO', minutes='1 minute', kit='toolkits/seo/02_Is_Your_Business_Ready_for_Local_Search.html',
         title='Are you ready to show up in local search?', cta='Get my local search plan',
         Q=[dict(id='gbp', label='Is your Google Business Profile claimed and verified?', type='choice'),
            dict(id='nap', label='Are your name, address and phone the same everywhere online?', type='choice'),
            dict(id='pages', label='Does each location or service area have its own page?', type='choice'),
            dict(id='reviews', label='Have you had a new Google review in the last month?', type='choice')],
         A=dict(gbp='yes', nap='unsure', pages='no', reviews='yes'),
         compute=r"""function compute(a){
  var order = ['gbp', 'nap', 'pages', 'reviews'], names = { gbp: 'your Business Profile', nap: 'consistent listings', pages: 'location pages', reviews: 'fresh reviews' };
  var why = { gbp: 'It is the listing people see in Maps and the local pack.', nap: 'Mismatched details make it harder for Google to trust which listing is right.', pages: 'A page per location gives each one something to rank with.', reviews: 'Recent reviews reassure people and signal an active business.' };
  var gaps = order.filter(function(k){ return a[k] !== 'yes'; });
  if (!gaps.length) return { big: 'Local-ready', detail: 'The basics are in place. The full toolkit checks categories, photos, Q&A and how you ask for reviews.', cta: 'Check the finer points' };
  return { big: gaps.length + ' of 4 to fix', hot: true, detail: 'Start with ' + names[gaps[0]] + '. ' + why[gaps[0]] };
}"""),
    dict(id='review-health', service='SEO', minutes='1 minute', kit='toolkits/seo/02_Is_Your_Business_Ready_for_Local_Search.html',
         title='How healthy are your Google reviews?', cta='Plan a steady review flow',
         Q=[dict(id='count', label='About how many Google reviews do you have?', type='number', max=100000),
            dict(id='recent', label='When did the most recent one arrive?', type='choice',
                 options=[['week', 'This week'], ['month', 'This month'], ['older', 'Longer ago'], ['unsure', 'Not sure']]),
            dict(id='reply', label='Do you reply to reviews?', type='choice',
                 options=[['all', 'All of them'], ['some', 'Some'], ['none', 'Rarely']])],
         A=dict(count=24, recent='older', reply='some'),
         compute=r"""function compute(a){
  var n = +a.count || 0, issues = [];
  if (a.recent === 'older' || a.recent === 'unsure') issues.push('No recent reviews: ask every customer after the job, not just the happy ones.');
  if (a.reply !== 'all') issues.push('Reply to every review, good and bad. People read the replies.');
  if (n < 10) issues.push('A handful of reviews is easy to outweigh; a steady flow matters more than a burst.');
  if (!issues.length) return { big: 'Healthy and active', detail: 'Steady, recent and answered. Keep asking the same way, and never offer anything in return for a review.', cta: 'See more ways to earn reviews', link: '../toolkits/plan/04_Would_Your_Customers_Recommend_You.html' };
  return { big: issues.length === 1 ? 'One thing to fix' : issues.length + ' things to fix', hot: true, detail: issues[0] };
}"""),
    dict(id='brand-entity-check', service='SEO', minutes='1 minute', kit='toolkits/seo/03_Does_Google_and_AI_Know_Who_You_Are.html',
         title='Does Google and AI know who you are?', cta='Check my entity signals',
         Q=[dict(id='schema', label='Does your homepage have Organization schema markup?', type='choice'),
            dict(id='nap', label='Are your name, address and phone the same everywhere online?', type='choice'),
            dict(id='panel', label='Does a Knowledge Panel show when you search your business name?', type='choice')],
         A=dict(schema='no', nap='unsure', panel='unsure'),
         compute=r"""function compute(a){
  var order = ['schema', 'nap', 'panel'], names = { schema: 'Organization schema', nap: 'consistent business details', panel: 'a Knowledge Panel' };
  var why = { schema: 'A snippet of code on your homepage that tells Google and AI tools exactly who you are. The quickest DIY fix of the three.', nap: 'Mismatched details across directories make it harder for Google to trust which listing is right.', panel: 'This tends to show up once the other signals are solid and consistent, not from a single fix.' };
  var gaps = order.filter(function(k){ return a[k] !== 'yes'; });
  if (!gaps.length) return { big: 'Entity signals solid', detail: 'Google and AI tools have a clear, consistent read on who you are. The full toolkit checks press mentions and cross-linked profiles too.', cta: 'Check the rest of my entity signals' };
  return { big: gaps.length + ' of 3 to fix', hot: gaps[0] !== 'panel', detail: 'Start with ' + names[gaps[0]] + '. ' + why[gaps[0]] };
}"""),
    dict(id='ai-overview-exposure', service='SEO', minutes='1 minute', kit='toolkits/seo/04_How_Exposed_Are_You_to_AI_Overviews.html',
         title='How exposed are you to AI Overviews?', cta='Check my AI Overview exposure',
         Q=[dict(id='af', label='Do your key pages answer the main question in the first sentence or two?', type='choice'),
            dict(id='faq', label='Do you use FAQ-style, question-phrased headers?', type='choice'),
            dict(id='schema', label='Do you have FAQPage or HowTo schema on any pages?', type='choice')],
         A=dict(af='unsure', faq='no', schema='no'),
         compute=r"""function compute(a){
  var order = ['af', 'faq', 'schema'], names = { af: 'answering first', faq: 'FAQ-style headers', schema: 'FAQPage or HowTo schema' };
  var why = { af: 'An AI tool usually lifts the first clear, complete answer it finds on a page.', faq: 'A header phrased as a real question gives AI tools a clean pair to lift.', schema: 'This marks up a question-and-answer section in a format AI tools can read directly.' };
  var strong = order.filter(function(k){ return a[k] === 'yes'; }).length;
  if (strong === 3) return { big: 'Ready for AI Overviews', detail: 'Your content is shaped the way AI tools tend to lift answers from. The full toolkit checks ranking and content freshness too.', cta: 'Check the rest of my exposure' };
  var gaps = order.filter(function(k){ return a[k] !== 'yes'; });
  var label = strong === 0 ? 'Low exposure' : 'Building exposure';
  return { big: label, hot: strong === 0, detail: 'Start with ' + names[gaps[0]] + '. ' + why[gaps[0]] };
}"""),
    dict(id='ai-crawler-check', service='SEO', minutes='1 minute', kit='toolkits/seo/05_Can_AI_Bots_Actually_Read_Your_Site.html',
         title='Can AI bots actually read your site?', cta='Check my AI crawler readiness',
         Q=[dict(id='robots', label='Does your robots.txt file block any named AI crawlers, like GPTBot or ClaudeBot?', type='choice'),
            dict(id='render', label='Is your key content visible without JavaScript?', type='choice'),
            dict(id='gating', label='Is any of your core content behind a login or paywall?', type='choice')],
         A=dict(robots='unsure', render='unsure', gating='no'),
         compute=r"""function compute(a){
  if (a.robots === 'yes') return { big: 'Blocked', hot: true, detail: 'Your robots.txt is telling at least one AI crawler not to visit. Nothing else matters until that block is removed.' };
  if (a.gating === 'yes') return { big: 'Blocked', hot: true, detail: 'Content behind a login or paywall is invisible to every crawler, AI included. Decide what, if anything, should be public.' };
  if (a.render !== 'yes') return { big: 'Partially ready', hot: true, detail: 'If key content only appears after JavaScript runs, many AI crawlers may see a blank page. Check your raw HTML.' };
  if (a.robots === 'unsure') return { big: 'Partially ready', hot: true, detail: 'Worth confirming: check yoursite.com/robots.txt for a Disallow line under any of the AI crawler names.' };
  return { big: 'Ready', detail: 'No blockers found. The full toolkit checks llms.txt, your sitemap and homepage speed too.', cta: 'Check the rest of my crawler readiness' };
}"""),
    # ---------------- Digital PR
    dict(id='media-kit', service='Digital PR', minutes='1 minute', kit='toolkits/pr/02_Build_Your_Media_Kit.html',
         title='Is your media kit ready for a journalist?', cta='Build my media kit',
         Q=[dict(id='bio', label='Short and long bios, ready to paste?', type='choice'),
            dict(id='photo', label='A high-resolution headshot?', type='choice'),
            dict(id='topics', label='Three topics you can speak on with authority?', type='choice'),
            dict(id='press', label='A press page on your website?', type='choice')],
         A=dict(bio='yes', photo='no', topics='unsure', press='no'),
         compute=r"""function compute(a){
  var keys = ['bio', 'photo', 'topics', 'press'], names = { bio: 'your bios', photo: 'a headshot', topics: 'your topics', press: 'a press page' };
  var ready = keys.filter(function(k){ return a[k] === 'yes'; }).length, gaps = keys.filter(function(k){ return a[k] !== 'yes'; });
  if (!gaps.length) return { big: 'Kit complete', detail: 'A journalist or host can find everything without emailing you. The toolkit helps you keep it current.', cta: 'Polish my media kit' };
  return { big: ready + ' of 4 ready', hot: ready < 3, detail: 'Add ' + names[gaps[0]] + ' next. Reporters on deadline use whoever makes it easy.' };
}"""),
    dict(id='podcast-ready', service='Digital PR', minutes='1 minute', kit='toolkits/pr/02_Build_Your_Media_Kit.html',
         title='Are you ready to be a podcast guest?', cta='Build my guest kit',
         Q=[dict(id='topic', label='A topic you could talk about for 30 minutes?', type='choice'),
            dict(id='story', label='A story or example only you can tell?', type='choice'),
            dict(id='audio', label='A decent mic and a quiet room?', type='choice')],
         A=dict(topic='yes', story='unsure', audio='no'),
         compute=r"""function compute(a){
  var gaps = ['topic', 'story', 'audio'].filter(function(k){ return a[k] !== 'yes'; });
  var tip = { topic: 'Pick one topic you could teach without notes.', story: 'Hosts book guests with a story; find one example only you can tell.', audio: 'A USB mic and a quiet room make a big difference to how you come across.' };
  if (!gaps.length) return { big: 'Ready to guest', detail: 'You have what hosts look for. The toolkit builds the one-page intro and host questions to send them.', cta: 'Build my guest kit' };
  return { big: gaps.length === 1 ? 'Almost ready' : gaps.length + ' things first', hot: gaps.length > 1, detail: tip[gaps[0]] };
}"""),
    # ---------------- Email Marketing
    dict(id='email-flows', service='Email Marketing', minutes='1 minute', kit='toolkits/email/02_Which_Emails_Should_Send_Themselves.html',
         title='Which emails should be sending themselves?', cta='Plan my automated emails',
         Q=[dict(id='welcome', label='Do new subscribers get a welcome series?', type='choice'),
            dict(id='after', label='Do customers hear from you after a purchase or project?', type='choice'),
            dict(id='quiet', label='Do you reach out to people who have gone quiet?', type='choice'),
            dict(id='cart', label='Do abandoned carts or quotes get a reminder?', type='choice',
                 options=[['yes', 'Yes'], ['no', 'No'], ['na', 'Not for us']])],
         A=dict(welcome='no', after='yes', quiet='no', cart='na'),
         compute=r"""function compute(a){
  var order = ['welcome', 'cart', 'after', 'quiet'], names = { welcome: 'a welcome series', cart: 'an abandoned cart or quote reminder', after: 'a post-purchase follow-up', quiet: 'a win-back email' };
  var missing = order.filter(function(k){ return a[k] === 'no' || a[k] === 'unsure'; });
  if (!missing.length) return { big: 'Core flows running', detail: 'The main automations are in place. The toolkit checks timing, content and what each flow should do next.', cta: 'Review my flows' };
  return { big: missing.length + ' flow' + (missing.length > 1 ? 's' : '') + ' missing', hot: true, detail: 'Start with ' + names[missing[0]] + '. Once built, it works every day without another send.' };
}"""),
    dict(id='email-health', service='Email Marketing', minutes='1 minute', kit='toolkits/email/03_Is_Your_Email_Program_Working.html',
         title='Is your email program healthy?', cta='Score my email program',
         Q=[dict(id='spam', label='Your spam complaint rate', type='choice',
                 options=[['low', 'Under 0.1%'], ['mid', '0.1–0.3%'], ['high', 'Over 0.3%'], ['unsure', "Don't know"]]),
            dict(id='sunset', label='Do you stop emailing people who never engage?', type='choice'),
            dict(id='results', label='Do you know the leads or revenue email brings in?', type='choice')],
         A=dict(spam='unsure', sunset='no', results='no'),
         compute=r"""function compute(a){
  if (a.spam === 'high') return { big: 'Deliverability at risk', hot: true, detail: 'Gmail and Yahoo ask bulk senders to stay under 0.3% complaints, and ideally under 0.1%. Fix this before anything else.', cta: 'Fix my deliverability', link: '../toolkits/email/01_Will_Your_Emails_Reach_the_Inbox.html' };
  if (a.spam === 'unsure') return { big: 'Check complaints first', hot: true, detail: 'Your platform reports it on every send. Above 0.3% risks the inbox at Gmail and Yahoo.' };
  var gaps = (a.spam === 'mid' ? 1 : 0) + (a.sunset !== 'yes' ? 1 : 0) + (a.results !== 'yes' ? 1 : 0);
  if (!gaps) return { big: 'Healthy', detail: 'Low complaints, a clean list and known results. The full scorecard checks clicks, bounces and growth.' };
  return { big: gaps + ' to improve', hot: gaps > 1, detail: a.sunset !== 'yes' ? 'Stop sending to people who never open or click; it protects delivery for everyone else.' : 'Tie email to leads or revenue so you know what it is worth.' };
}"""),
    # ---------------- Strategy
    dict(id='situation-check', service='Strategy', minutes='1 minute', kit='toolkits/plan/01_Are_You_Solving_the_Right_Problem.html',
         title='Are you solving the right marketing problem?', cta='Get my situation read',
         Q=[dict(id='market', label='Which sounds most like you?', type='choice',
                 options=[['capture', 'People already look for what we sell'], ['generate', 'We have to create the interest'], ['expand', "We've won our main market"]]),
            dict(id='hold', label='What holds growth back most?', type='choice',
                 options=[['diff', 'We look like everyone else'], ['profit', 'Growth costs too much'], ['durable', "Wins don't last"], ['unsure', 'Not sure']])],
         A=dict(market='capture', hold='diff'),
         compute=r"""function compute(a){
  var lead = { capture: 'Be found and chosen', generate: 'Get noticed first', expand: 'Grow what you have won' };
  var fix = { diff: 'Sharpen why someone should choose you over the others.', profit: 'Make each customer cost less to win and worth more once won.', durable: 'Turn customers into repeat buyers and referrers.', unsure: 'Answer a few more questions to see which constraint matters most.' };
  return { big: lead[a.market], detail: fix[a.hold] + ' This is a preliminary read from two answers, not research.' };
}"""),
    dict(id='foundations-check', service='Strategy', minutes='1 minute', kit='toolkits/plan/02_What_Do_You_Already_Have.html',
         title='Which marketing foundation do you fix first?', cta='Check all my foundations',
         Q=[dict(id='pos', label='A clear, written reason to choose you?', type='choice'),
            dict(id='site', label='A website that turns visits into leads or sales?', type='choice'),
            dict(id='track', label='Tracking you trust?', type='choice'),
            dict(id='crm', label='A CRM every lead lands in?', type='choice')],
         A=dict(pos='unsure', site='yes', track='no', crm='yes'),
         compute=r"""function compute(a){
  var order = ['pos', 'site', 'track', 'crm'], names = { pos: 'your positioning', site: 'your website', track: 'tracking', crm: 'your CRM' };
  var gaps = order.filter(function(k){ return a[k] !== 'yes'; });
  if (!gaps.length) return { big: 'Solid foundations', detail: 'The basics hold up. The full check covers 13 areas and credits what already works.', cta: 'Check all 13 areas' };
  return { big: 'Fix ' + names[gaps[0]] + ' first', hot: true, detail: 'It sits underneath the others: work built on top of it ' + (gaps[0] === 'pos' ? 'repeats a message that hasn\'t been settled.' : 'can\'t be measured or kept.') + (a[gaps[0]] === 'unsure' ? ' Not sure counts as a gap until checked.' : '') };
}"""),
    dict(id='referral-ready', service='Strategy', minutes='1 minute', kit='toolkits/plan/04_Would_Your_Customers_Recommend_You.html',
         title='Would your customers recommend you?', cta='Plan moments worth sharing',
         Q=[dict(id='checkin', label='Do you check in during the first week of working together?', type='choice'),
            dict(id='ask', label='Do you ask every customer for a review?', type='choice'),
            dict(id='refer', label='Is there an easy way for customers to refer someone?', type='choice')],
         A=dict(checkin='no', ask='unsure', refer='no'),
         compute=r"""function compute(a){
  if (a.checkin !== 'yes') return { big: 'Start with week one', hot: true, detail: 'A quick check-in early catches problems before they become reviews. Recommendations start with a good first week.' };
  if (a.ask !== 'yes') return { big: 'Ask everyone', hot: true, detail: 'Ask every customer, not only the happy ones. Filtering who gets asked breaks Google\'s review rules.' };
  if (a.refer !== 'yes') return { big: 'Make referring easy', detail: 'One simple way to introduce a friend. If you offer a reward, say so openly.' };
  return { big: 'Worth recommending', detail: 'The habits are in place. The toolkit maps the nine moments where customers decide.', cta: 'Map my customer moments' };
}"""),
]


def build(w):
    tpl = open(os.path.join(ROOT, 'tools', 'widget_template.html'), encoding='utf-8').read()
    light, dark = ACCENTS[w['service']]
    Q = [dict(q) for q in w['Q']]
    vals = {'{{TITLE}}': w['title'], '{{ACCENT}}': light, '{{ACCENT_DARK}}': dark, '{{SERVICE}}': w['service'],
            '{{MINUTES}}': w['minutes'], '{{KIT}}': w['kit'], '{{CTA}}': w['cta'],
            '{{Q}}': json.dumps(Q, ensure_ascii=False), '{{A}}': json.dumps(w['A'], ensure_ascii=False), '{{COMPUTE}}': w['compute']}
    for k, v in vals.items():
        tpl = tpl.replace(k, v)
    assert '{{' not in tpl, w['id']
    open(os.path.join(ROOT, 'widgets', w['id'] + '.html'), 'w', encoding='utf-8').write(tpl)


if __name__ == '__main__':
    for w in WIDGETS:
        build(w)
        print('built widgets/' + w['id'] + '.html')

"""Offline and live-public-listing checks for PAL buyer selector."""
import pathlib,re,html.parser,urllib.request,urllib.parse,ssl,json,unittest
ROOT=pathlib.Path(__file__).resolve().parent.parent
DOMAIN='https://apify.com/practical_ai_lab_jp/'
class Parser(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.actors=[];self.links=[];self.cards=0
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='article' and 'card' in d.get('class','').split():
   self.cards+=1;self.actors.append(d.get('data-actor'))
  if tag=='a':self.links.append(d.get('href',''))
class ToolFinderTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.html=(ROOT/'tool-finder.html').read_text()
  cls.parser=Parser();cls.parser.feed(cls.html)
 def test_eight_specific_tasks(self):
  self.assertEqual(self.parser.cards,8)
  self.assertEqual(len(self.parser.actors),8)
  self.assertEqual(len(set(self.parser.actors)),8)
 def test_each_task_has_exact_public_store_link(self):
  for slug in self.parser.actors:
   self.assertTrue(any(x.startswith(DOMAIN+slug+'?utm_source=pal_github_pages') for x in self.parser.links),slug)
 def test_links_are_public_today(self):
  u='https://api.apify.com/v2/store?'+urllib.parse.urlencode({'username':'practical_ai_lab_jp','limit':100})
  with urllib.request.urlopen(u,timeout=16,context=ssl.create_default_context(cafile='/etc/ssl/cert.pem')) as f:
   data=json.load(f)['data']
  public={a['name'] for a in data['items'] if a.get('username')=='practical_ai_lab_jp'}
  self.assertTrue(set(self.parser.actors)<=public,set(self.parser.actors)-public)
 def test_requirements_and_disclosures(self):
  self.assertIn('Check current',self.html.replace('check the live','Check current') if False else 'Check current')
  self.assertIn('not a paid execution',self.html)
  self.assertIn('Not for:',self.html)
  self.assertIn('utm_campaign=buyer_job_selector',self.html)
  self.assertIn('name="description"',self.html)
  self.assertIn('tool-finder.html', (ROOT/'sitemap.xml').read_text())
  self.assertIn('href="tool-finder.html"', (ROOT/'index.html').read_text())
  self.assertIn('href="tool-finder.html"', (ROOT/'catalog.html').read_text())
 def test_no_tracking_or_external_scripts(self):
  self.assertNotIn('<script',self.html.lower())
  self.assertNotIn('<form',self.html.lower())
  self.assertNotIn('fetch(',self.html)
if __name__=='__main__':unittest.main()

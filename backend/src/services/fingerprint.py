import hashlib,json
from src.constants.vocabulary import WHITELIST
def fingerprint(corpus,documents,config):
 payload={'corpus':{k:corpus[k] for k in ('id','name','filename','description')},'documents':sorted([{'id':d['id'],'reference':d['reference'],'title':d['title'],'tokens_text':d['tokens_text']} for d in documents],key=lambda x:x['reference']),'config':config,'whitelist':list(WHITELIST),'algorithm':'whitespace-tfidf-nmf-reference-hungarian-v1'}
 return hashlib.sha256(json.dumps(payload,sort_keys=True,allow_nan=False,separators=(',',':')).encode()).hexdigest()

from collections import Counter
import numpy as np
from src.constants.vocabulary import WHITELIST

def build_tfidf(documents,min_df):
 if not documents or not isinstance(min_df,int) or min_df<1:raise ValueError('语料为空或min_df不合法')
 allowed=set(WHITELIST);tokens=[[w for w in d['tokens_text'].split() if w in allowed] for d in documents]
 df=Counter(w for doc in tokens for w in set(doc));vocabulary=sorted(w for w,n in df.items() if n>=min_df)
 if not vocabulary:raise ValueError('白名单与min_df后词汇为空')
 n=len(documents);idf=np.asarray([np.log((1+n)/(1+df[w]))+1 for w in vocabulary]);lookup={w:i for i,w in enumerate(vocabulary)};X=np.zeros((n,len(vocabulary)))
 for i,doc in enumerate(tokens):
  for w,count in Counter(doc).items():
   if w in lookup:X[i,lookup[w]]=count*idf[lookup[w]]
  norm=np.linalg.norm(X[i])
  if norm:X[i]/=norm
 kept=np.flatnonzero(np.linalg.norm(X,axis=1)>0);excluded=[{'id':d['id'],'reference':d['reference'],'reason':'白名单后空词' if not tokens[i] else 'min_df后空词'} for i,d in enumerate(documents) if i not in set(kept)]
 return {'X':X[kept],'kept_indices':kept,'excluded':excluded,'vocabulary':vocabulary,'idf':idf.tolist(),'document_frequency':[df[w] for w in vocabulary],'idf_n_documents':n,'parameters':{'tokenizer':'str.split whitespace only; exact whitelist match','tf':'raw count','idf':'ln((1+n_documents)/(1+document_frequency))+1','norm':'L2 per document','min_df':min_df,'whitelist':list(WHITELIST),'empty_documents':'excluded from NMF; still counted in IDF n_documents'}}

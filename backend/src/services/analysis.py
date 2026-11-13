import numpy as np
from .tfidf import build_tfidf
from .factorization import fit_matrix
from .alignment import align_topics
from .fingerprint import fingerprint

def analyze(corpus,documents,config):
 documents=sorted(documents,key=lambda d:d['reference'])
 if len({d['reference'] for d in documents})!=len(documents):raise ValueError('文档reference重复')
 if not isinstance(config['repeats'],int) or not 5<=config['repeats']<=10:raise ValueError('初始化重复数必须5..10')
 if not isinstance(config['seed'],int) or not 0<=config['seed']<=1000000000:raise ValueError('seed范围不合法')
 data=build_tfidf(documents,config['min_df']);X=data['X'];k=config['k'];fits=[]
 for index in range(config['repeats']):
  seed=config['seed']+index
  fit=fit_matrix(X,k,seed,config['max_iter'],config['tolerance']);fits.append(fit)
 reference=fits[0]['H'];replicates=[]
 for index,fit in enumerate(fits):
  match=align_topics(reference,fit['H']);permutation=match['permutation'];replicates.append({'index':index,'seed':config['seed']+index,'iterations':fit['iterations'],'reconstruction_error':fit['reconstruction_error'],'relative_error':fit['relative_error'],'W':fit['W'].tolist(),'H':fit['H'].tolist(),'aligned_W':fit['W'][:,permutation].tolist(),'aligned_H':fit['H'][permutation].tolist(),'alignment':match})
 stability=np.asarray([r['alignment']['similarities'] for r in replicates[1:]])
 profiles=[]
 for topic in range(k):
  weights=reference[topic];order=np.argsort(-weights,kind='stable');profiles.append({'topic_index':topic,'label':f'待命名主题{topic+1:02d}','weights':[{'term':data['vocabulary'][int(i)],'weight':float(weights[i])} for i in order],'mean_similarity':float(stability[:,topic].mean()),'similarities':stability[:,topic].tolist()})
 kept=[documents[int(i)] for i in data['kept_indices']];baseW=fits[0]['W'];scores=[]
 for i,doc in enumerate(kept):
  activation=baseW[i];total=float(activation.sum());scores.append({'id':doc['id'],'reference':doc['reference'],'title':doc['title'],'activation':activation.tolist(),'relative_activation':(activation/total).tolist() if total>1e-14 else None})
 return {'fingerprint':fingerprint(corpus,documents,config),'k':k,'repeats':config['repeats'],'reference_repeat':0,'reference_seed':config['seed'],'vocabulary':data['vocabulary'],'idf':data['idf'],'document_frequency':data['document_frequency'],'tfidf_parameters':data['parameters'],'idf_n_documents':data['idf_n_documents'],'effective_documents':len(kept),'kept_document_ids':[d['id'] for d in kept],'excluded_documents':data['excluded'],'profiles':profiles,'replicates':replicates,'document_topics':scores,'mean_alignment_similarity':float(stability.mean()),'baseline_relative_error':fits[0]['relative_error'],'interpretation':'K is preselected, not optimized by decreasing reconstruction error. Relative activations are not posterior probabilities. Stability measures seed sensitivity, not semantic truth; editorial names are human input. All repeats refit independently with random init.'}

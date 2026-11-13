import warnings
import numpy as np
from sklearn.decomposition import NMF
from sklearn.exceptions import ConvergenceWarning
from .alignment import normalize_factors

def fit_matrix(X,k,seed,max_iter,tolerance):
 X=np.asarray(X,dtype=float)
 if X.ndim!=2 or min(X.shape)<2 or not np.isfinite(X).all() or (X<0).any() or not X.any():raise ValueError('NMF矩阵必须有限非负且非空')
 if not isinstance(k,int) or not 2<=k<=6 or k>min(X.shape) or np.linalg.matrix_rank(X,tol=1e-10)<k:raise ValueError('K超出文档/词汇/数值秩；常量或低秩语料不可估计此K')
 if not isinstance(max_iter,int) or max_iter<1 or not np.isfinite(tolerance) or tolerance<=0:raise ValueError('迭代参数不合法')
 model=NMF(n_components=k,init='random',solver='cd',beta_loss='frobenius',random_state=seed,max_iter=max_iter,tol=tolerance,alpha_W=0.,alpha_H=0.,l1_ratio=0.,shuffle=False)
 with warnings.catch_warnings(record=True) as seen:
  warnings.simplefilter('always',ConvergenceWarning);W=model.fit_transform(X)
 if any(issubclass(w.category,ConvergenceWarning) for w in seen):raise ValueError(f'未收敛：seed={seed} max_iter={max_iter}；增加上限后重新运行')
 Wn,Hn=normalize_factors(W,model.components_);error=float(np.linalg.norm(X-Wn@Hn))
 return {'W':Wn,'H':Hn,'iterations':int(model.n_iter_),'reconstruction_error':error,'relative_error':error/float(np.linalg.norm(X))}

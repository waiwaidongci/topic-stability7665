import numpy as np
from scipy.optimize import linear_sum_assignment

def normalize_factors(W,H):
 W=np.asarray(W,dtype=float);H=np.asarray(H,dtype=float)
 if W.ndim!=2 or H.ndim!=2 or W.shape[1]!=H.shape[0] or not np.isfinite(W).all() or not np.isfinite(H).all() or (W<0).any() or (H<0).any():raise ValueError('W/H须有限非负且维度匹配')
 scales=H.sum(axis=1)
 if (scales<=1e-14).any():raise ValueError('出现空主题分量，不能归一或声称稳定')
 return W*scales,H/scales[:,None]
def align_topics(reference,candidate):
 A=np.asarray(reference,dtype=float);B=np.asarray(candidate,dtype=float)
 if A.ndim!=2 or A.shape!=B.shape or not len(A) or not np.isfinite(A).all() or not np.isfinite(B).all() or (A<0).any() or (B<0).any():raise ValueError('待对齐主题形状不一致或非法')
 an=np.linalg.norm(A,axis=1);bn=np.linalg.norm(B,axis=1)
 if (an<=1e-14).any() or (bn<=1e-14).any():raise ValueError('空主题不可对齐')
 cosine=np.clip((A/an[:,None])@(B/bn[:,None]).T,0,1);row,col=linear_sum_assignment(-cosine);permutation=np.empty(len(A),dtype=int);permutation[row]=col
 return {'permutation':permutation.tolist(),'similarities':cosine[np.arange(len(A)),permutation].tolist(),'cosine_matrix':cosine.tolist()}

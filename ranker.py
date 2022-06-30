import math
import sys
import time
import metapy
import pytoml
import numpy as np
from scipy.stats import ttest_rel as tt 
import random
from scipy.stats import wilcoxon
from matplotlib import pyplot as plt

def load_ranker(cfg_file,mu):
    """
    Use this function to return the Ranker object to evaluate, 
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    
    # return metapy.index.JelinekMercer(0.5) 
    return metapy.index.DirichletPrior(mu) 

def score2(ranker,index,query,top_k,alpha):
    print("Scoring")
    # print("start")
    results = ranker.score(index, query, 1000)
    # print(results[:20])
    for res in results[:20]:
        doc_name = index.metadata(res[0]).get('doc_name')
        # print(doc_name,res[1])

    new_results = []
    new_scores = []
    updated_results = {}
    alpha = alpha #all, 2500, 0.13, 0.666
    for res in results:
        doc_name = index.metadata(res[0]).get('doc_name')
        # print(doc_name)
        # print(float(index.metadata(res[0]).get('prior')))
        updated_results[doc_name] = (1-alpha)*res[1]+alpha*float(index.metadata(res[0]).get('prior') )
        new_scores.append(updated_results[doc_name])

    # print (sorted(updated_results.items(),key=lambda k:k[1],reverse=True)[:])

    new_idx = np.argsort(np.array(new_scores))[::-1][:top_k]
       
    for idx in new_idx:
        new_results.append((results[idx][0],new_scores[idx]))
    return new_results,updated_results
    


def score1(ranker,index,query,top_k):
    # print("Scoring")
    # print(query)
    results = ranker.score(index, query, top_k)
    # print(results[:20])
    for res in results[:20]:
        doc_name = index.metadata(res[0]).get('doc_name')
        # print(doc_name,res[1])

    new_results = []
    new_scores = []
    updated_results = {}
    
    for res in results:
        doc_name = index.metadata(res[0]).get('doc_name')
        # print(float(index.metadata(res[0]).get('prior')))
        updated_results[doc_name] =  res[1]+float(index.metadata(res[0]).get('prior') )
        new_scores.append(updated_results[doc_name])

    # print (sorted(updated_results.items(),key=lambda k:k[1],reverse=True)[:10])

    new_idx = np.argsort(np.array(new_scores))[::-1][:10]
       
    for idx in new_idx:
        new_results.append((results[idx][0],new_scores[idx]))
    return new_results
    # return results[:top_k]

if __name__ == '__main__':
  
    cfg = '/Users/bhavya/Documents/explanation/UI/para_idx_data/config.toml'
    with open(cfg,'r') as f:
        print(f.read())

    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    
    query_path = query_cfg.get('query-path', 'slide-queries.txt')
    query_start = query_cfg.get('query-id-start', 1)
    ev = metapy.index.IREval(cfg)


    query = metapy.index.Document()
    query.content('WordNet ontology')
    score2(ranker,idx,query)
    
    # with open(query_path) as query_file:
    #     queries = [q.strip('\n') for q in query_file.readlines()]
    # # random.shuffle(queries)
    # qids = list(range(len(queries)))
    # # random.shuffle(qids)
    # folds_div_test = {}
    # folds_div_train = {}
    # for fold in range(1):
    #     st= int(0.0*(fold)*len(queries))
    #     folds_div_test[fold] = qids[st:int(0.0*(fold+1)*len(queries))]
    #     folds_div_train[fold] = []
    #     for qi in qids:
    #         if qi not in folds_div_test[fold]:
    #             folds_div_train[fold].append(qi)


   

    # print('Running queries')

    # overall_avg = {}
    # fig, axs = plt.subplots(3, 3,sharex=True,sharey=True)
    # cnt1 = 0
    # cnt2 = 0
    # fig.text(0.5, 0.04, 'alpha', ha='center')
    # fig.text(0.055, 0.5, 'Recall@3', va='center', rotation='vertical')
    # with open('garbage.txt','w',buffering=0) as f:
    #     for fold in range(1):
    #         train_queries = []
    #         test_queries = []
    #         train_qids = []
    #         test_qids = []
    #         for qidx,q in enumerate(queries):
    #             if qidx in folds_div_test[fold]:
    #                 test_queries.append(q)
    #                 test_qids.append(qidx)
    #             else:
    #                 train_queries.append(q)
    #                 train_qids.append(qidx)
    #         print(len(train_queries),len(test_queries))
    #         top_k = 3
    #         best_ndcg1 = 0
    #         best1_params = 0
    #         best_ndcg2 = 0
    #         best2_params = [0,0]

           
    #         for mu in np.arange(1000,5500,500):
    #             print(fold,top_k,mu)
    #             plt_ndcg1 = []
    #             plt_ndcg2 = []
    #             for alpha in np.arange(0,1.01,0.01):


    #                 ndcg1 = 0.0
    #                 ndcg2 = 0.0
    #                 ndcg1_arr = []
    #                 ndcg2_arr = []

    #                 num_queries = 0
                    
    #                 for query_num, line in enumerate(train_queries):
    #                     ranker = load_ranker(cfg,mu)
    #                     # print(line)
    #                     query.content(line.strip())
    #                     results1 = score1(ranker,idx, query,top_k)
    #                     results2 = score2(ranker,idx,query,top_k,alpha)
    #                     # if ev.ndcg(results1, query_start + query_num, top_k)<ev.ndcg(results2, query_start + query_num, top_k):
    #                     #     print(query_num,results1[:top_k],results2[:top_k])
    #                     #     print( query.content(),ev.ndcg(results1, query_start + query_num, top_k),ev.ndcg(results2, query_start + query_num, top_k))
    #                     # f.write(ev.ndcg(results2, query_start + query_num, top_k))
    #                     tmp1 = ev.recall(results1, train_qids[query_num]+query_start, top_k)
    #                     ndcg1 += tmp1
    #                     ndcg1_arr.append(tmp1)
    #                     tmp2 = ev.recall(results2, train_qids[query_num]+query_start, top_k)
    #                     ndcg2 += tmp2
    #                     ndcg2_arr.append(tmp2)
    #                     num_queries+=1
    #                 ndcg1= ndcg1 / num_queries
    #                 ndcg2= ndcg2 / num_queries
                    
    #                 if ndcg1>best_ndcg1:
    #                     best_ndcg1 = ndcg1
    #                     best1_params = mu 
    #                 if ndcg2>best_ndcg2:
    #                     best_ndcg2 = ndcg2
    #                     best2_params = [mu,alpha] 
    #                 plt_ndcg2.append(ndcg2)
    #                 plt_ndcg1.append(ndcg1)
    #                 # f.write("Fold {} top {} {} {} {} {} \n".format(fold,top_k,ndcg1,ndcg2,mu,alpha))
    #                 # f.write(str(tt(ndcg1_arr,ndcg2_arr)))
    #                 print(ndcg1,ndcg2,best1_params,best2_params)

    #             axs[cnt1,cnt2].plot(list(np.arange(0,1.01,0.01)),plt_ndcg1,'k-.',linewidth=1,markersize=3)
    #             axs[cnt1,cnt2].plot(list(np.arange(0,1.01,0.01)),plt_ndcg2,'r-.',linewidth=1,markersize=3)
    #             axs[cnt1,cnt2].set_title('mu = {}'.format(mu))
    #             axs[cnt1,cnt2].grid()
    #             axs[cnt1,cnt2].set_ylim([0.69,0.73])
                
    #             # axs[cnt1,cnt2].legend(loc="upper right")
    #             cnt2 += 1
    #             if cnt2 == 3:
    #                 cnt1+= 1
    #                 cnt2 = 0
    #     print(best1_params,best2_params)
    #     plt.show()
            # f.write("Fold {} top {}\n".format(fold,top_k))
            # f.write("Train\n")
            # f.write("NDCG1: {} \t{} \n".format(best_ndcg1,best1_params))
            # f.write("NDCG2: {} \t{} \t{}\n".format(best_ndcg2,best2_params[0],best2_params[1]))
            # f.write("Test:\n")
            # print(best1_params,best2_params)
    # best1_params = 3000
    # best2_params = [2500,0.34]
    # test_queries = queries
    # test_qids = qids
    # with open('complete.txt','w') as f:
    #         for top_k in [1,2,3]:
    #             print(top_k)
    #             ndcg1 = 0.0
    #             ndcg2 = 0.0
    #             avg_p1 = 0.0
    #             avg_p2 = 0.0
    #             avg_recall1 = 0.0
    #             avg_recall2 = 0.0
    #             ndcg1_arr = []
    #             ndcg2_arr = []
    #             avgp1_arr = []
    #             avgp2_arr = []
    #             avgr1_arr = []
    #             avgr2_arr = []
    #             num_queries = 0
    #             sgn = 0
                

    #             for query_num, line in enumerate(test_queries):
    #                 ranker = load_ranker(cfg,best1_params)
    #                 query.content(line.strip())
    #                 results1 = score1(ranker,idx, query,top_k)
    #                 tmp1 = ev.ndcg(results1, test_qids[query_num]+query_start, top_k)
    #                 ndcg1 += tmp1
    #                 ndcg1_arr.append(tmp1)
    #                 ranker = load_ranker(cfg,best2_params[0])
    #                 query.content(line.strip())
    #                 results2 = score2(ranker,idx, query,top_k,best2_params[1])
    #                 tmp2 = ev.ndcg(results2, test_qids[query_num]+query_start, top_k)
    #                 ndcg2 += tmp2
    #                 ndcg2_arr.append(tmp2)

                    
    #                 # if tmp1>tmp2:
    #                 #     print("1>2\n")
    #                 #     print(query.content(),tmp1,tmp2,results1,results2)
    #                 sgn += (tmp2-tmp1)<0
    #                 if tmp1<tmp2:
    #                     print("1<2\n")
    #                     print(query.content(),tmp1,tmp2,results1,results2)
    #                 tmp1 = ev.recall(results1, test_qids[query_num]+query_start, top_k)
    #                 avg_recall1 += tmp1
    #                 avgr1_arr.append(tmp1)
    #                 tmp1 = ev.avg_p(results1, test_qids[query_num]+query_start, top_k)
    #                 avg_p1 += tmp1
    #                 avgp1_arr.append(tmp1)
                    
                    
    #                 tmp2 = ev.recall(results2, test_qids[query_num]+query_start, top_k)
    #                 avg_recall2 += tmp2
    #                 avgr2_arr.append(tmp2)
    #                 tmp2 = ev.avg_p(results2, test_qids[query_num]+query_start, top_k)
    #                 avg_p2 += tmp2
    #                 avgp2_arr.append(tmp2)
    #                 num_queries+=1

    #             ndcg1= ndcg1 / num_queries
               

    #             ndcg2= ndcg2 / num_queries
    #             avg_recall1= avg_recall1 / num_queries
               

    #             avg_recall2= avg_recall2 / num_queries
    #             avg_p1= avg_p1 / num_queries
               

    #             avg_p2= avg_p2 / num_queries
    #             sgn = sgn/float(num_queries)
    #             print(len(ndcg1_arr),len(ndcg2_arr),len(avgp2_arr),len(avgp1_arr),len(avgp1_arr),len(avgr2_arr))

    #             f.write("NDCG1: {}  \n".format(ndcg1))
    #             f.write("NDCG2: {}  \n".format(ndcg2))
    #             # print(np.std(np.array(ndcg1_arr)),np.std(np.array(ndcg2_arr)))
    #             f.write(str(ndcg1_arr))
    #             f.write('\n')
    #             f.write(str(ndcg2_arr))
    #             f.write(str(sgn))
    #             f.write('\n')
    #             f.write("pvalue: {} \n".format(wilcoxon(ndcg1_arr,ndcg2_arr)))
    #             f.write("AVG1: {}  \n".format(avg_p1))
    #             f.write("AVG2: {}  \n".format(avg_p2))
    #             f.write("pvalue: {} \n".format(wilcoxon(avgp1_arr,avgp2_arr)))
    #             f.write("rec1: {}  \n".format(avg_recall1))
    #             f.write("rec2: {}  \n".format(avg_recall2))
    #             f.write("pvalue: {} \n".format(wilcoxon(avgr1_arr,avgr2_arr)))
    #     #         try:
        #             overall_avg['train_ndcg1_{}'.format(top_k)].append(best_ndcg1)
        #             overall_avg['test_ndcg1_{}'.format(top_k)].append(ndcg1)
        #             overall_avg['train_ndcg2_{}'.format(top_k)].append(best_ndcg2)
        #             overall_avg['test_ndcg2_{}'.format(top_k)].append(ndcg2)
        #             overall_avg['test_r1_{}'.format(top_k)].append(avg_recall1)
        #             overall_avg['test_r2_{}'.format(top_k)].append(avg_recall2)
        #             overall_avg['test_p1_{}'.format(top_k)].append(avg_p1)
        #             overall_avg['test_p2_{}'.format(top_k)].append(avg_p2)
        #         except:

        #             overall_avg['train_ndcg1_{}'.format(top_k)] = [best_ndcg1]
        #             overall_avg['test_ndcg1_{}'.format(top_k)] = [ndcg1]
        #             overall_avg['train_ndcg2_{}'.format(top_k)] = [best_ndcg2]
        #             overall_avg['test_ndcg2_{}'.format(top_k)] = [ndcg2]
        #             overall_avg['test_r1_{}'.format(top_k)] = [avg_recall1]
        #             overall_avg['test_r2_{}'.format(top_k)] = [avg_recall2]
        #             overall_avg['test_p1_{}'.format(top_k)] = [avg_p1]
        #             overall_avg['test_p2_{}'.format(top_k)] = [avg_p2]

        # f.write('#'*20+'\n')


        # for top_k in [1,3,5]:
            
        #     f.write("TOp k {}\n".format(top_k))
        #     f.write('Train avg ndcg1: {} \t {}\t Train avg ndcg2: {}\t {}\tTest avg ndcg1: {} \t {}\tTest avg ndcg2: {}\t{}\t \n\n'.format(np.average(np.array(overall_avg['train_ndcg1_{}'.format(top_k)])),1.96*np.std(np.array(overall_avg['train_ndcg1_{}'.format(top_k)])),np.average(np.array(overall_avg['train_ndcg2_{}'.format(top_k)])),1.96*np.std(np.array(overall_avg['train_ndcg2_{}'.format(top_k)])),np.average(np.array(overall_avg['test_ndcg1_{}'.format(top_k)])),1.96*np.std(np.array(overall_avg['test_ndcg1_{}'.format(top_k)])),np.average(np.array(overall_avg['test_ndcg2_{}'.format(top_k)])),1.96*np.std(np.array(overall_avg['test_ndcg2_{}'.format(top_k)]))))

        #     f.write('Test avg p1: {} \t {}\tTest avg p2: {}\t{}\t Test avg r1: {} \t {}\tTest avg r2: {}\t{}\t\n'.format(np.average(np.array(overall_avg['test_p1_{}'.format(top_k)])),1.96*np.std(np.array(overall_avg['test_p1_{}'.format(top_k)])),np.average(np.array(overall_avg['test_p2_{}'.format(top_k)])),1.96*np.std(np.array(overall_avg['test_p2_{}'.format(top_k)])),np.average(np.array(overall_avg['test_r1_{}'.format(top_k)])),1.96*np.std(np.array(overall_avg['test_r1_{}'.format(top_k)])),np.average(np.array(overall_avg['test_r2_{}'.format(top_k)])),1.96*np.std(np.array(overall_avg['test_r2_{}'.format(top_k)]))))

                                        
                    # f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(mu,alpha,top_k, ndcg1,ndcg2,(ndcg2-ndcg1)/ndcg1,tt(ndcg1_arr,ndcg2_arr)))
                    # print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
                    # print(tt(ndcg1_arr,ndcg2_arr))
